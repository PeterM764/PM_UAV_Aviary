import openmdao.api as om

from aviary.variable_info.variables import Aircraft
from aviary.variable_info.functions import add_aviary_input, add_aviary_output
from aviary.examples.external_subsystems.UAV_Mass.dbf_variable_info.dbf_mass_variables import Aircraft
from aviary.examples.external_subsystems.UAV_Mass.dbf_variable_info.dbf_mass_variable_metadata import (
    ExtendedMetaData,
)

class MassSummation(om.Group):
    """
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
        
class StructureMass(om.JaxExplicitComponent):
    def setup(self):
        add_aviary_input(self, Aircraft.Wing.MASS, val=0.0, units='kg', meta_data=ExtendedMetaData, primal_name='wmass')
        add_aviary_input(self, Aircraft.Fuselage.MASS, val=0.0, units='kg', meta_data=ExtendedMetaData, primal_name='fmass')
        add_aviary_input(self, Aircraft.HorizontalTail.MASS, val=0.0, units='kg', meta_data=ExtendedMetaData, primal_name='hmass')
        add_aviary_input(self, Aircraft.VerticalTail.MASS, val=0.0, units='kg', meta_data=ExtendedMetaData, primal_name='vmass')
        # More masses can be added, i.e., tail, spars, flaps, etc. as needed
        add_aviary_output(self, Aircraft.Design.STRUCTURE_MASS, units='kg', meta_data=ExtendedMetaData, primal_name='total_mass')

    def compute_primal(self, wmass, fmass, hmass, vmass):
        total_mass = wmass + fmass + hmass + vmass
        return total_mass
