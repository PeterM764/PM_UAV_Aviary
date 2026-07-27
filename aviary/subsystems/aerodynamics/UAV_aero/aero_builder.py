'''
The builder for aero external subsystem. 

inputs: altitude and velocity

outputs: lift, drag, alpha, avg_CL, lifting_surface_CD

parameters: geometry of wing, tail, fuselage; span, root_chord, sweep, etc

QUESTIONS:
    Should there be a PRE-MISSION for an aero external subsystem?

    Do we or do we not need needs_mission_solver,i.e. is there a solver that gets used?

    Is everything being called/used in a way that is up to date with 2026 Aviary?

    Where are the returned outputs being used as opposed to all of the other outputs 
    that warrants them being outputs and not the others?
'''

import openmdao.api as om

import numpy as np
from aviary.subsystems.subsystem_builder import SubsystemBuilder
from aviary.subsystems.aerodynamics.UAV_aero.aero_model import TotalAircraftAero
from aviary.variable_info.variables import Aircraft, Dynamic
from aviary.utils.aviary_values import AviaryValues

class AeroBuilder(SubsystemBuilder):
    def __init__(self, name='UAV_aero'):
        super().__init__(name)
#changed any def get input/output to mission inputs and outputs
    def mission_inputs(self, aviary_inputs=None, user_options=None, subsystem_options=None,
    ):
        return [
            Dynamic.Mission.ALTITUDE,
            Dynamic.Mission.VELOCITY,
            Dynamic.Vehicle.MASS,
            'aircraft:*',
        ]
    
    def mission_outputs(
    self,
    aviary_inputs=None,
    user_options=None,
    subsystem_options=None,
):
        return [
            Dynamic.Vehicle.LIFT,
            Dynamic.Vehicle.DRAG,
            Dynamic.Vehicle.DRAG_COEFFICIENT,
            'alpha',
            Dynamic.Vehicle.LIFT_COEFFICIENT,
            'lifting_surface_CD',
            'CD_fus',
            'CD_vtail',
            'CD_gear',
        ]
    
    def get_parameters(self, aviary_inputs=None, **kwargs):
        params = {}

        params[Aircraft.Wing.SPAN] = {
            'val': '1.0',
            'units': 'm',
            'static_target': True,
        }
        params[Aircraft.Wing.ROOT_CHORD] = {
            'val': '1.0',
            'units': 'm',
            'static_target': True,
        }
        params[Aircraft.Wing.SWEEP] = {
            'val': '0.0',
            'units': 'deg',
            'static_target': True,
        }
        params[Aircraft.Wing.INCIDENCE] = {
            'val': '0.0',
            'units': 'deg',
            'static_target': True
        }
        params[Aircraft.Wing.FUSELAGE_INTERFERENCE_FACTOR] = {
            'val': '0.0',
            'units': 'unitless',
            'static_target': True,
        }
        params[Aircraft.HorizontalTail.SPAN] = {
            'val': '1.0',
            'units': 'm',
            'static_target': True
        }
        params[Aircraft.HorizontalTail.ROOT_CHORD] = {
            'val': '1.0',
            'units': 'm',
            'static_target': True
        }
        params[Aircraft.HorizontalTail.SWEEP] = {
            'val': '0.0',
            'units': 'deg',
            'static_target': True
        }
        params[Aircraft.Fuselage.MAX_HEIGHT] = {
            'val': '1.0',
            'units': 'm',
            'static_target': True
        }
        params[Aircraft.Fuselage.MAX_WIDTH] = {
            'val': '1.0',
            'units': 'm',
            'static_target': True
        }
        params[Aircraft.Fuselage.LENGTH] = {
            'val': '1.0',
            'units': 'm',
            'static_target': True
        }
        params[Aircraft.VerticalTail.SPAN] = {
            'val': '1.0',
            'units': 'm',
            'static_target': True
        }
        params[Aircraft.VerticalTail.ROOT_CHORD] = {
            'val': '1.0',
            'units': 'm',
            'static_target': True
        }
        return params
    
    def build_mission(self, num_nodes, aviary_inputs, **kwargs):
        mission = TotalAircraftAero(
            aviary_inputs=aviary_inputs,
            num_nodes=num_nodes,
        )
        
        #removes the ambiguity for promoted 'velocity' in openaerostruct and dymos
        mission.set_input_defaults(
            'velocity',
            val=np.zeros(num_nodes),
            units='m/s',
        )

        return mission
    
    def needs_mission_solver(self, aviary_inputs=None, subsystem_options=None, **kwargs):
        return True      #changed from false to true