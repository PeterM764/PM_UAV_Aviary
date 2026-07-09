import os

import numpy as np

from aviary.examples.external_subsystems.UAV_Mass.dbf_mass_premission import MassPremission
from aviary.examples.external_subsystems.UAV_Mass.dbf_variable_info.dbf_mass_variables import Aircraft
from aviary.subsystems.subsystem_builder import SubsystemBuilder


_MODULE_DIR = os.path.dirname(__file__)


def _airfoil_path(filename):
    return os.path.abspath(os.path.join(_MODULE_DIR, 'option_info', filename))

class DBFMassBuilder(SubsystemBuilder):
    
    """
    Builder for DBF mass models (wing, htail, vtail, fuselage, ...)
    """
    def build_pre_mission(self, aviary_inputs, subsystem_options=None):
        subsystem_options = subsystem_options or {}

        #Wing subsystem options
        subsystem_options.setdefault('aircraft:wing:dbf:airfoil_path', _airfoil_path('mh84-il.csv'))
        rib_materials = ['Balsa'] * 15 + ['Ply'] * 5
        subsystem_options.setdefault('aircraft:wing:dbf:rib_materials',
            rib_materials
        )
        ribs = np.array([0] * 15 + [1] * 5)
        rib_thicks = np.where(ribs != 0, 0.125, 0.125)
        subsystem_options.setdefault('aircraft:wing:dbf:rib_thickness',
            rib_thicks
        )
        subsystem_options.setdefault('aircraft:wing:dbf:type',
            'medium'
        )

        #Horizontal tail subsystem options
        subsystem_options.setdefault('aircraft:horizontal_tail:dbf:airfoil_path', _airfoil_path('n0012-il.csv'))
        subsystem_options.setdefault('aircraft:horizontal_tail:dbf:rib_materials',
            rib_materials
        )
        subsystem_options.setdefault('aircraft:horizontal_tail:dbf:rib_thickness',
            rib_thicks
        )

        #Vertical tail subsystem options
        subsystem_options.setdefault('aircraft:vertical_tail:dbf:airfoil_path', _airfoil_path('n0012-il.csv'))
        subsystem_options.setdefault('aircraft:vertical_tail:dbf:rib_materials',
            rib_materials
        )
        subsystem_options.setdefault('aircraft:vertical_tail:dbf:rib_thickness',
            rib_thicks
        )

        #Fuselage subsystem options
        bulkhead_materials = np.where(ribs != 0, 'Ply', 'Balsa').tolist()
        subsystem_options.setdefault('aircraft:fuselage:dbf:bulkhead_materials',
            bulkhead_materials
        )
        ribs = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2])
        bulkhead_thicks = np.where(ribs == 2, 0.25, 0.125)
        subsystem_options.setdefault('aircraft:fuselage:dbf:bulkhead_thickness',
            bulkhead_thicks
        )
        
        return MassPremission(

            aviary_inputs = aviary_inputs,
            subsystem_options = subsystem_options,

        )
    def get_design_vars(self, aviary_inputs=None, user_options=None, subsystem_options=None, phase_info=None):
        DVs = {
            Aircraft.Wing.WETTED_AREA: {
                'units': 'm**2',
                'lower': 0.1,
                'upper': 5.0,
                'val': 2.0,  
            },
            Aircraft.Wing.SPAN: {
                'units': 'm',
                'lower': 0.1,
                'upper': 5.0,
                'val': 2.0,  
            },
            Aircraft.Wing.ROOT_CHORD: {
                'units': 'm',
                'lower': 0.1,
                'upper': 1.0,
                'val': 0.5,  
            },
            Aircraft.Fuselage.WETTED_AREA: {
                'units': 'm**2',
                'lower': 0.1,
                'upper': 5.0,
                'val': 2.0,  
            },
            Aircraft.Fuselage.LENGTH: {
                'units': 'm',
                'lower': 0.1,
                'upper': 5.0,
                'val': 1.0,  
            },
            Aircraft.Fuselage.AVG_HEIGHT: {
                'units': 'm',
                'lower': 0.1,
                'upper': 2.0,
                'val': 0.5,  
            },
            Aircraft.Fuselage.AVG_WIDTH: {
                'units': 'm',
                'lower': 0.1,
                'upper': 2.0,
                'val': 0.5,  
            },
            Aircraft.HorizontalTail.SPAN: {
                'units': 'm',
                'lower': 0.1,
                'upper': 5.0,
                'val': 2.0,  
            },
            Aircraft.HorizontalTail.ROOT_CHORD: {
                'units': 'm',
                'lower': 0.1,
                'upper': 5.0,
                'val': 1.0,  
            },
            Aircraft.HorizontalTail.WETTED_AREA: {
                'units': 'm**2',
                'lower': 0.1,
                'upper': 5.0,
                'val': 2.0,  
            },
            Aircraft.VerticalTail.SPAN: {
                'units': 'm',
                'lower': 0.1,
                'upper': 5.0,
                'val': 1.0,  
            },
            Aircraft.VerticalTail.ROOT_CHORD: {
                'units': 'm',
                'lower': 0.1,
                'upper': 1.0,
                'val': 0.5,  
            },
            Aircraft.VerticalTail.WETTED_AREA: {
                'units': 'm**2',
                'lower': 0.1,
                'upper': 5.0,
                'val': 2.0,  
            },
        }
        return DVs
    
    def get_inputs(self):

        return [

            Aircraft.Wing.SPAN,
            Aircraft.Wing.ROOT_CHORD,
            Aircraft.Wing.WETTED_AREA,
            Aircraft.Fuselage.LENGTH,
            Aircraft.Fuselage.AVG_HEIGHT,
            Aircraft.Fuselage.AVG_WIDTH,
            Aircraft.Fuselage.WETTED_AREA,
            Aircraft.HorizontalTail.SPAN,
            Aircraft.HorizontalTail.ROOT_CHORD,
            Aircraft.HorizontalTail.WETTED_AREA,
            Aircraft.VerticalTail.SPAN,
            Aircraft.VerticalTail.ROOT_CHORD,
            Aircraft.VerticalTail.WETTED_AREA,

        ]
    
    def get_outputs(self):

        return [

            Aircraft.Wing.MASS,
            Aircraft.HorizontalTail.MASS,
            Aircraft.VerticalTail.MASS,
            Aircraft.Fuselage.MASS,
            Aircraft.Design.STRUCTURE_MASS,

        ]
