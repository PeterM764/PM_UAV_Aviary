
"""
Climb-only RC-electric small UAV Aviary example.

"""

from copy import deepcopy
from pathlib import Path

import numpy as np
import aviary.api as av

from aviary.models.aircraft.small_uav.phases.dbf_example_energy_phase import (phase_info as base_phase_info,)
from aviary.examples.external_subsystems.dbf_based_mass.dbf_mass_builder import (DBFMassBuilder,)
from aviary.examples.external_subsystems.custom_aero.custom_aero_builder import (CustomAeroBuilder,)
from aviary.subsystems.propulsion.rc_electric.rc_builder import RCBuilder

#phase info can be in a seperate file after debugging
def climb_phase_info():

    phase_info = deepcopy(base_phase_info)

    # Keep climb only.
    phase_info.pop('cruise', None)
    phase_info.pop('descent', None)

    # Disable full-mission/range constraints that need cruise.
    if 'post_mission' in phase_info:
        phase_info['post_mission']['constrain_range'] = False
        phase_info['post_mission']['include_landing'] = False

    # Pre-mission mass model.
    phase_info['pre_mission']['external_subsystems'] = [DBFMassBuilder()]

    # Climb external aero.
    phase_info['climb']['external_subsystems'] = [CustomAeroBuilder()]
    phase_info['climb']['subsystem_options']['aerodynamics'] = {
        'method': 'external',
    }

    # Keep this simple while debugging.
    phase_info['climb']['user_options']['num_segments'] = 4
    phase_info['climb']['user_options']['order'] = 3
    # Remove legacy options that are not accepted by the current climb phase builder.
    phase_info['climb']['user_options'].pop('electric_current_polynomial_order', None)
    phase_info['climb']['user_options'].pop('electric_current_max_polynomial_order', None)
    # Time setup.
    phase_info['climb']['user_options']['time_duration_bounds'] = ((20.0, 90.0), 's')
    phase_info['climb']['initial_guesses']['time'] = ([0.0, 40.0], 's')

    # Fixed Mach.
    phase_info['climb']['user_options']['mach_optimize'] = False
    phase_info['climb']['user_options']['mach_initial'] = (0.02, 'unitless')
    phase_info['climb']['user_options']['mach_final'] = (0.02, 'unitless')
    phase_info['climb']['initial_guesses']['mach'] = ([0.02, 0.02], 'unitless')

    # Fixed climb altitude.
    phase_info['climb']['user_options']['altitude_optimize'] = False
    phase_info['climb']['user_options']['altitude_initial'] = (0.0, 'ft')
    phase_info['climb']['user_options']['altitude_final'] = (200.0, 'ft')
    phase_info['climb']['initial_guesses']['altitude'] = ([0.0, 200.0], 'ft')

    # Mass guess.
    phase_info['climb']['initial_guesses']['mass'] = ([4.6, 4.6], 'kg')

    return phase_info
##phase info will end here

def set_climb_control_guesses(prob):
    
    prob.set_val('traj.climb.controls:current_flow', 20.0, units='A')
    prob.set_val('traj.climb.controls:current_flow_max', 80.0, units='A')


def build_climb(
    optimizer='IPOPT',
    max_iter=300,
    verbosity=1,
):
    """
    Build and setup the climb-only AviaryProblem.
    """
    rc_prop = RCBuilder()
    phase_info = climb_phase_info()

    prob = av.AviaryProblem(verbosity=verbosity)
    prob.options['group_by_pre_opt_post'] = True

    prob.load_inputs(
    'validation_cases/validation_data/test_models/small_scale_uav.csv',
    phase_info,
    )

    prob.load_external_subsystems(
        external_subsystems=[rc_prop, CustomAeroBuilder()]
    )

    prob.check_and_preprocess_inputs()

    prob.add_pre_mission_systems()
    prob.add_phases()
    prob.add_post_mission_systems()

    # Safe to leave this here. With only one phase, there is little to link.
    prob.link_phases()

    prob.add_driver(optimizer)

   
    prob.driver.opt_settings['max_iter'] = 300
    prob.driver.opt_settings['tol'] = 1.0e-6

    prob.driver.options['debug_print'] = []

    prob.add_design_variables()

    # Electric aircraft: fuel burned should stay zero. will only need if adding cruise or other phases
  
    # prob.model.add_constraint(
    #     'mission:summary:fuel_burned',
    #     equals=0.0,
    #     units='lbm',
    #     ref=1.0,
    # )

    # Since the only phase is climb, this minimizes climb time.
    prob.add_objective('time')

    prob.setup()
    prob.set_initial_guesses()
    set_climb_control_guesses(prob)

    return prob


def print_climb_summary(prob):
    
    checks = [
        'gtow_constraint.GTOW',
        'mission:constraints:mass_residual',
        # 'mission:summary:fuel_burned',
        'traj.climb.rhs_all.thrust_residual',
        'traj.climb.t_duration',
    ]

    print("\n" + "=" * 70)
    print("CLIMB-ONLY OPTIMIZATION CHECK SUMMARY")

    for name in checks:
        try:
            val = prob.get_val(name)
            print(f"\n{name}:")
            print(val)
            print("max abs =", abs(val).max())
        except Exception as err:
            print(f"\n{name}: NOT FOUND")
            print(err)

def print_current_debug(prob, label):
    print("\n" + "=" * 60)
    print(label)

    names = [
        ('aircraft:engine:motor:idle_current', 'A'),
        ('aircraft:engine:motor:max_cont_current', 'A'),
        ('aircraft:engine:motor:mass', 'kg'),
        ('traj.climb.controls:current_flow', 'A'),
        ('traj.climb.controls:current_flow_max', 'A'),
    ]

    for name, units in names:
        try:
            print(name, prob.get_val(name, units=units))
        except Exception as err:
            print(name, "NOT FOUND:", err)

def main():
    prob = build_climb()
    print_current_debug(prob, "BEFORE RUN")
    failed = prob.run_aviary_problem(suppress_solver_print=False)
    print("FAILED =", failed)
    print_current_debug(prob, "AFTER RUN")
    print_climb_summary(prob)

    output_file = Path(__file__).parent / "climb_only_newvars.txt"
    with open(output_file, "w") as f:
        prob.model.list_vars(print_arrays=True, out_stream=f, units=True)


if __name__ == '__main__':
    main()
    