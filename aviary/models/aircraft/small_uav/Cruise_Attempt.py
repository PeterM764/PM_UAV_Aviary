from copy import deepcopy
from weakref import ref
import numpy as np
import openmdao.api as om
import aviary.api as av
from aviary.models.aircraft.small_uav.phases.dbf_example_energy_phase import phase_info
from aviary.examples.external_subsystems.dbf_based_mass.dbf_mass_builder import DBFMassBuilder
from aviary.examples.external_subsystems.custom_aero.custom_aero_builder import CustomAeroBuilder
from aviary.subsystems.propulsion.rc_electric.rc_builder import RCBuilder
from aviary.variable_info.dbf_variables import Aircraft


class MeanPowerComp(om.ExplicitComponent):
    def setup(self):
        self.add_input('p_cruise_kw', shape_by_conn=True, units='kW')
        self.add_output('p_avg_kw', val=1.0, units='kW')
        self.declare_partials('p_avg_kw', 'p_cruise_kw', method='fd')

    def compute(self, inputs, outputs):
        outputs['p_avg_kw'] = np.mean(inputs['p_cruise_kw'])



# Builders
# defaults to feedforward power balance; change to power_balance_mode='solver' for solver-based power balance
rc_prop = RCBuilder()

phase_info = deepcopy(phase_info)



phase_info.pop('climb')
phase_info.pop('descent')


#Pre-Mission Mass Model

phase_info['pre_mission']['include_takeoff'] = False
phase_info['pre_mission']['optimize_mass'] = False
phase_info['pre_mission']['external_subsystems'] = [DBFMassBuilder()]


#Setup Cruise

phase_info['cruise']['external_subsystems'] = [CustomAeroBuilder()]

phase_info['cruise']['subsystem_options']['aerodynamics'] = {
    'method': 'external',
}

phase_info['cruise']['user_options'].update({
    'num_segments': 5,
    'order': 3,

    #Fixed Speed
    # Cruise at ~60 ft/s (18.29 m/s, mach ~0.0538). Operating point is throttle ~0.54,
    'mach_optimize': False,
    'mach_initial': (0.0538, 'unitless'),
    'mach_final': (0.0538, 'unitless'),

    # Level Cruise
    'altitude_optimize': False,
    'altitude_initial': (200.0, 'ft'),
    'altitude_final': (200.0, 'ft'),

    #Distance_Target
    'distance_initial': (0.0, 'm'),
    'distance_ref': (1000.0, 'm'),
    'target_distance': (1000.0, 'm'),

    #Scaling
    'mass_ref': (4.0, 'kg'),

    
    # ODE, so a throttle-balance Newton would be exactly singular.)
    'throttle_enforcement': 'control',
    'throttle_bounds': ((0.2, 0.9), 'unitless'),

    #Time 
    'time_initial': (0.0, 's'),
    'time_duration_bounds': ((20,90.0), 's'),


})

# Remove legacy options that are not accepted by the current cruise phase builder.
phase_info['cruise']['user_options'].pop('electric_current_polynomial_order', None)
phase_info['cruise']['user_options'].pop('electric_current_max_polynomial_order', None)

phase_info['cruise']['initial_guesses'] = {
    'time': ([0.0, 54.7], 's'),   # 1 km at ~18.29 m/s (60 ft/s) ~= 54.7 s
    'distance': ([0.0, 1000.0], 'm'),
    'mach': ([0.0538, 0.0538], 'unitless'),

}

# -----------------------------
# Aviary problem
# -----------------------------
prob = av.AviaryProblem(verbosity=0)
prob.options['group_by_pre_opt_post'] = True

prob.load_inputs(
    'validation_cases/validation_data/test_models/small_scale_uav.csv',
    phase_info,
)
prob.load_external_subsystems(external_subsystems=[rc_prop, CustomAeroBuilder()])
prob.aviary_inputs.set_val(Aircraft.Engine.Propeller.PITCH, 12.0, units='inch')


#taking out fuel
prob.aviary_inputs.set_val('aircraft:fuel:ignore_fuel_capacity_constraint', True, units='unitless')
prob.aviary_inputs.set_val('mission:taxi:fuel_mass_taxi_out', 0.0, units='lbm')
prob.aviary_inputs.set_val('mission:taxi:fuel_mass_taxi_in', 0.0, units='lbm')
prob.aviary_inputs.set_val('mission:takeoff:fuel_mass', 0.0, units='lbm')

for _k in ('mission:design:gross_mass', 'aircraft:design:gross_mass', 'mission:gross_mass'):
    try:
        print("Loaded gross mass key:", _k)
        print("Loaded gross mass kg:", prob.aviary_inputs.get_val(_k, units='kg'))
        print("Loaded gross mass lbm:", prob.aviary_inputs.get_val(_k, units='lbm'))
        break
    except KeyError:
        continue

prob.check_and_preprocess_inputs()

prob.add_pre_mission_systems()
prob.add_phases()
prob.add_post_mission_systems()
prob.link_phases()

# Tighten the existing thrust-balance constraint scaling for this mission case
for _thrust_con in (
    'traj.cruise.rhs_all.thrust_residual',
    'traj.phases.cruise.rhs_all.throttle_balance.thrust_residual',
):
    try:
        prob.model.set_constraint_options(_thrust_con, ref=10.0)
        break
    except Exception:
        continue

for _resp in (
    'mission:constraints:mass_residual',
):
    prob.model._static_responses.pop(_resp, None)



prob.add_driver('IPOPT', use_coloring=False, max_iter=15)
prob.driver.opt_settings['print_level'] = 5
prob.driver.opt_settings['mu_strategy'] = 'adaptive'
prob.driver.opt_settings['tol'] = 1e-6
prob.driver.opt_settings['acceptable_tol'] = 1e-6
prob.driver.opt_settings['acceptable_iter'] = 0
prob.driver.opt_settings['constr_viol_tol'] = 1e-7
prob.driver.opt_settings['acceptable_constr_viol_tol'] = 1e-6
prob.driver.options["debug_print"] = ["desvars", "objs", "nl_cons"]

prob.add_design_variables()

# Aviary adds gross-mass DVs with transport-scale defaults (lbm, upper=None).
# Replace them with UAV-scale kg bounds so the optimizer cannot drift to
# unrealistically large mass in this electric cruise case.
prob.model._static_design_vars.pop('aircraft:design:gross_mass', None)
prob.model._static_design_vars.pop('mission:gross_mass', None)
prob.model.add_design_var('aircraft:design:gross_mass', units='kg', lower=2.0, upper=10.0, ref=7.0)


# Objective: MAXIMIZE endurance = battery energy / cruise electric power.
prob.model.add_subsystem(
    'mean_power_comp',
    MeanPowerComp(),
)

prob.model.add_subsystem(
    'endurance_comp',
    om.ExecComp(
        'endurance = energy / (1000.0 * p_avg_kw + 1.0e-3)',
        endurance={'val': 1.0, 'units': 'h'},
        energy={'val': 1.0, 'units': 'W*h'},
        p_avg_kw={'val': 1.0, 'units': 'kW'},
    ),
)
prob.model.connect('aircraft:battery:energy_capacity', 'endurance_comp.energy')
prob.model.connect(
    'traj.cruise.timeseries.electric_power_in_total',
    'mean_power_comp.p_cruise_kw',
)
prob.model.connect('mean_power_comp.p_avg_kw', 'endurance_comp.p_avg_kw')
prob.model.add_objective('endurance_comp.endurance', ref=-1.0)

prob.model.set_input_defaults('aircraft:battery:voltage', val=22.2, units='V')
prob.model.set_input_defaults('aircraft:engine:motor:idle_current', val=2.2, units='A')
prob.model.set_input_defaults('aircraft:engine:motor:max_cont_current', val=100.0, units='A')


prob.setup()

prob.set_solver_print(level=0)



prob.set_initial_guesses()

prob.set_val('aircraft:design:gross_mass', 7.0, units='kg')
prob.set_val('aircraft:battery:voltage', 25.2, units='V')

# Start the motor-sizing design variables strictly INSIDE their bounds. The CSV
# motor mass (0.131 kg, also seen as 0.637) is below the [0.68, 1.12] kg DV bound,
# and an infeasible-to-bounds start makes IPOPT crash. 
prob.set_val('aircraft:engine:motor:mass', 0.45, units='kg')   # mid of [0.25, 0.65] -> KV ~370
prob.set_val('aircraft:engine:motor:idle_current', 2.0, units='A')

#
prob.set_val('traj.cruise.controls:throttle', 0.6, units='unitless')
prob.set_val('traj.cruise.controls:current_flow', 40.0, units='A')
prob.set_val('traj.cruise.controls:current_flow_max', 65, units='A')
prob.set_val('traj.cruise.controls:rpm_lookup', 95, units='rev/s')
prob.set_val('traj.cruise.controls:rpm_lookup_max', 122.0, units='rev/s')

# Run in two steps for continuation robustness.
prob.run_aviary_problem(run_driver=False, suppress_solver_print=True, make_plots=False)
prob.run_aviary_problem(suppress_solver_print=True, make_plots=False)

print("\n===== MASS CHECK =====")

print("Design Gross Mass")
print("kg :", prob.get_val('aircraft:design:gross_mass', units='kg'))
print("lbm:", prob.get_val('aircraft:design:gross_mass', units='lbm'))

print("\nTrajectory Mass")
print("kg :", prob.get_val('traj.cruise.states:mass', units='kg'))
print("lbm:", prob.get_val('traj.cruise.states:mass', units='lbm'))

print("\nSummary Gross Mass")
print("kg :", prob.get_val('mission:gross_mass', units='kg'))
print("lbm:", prob.get_val('mission:gross_mass', units='lbm'))

