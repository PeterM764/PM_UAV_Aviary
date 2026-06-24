import openmdao.api as om
import aviary.api as av
from aviary.examples.external_subsystems.dbf_based_mass.dbf_wing import DBFWingMass
from aviary.examples.external_subsystems.dbf_based_mass.dbf_fuselage import DBFFuselageMass
from aviary.examples.external_subsystems.dbf_based_mass.dbf_horizontaltail import DBFHorizontalTailMass
from aviary.examples.external_subsystems.dbf_based_mass.dbf_verticaltail import DBFVerticalTailMass
from aviary.examples.external_subsystems.dbf_based_mass.mass_summation import MassSummation
from aviary.examples.external_subsystems.dbf_based_mass.variable_info.dbf_mass_variables import Aircraft

class MassPremission(om.Group):
    def initialize(self):
        self.options.declare("aviary_inputs", types=av.AviaryValues)
        self.options.declare("subsystem_options", types=dict, default={})
    
    def setup(self):
        self.add_subsystem(
            'wing_mass', 
            DBFWingMass(), 
            promotes_inputs=['*'], 
            promotes_outputs=[Aircraft.Wing.MASS],
        )
        self.add_subsystem(
            'horizontal_tail_mass',
            DBFHorizontalTailMass(),
            promotes_inputs=['*'],
            promotes_outputs=[Aircraft.HorizontalTail.MASS],
        )
        self.add_subsystem(
            'vertical_tail_mass',
            DBFVerticalTailMass(),
            promotes_inputs=['*'],
            promotes_outputs=[Aircraft.VerticalTail.MASS],
        )
        self.add_subsystem(
            'fuselage_mass',
            DBFFuselageMass(),
            promotes_inputs=['*'],
            promotes_outputs=[Aircraft.Fuselage.MASS],
        )
        self.add_subsystem(
            'mass_group', 
            MassSummation(), 
            promotes_inputs=['*'], 
            promotes_outputs=['*']
        )
