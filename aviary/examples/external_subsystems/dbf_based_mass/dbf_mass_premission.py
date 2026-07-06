import openmdao.api as om
import aviary.api as av
from aviary.examples.external_subsystems.dbf_based_mass.dbf_wing import DBFWingMass
from aviary.examples.external_subsystems.dbf_based_mass.dbf_fuselage import DBFFuselageMass
from aviary.examples.external_subsystems.dbf_based_mass.dbf_horizontaltail import DBFHorizontalTailMass
from aviary.examples.external_subsystems.dbf_based_mass.dbf_verticaltail import DBFVerticalTailMass
from aviary.examples.external_subsystems.dbf_based_mass.mass_summation import MassSummation
from aviary.examples.external_subsystems.dbf_based_mass.dbf_variable_info.dbf_mass_variables import Aircraft

class MassPremission(om.Group):
    def initialize(self):
        self.options.declare("aviary_inputs", types=av.AviaryValues)
        self.options.declare("subsystem_options", types=dict, default={})
    
    def setup(self):

        # Pull the options dictionary the builder passed in
        opts = self.options["subsystem_options"]

        wing = DBFWingMass()
        for key, val in opts.items():
            if key.startswith("aircraft:wing:dbf"):
                wing.options[key] = val

        self.add_subsystem(
            'wing_mass',
            wing,
            promotes_inputs=['*'],
            promotes_outputs=[Aircraft.Wing.MASS],
        )

        htail = DBFHorizontalTailMass()
        for key, val in opts.items():
            if key.startswith("aircraft:horizontal_tail:dbf"):
                htail.options[key] = val

        self.add_subsystem(
            'horizontal_tail_mass',
            htail,
            promotes_inputs=['*'],
            promotes_outputs=[Aircraft.HorizontalTail.MASS],
        )

        vtail = DBFVerticalTailMass()
        for key, val in opts.items():
            if key.startswith("aircraft:vertical_tail:dbf"):
                vtail.options[key] = val

        self.add_subsystem(
            'vertical_tail_mass',
            vtail,
            promotes_inputs=['*'],
            promotes_outputs=[Aircraft.VerticalTail.MASS],
        )

        fus = DBFFuselageMass()
        for key, val in opts.items():
            if key.startswith("aircraft:fuselage:dbf"):
                fus.options[key] = val

        self.add_subsystem(
            'fuselage_mass',
            fus,
            promotes_inputs=['*'],
            promotes_outputs=[Aircraft.Fuselage.MASS],
        )

        self.add_subsystem(
            'mass_group',
            MassSummation(),
            promotes_inputs=['*'],
            promotes_outputs=['*']
        )