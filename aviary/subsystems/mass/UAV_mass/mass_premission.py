import openmdao.api as om
import aviary.api as av
from PM_UAV_Aviary.aviary.subsystems.mass.UAV_mass.wing import DBFWingMass
from PM_UAV_Aviary.aviary.subsystems.mass.UAV_mass.fuselage import DBFFuselageMass
from PM_UAV_Aviary.aviary.subsystems.mass.UAV_mass.horizontaltail import DBFHorizontalTailMass
from PM_UAV_Aviary.aviary.subsystems.mass.UAV_mass.verticaltail import DBFVerticalTailMass
from PM_UAV_Aviary.aviary.subsystems.mass.UAV_mass.mass_summation import MassSummation
from PM_UAV_Aviary.aviary.subsystems.mass.UAV_mass.variable_info.mass_variables import Aircraft

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
