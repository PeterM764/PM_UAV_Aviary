import numpy as np
import openmdao.api as om

from aviary.variable_info.variables import Aircraft
from aviary.variable_info.functions import add_aviary_input, add_aviary_output
from aviary.examples.external_subsystems.dbf_based_mass.variable_info.dbf_mass_variables import Aircraft
from aviary.examples.external_subsystems.dbf_based_mass.variable_info.dbf_mass_variable_metadata import (
    ExtendedMetaData,
)

class MassSummation(om.Group):
    """
    Group to compute various design masses for this mass group.
    This group will be expanded greatly as more subsystems are created. 
    """
    def setup(self):
        self.add_subsystem(
            'structure_mass_sum',
            StructureMass(),
            promotes_inputs=[
                Aircraft.Wing.MASS,
                Aircraft.Fuselage.MASS,
                Aircraft.HorizontalTail.MASS,
                Aircraft.VerticalTail.MASS,
            ],
            promotes_outputs=[Aircraft.Design.STRUCTURE_MASS])
        
class StructureMass(om.ExplicitComponent):
    def setup(self):
        add_aviary_input(self, Aircraft.Wing.MASS, val=0.0, units='kg', meta_data=ExtendedMetaData)
        add_aviary_input(self, Aircraft.Fuselage.MASS, val=0.0, units='kg', meta_data=ExtendedMetaData)
        add_aviary_input(self, Aircraft.HorizontalTail.MASS, val=0.0, units='kg', meta_data=ExtendedMetaData)
        add_aviary_input(self, Aircraft.VerticalTail.MASS, val=0.0, units='kg', meta_data=ExtendedMetaData)
        
        # More masses can be added, i.e., tail, spars, flaps, etc. as needed

        add_aviary_output(self, Aircraft.Design.STRUCTURE_MASS, units='kg', meta_data=ExtendedMetaData)

    def compute(self, inputs, outputs):
        outputs[Aircraft.Design.STRUCTURE_MASS] = (
            inputs[Aircraft.Wing.MASS] +
            inputs[Aircraft.Fuselage.MASS] +
            inputs[Aircraft.HorizontalTail.MASS] +
            inputs[Aircraft.VerticalTail.MASS]
        )