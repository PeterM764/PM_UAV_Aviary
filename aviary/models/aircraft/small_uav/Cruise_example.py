import numpy as np
import openmdao.api as om
import aviary.api as av
from aviary.models.aircraft.small_uav.phases.UAV_energy_phase import get_cruise_phase_info
from aviary.subsystems.mass.UAV_mass.mass_builder import MassBuilder as DBFMassBuilder
from aviary.subsystems.mass.UAV_mass.variable_info.mass_variables import Aircraft as DBFAircraft
from aviary.subsystems.aerodynamics.UAV_Aero.custom_aero_builder import CustomAeroBuilder
from aviary.subsystems.propulsion.rc_electric.UAV_Builder import RCBuilder
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

phase_info = get_cruise_phase_info(
    throttle_enforcement='bounded' if rc_prop.power_balance_mode == 'solver' else 'control',
    throttle_bounds=((0.2, 0.9), 'unitless'),
    external_subsystems=[CustomAeroBuilder()],
)


# Aviary problem
prob = av.AviaryProblem(verbosity=0)
prob.options['group_by_pre_opt_post'] = True

prob.load_inputs(
    'validation_cases/validation_data/test_models/small_scale_uav.csv',
    phase_info,
)
prob.load_external_subsystems(external_subsystems=[rc_prop, CustomAeroBuilder(), DBFMassBuilder()])
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


prob.add_driver('IPOPT', use_coloring=False, max_iter=15)
prob.driver.opt_settings['print_level'] = 5
prob.driver.opt_settings['mu_strategy'] = 'adaptive'
prob.driver.opt_settings['tol'] = 1e-6
prob.driver.opt_settings['acceptable_tol'] = 5e-7
prob.driver.opt_settings['acceptable_iter'] = 0
prob.driver.opt_settings['constr_viol_tol'] = 1e-7
prob.driver.opt_settings['acceptable_constr_viol_tol'] = 5e-7
prob.driver.options["debug_print"] = ["desvars", "objs", "nl_cons"]

prob.add_design_variables()





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
prob.model.connect(Aircraft.Battery.ENERGY_CAPACITY, 'endurance_comp.energy')
prob.model.connect(
    'traj.cruise.timeseries.electric_power_in_total',
    'mean_power_comp.p_cruise_kw',
)

prob.model.connect('mean_power_comp.p_avg_kw', 'endurance_comp.p_avg_kw')
# Objective: maximize endurance.
prob.model.add_objective('endurance_comp.endurance', scaler=-1.0)

prob.model.set_input_defaults(Aircraft.Battery.VOLTAGE, val=22.2, units='V')
prob.model.set_input_defaults(Aircraft.Engine.Motor.IDLE_CURRENT, val=2.2, units='A')
prob.model.set_input_defaults(Aircraft.Engine.Motor.MAX_CONT_CURRENT, val=100.0, units='A')

prob.model.add_constraint(Aircraft.Design.GROSS_MASS, lower=4.0, upper=20.0, units='kg')
prob.model.add_constraint('mission:gross_mass', lower=4.0, upper=20.0, units='kg')

# Constrain geometry directly in physical units to prevent optimizer runaway.
prob.model.add_constraint(Aircraft.Fuselage.LENGTH, lower=0.5, upper=2.5, units='m')
prob.model.add_constraint(DBFAircraft.Fuselage.AVG_HEIGHT, lower=0.1, upper=0.6, units='m')
prob.model.add_constraint(DBFAircraft.Fuselage.AVG_WIDTH, lower=0.1, upper=0.6, units='m')

prob.model.add_constraint(Aircraft.Wing.SPAN, lower=1.0, upper=5.0, units='m')
prob.model.add_constraint(Aircraft.Wing.ROOT_CHORD, lower=0.1, upper=1.0, units='m')
prob.model.add_constraint(Aircraft.Wing.WETTED_AREA, lower=0.1, upper=5.0, units='m**2')

prob.model.add_constraint(Aircraft.HorizontalTail.SPAN, lower=0.2, upper=3.0, units='m')
prob.model.add_constraint(Aircraft.HorizontalTail.ROOT_CHORD, lower=0.1, upper=1.5, units='m')
prob.model.add_constraint(Aircraft.HorizontalTail.WETTED_AREA, lower=0.05, upper=2.0, units='m**2')

prob.model.add_constraint(Aircraft.VerticalTail.SPAN, lower=0.2, upper=3.0, units='m')
prob.model.add_constraint(Aircraft.VerticalTail.ROOT_CHORD, lower=0.1, upper=1.5, units='m')
prob.model.add_constraint(Aircraft.VerticalTail.WETTED_AREA, lower=0.05, upper=2.0, units='m**2')


prob.setup()

prob.set_solver_print(level=0)

prob.set_initial_guesses()

prob.set_val(Aircraft.Design.GROSS_MASS, 7.0, units='kg')
prob.set_val('mission:gross_mass', 7.0, units='kg')
prob.set_val(Aircraft.Battery.VOLTAGE, 25.2, units='V')

# Set fuselage wetted area initial value (still optimized as a DV).
prob.set_val(Aircraft.Fuselage.WETTED_AREA, 904.0, units='inch**2')

# Start the motor-sizing design variables strictly INSIDE their bounds. The CSV
# motor mass (0.131 kg, also seen as 0.637) is below the [0.68, 1.12] kg DV bound,
# and an infeasible-to-bounds start makes IPOPT crash. 
prob.set_val(Aircraft.Engine.Motor.MASS, 0.45, units='kg')   # mid of [0.25, 0.65] -> KV ~370
prob.set_val(Aircraft.Engine.Motor.IDLE_CURRENT, 2.0, units='A')

prob.set_val('traj.cruise.controls:throttle', 0.6, units='unitless')
prob.set_val('traj.cruise.controls:current_flow', 40.0, units='A')
prob.set_val(Aircraft.Engine.Motor.MAX_CONT_CURRENT, 65.0, units='A')
prob.set_val('traj.cruise.controls:rpm_lookup', 95, units='rev/s')
prob.set_val('traj.cruise.controls:rpm_lookup_max', 122.0, units='rev/s')


# Run in two steps for continuation robustness.
prob.run_aviary_problem(run_driver=False, suppress_solver_print=True, make_plots=False)


prob.run_aviary_problem(run_driver=True, suppress_solver_print=True, make_plots=False)
