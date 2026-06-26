import unittest
import numpy as np
import openmdao.api as om
import os 

from aviary.examples.external_subsystems.dbf_based_mass.dbf_mass_premission import MassPremission
from aviary.examples.external_subsystems.dbf_based_mass.dbf_variable_info.dbf_mass_variables import Aircraft

class TestMassPremission(unittest.TestCase):
    def set_dbf_defaults(self, comp, AircraftDbf):
        # Spars
        comp.set_option(AircraftDbf.NUM_SPARS, 0.5, units="unitless")
        comp.set_option(AircraftDbf.SPAR_OUTER_DIAMETER, 1, units="inch")
        comp.set_option(AircraftDbf.SPAR_WALL_THICKNESS, 0.0625, units="inch")
        comp.set_option(AircraftDbf.SPAR_DENSITY, 2.0, units="g/cm**3")

        # Stringers (only if the variable exists)
        if hasattr(AircraftDbf, "NUM_STRINGERS"):
            comp.set_option(AircraftDbf.NUM_STRINGERS, 4, units="unitless")
        if hasattr(AircraftDbf, "FLOOR_THICKNESS"):
            comp.set_option(AircraftDbf.FLOOR_THICKNESS, 0.125, units = 'inch')
        if hasattr(AircraftDbf, "FLOOR_DENSITY"):
            comp.set_option(AircraftDbf.FLOOR_DENSITY, 340, units = 'kg / m**3')
        if hasattr(AircraftDbf, "FLOOR_LENGTH"):
            comp.set_option(AircraftDbf.FLOOR_LENGTH, 2, units = 'ft')
        if hasattr(AircraftDbf, "STRINGER_THICKNESS"):
            comp.set_option(AircraftDbf.STRINGER_THICKNESS, 0.375, units="inch")
        if hasattr(AircraftDbf, "STRINGER_DENSITY"):
            comp.set_option(AircraftDbf.STRINGER_DENSITY, 160, units="kg/m**3")
        if hasattr(AircraftDbf, "BULKHEAD_LIGHTENING_FACTOR"):
            comp.set_option(AircraftDbf.BULKHEAD_LIGHTENING_FACTOR, 0.18, units = 'unitless')

        # Sheeting
        comp.set_option(AircraftDbf.SHEETING_THICKNESS, 0.03125, units="inch")
        comp.set_option(AircraftDbf.SHEETING_DENSITY, 160, units="kg/m**3")
        comp.set_option(AircraftDbf.SHEETING_COVERAGE, 1.0, units="unitless")
        comp.set_option(AircraftDbf.SHEETING_LIGHTENING_FACTOR, 0.3, units="unitless")

        # Skin + glue
        comp.set_option(AircraftDbf.SKIN_DENSITY, 20, units="g/m**2")
        comp.set_option(AircraftDbf.GLUE_FACTOR, 0.08, units="unitless")

        # Misc
        comp.set_option(AircraftDbf.MISC_MASS, 0.0, units="kg")

    def setUp(self):

        base = os.path.dirname(__file__)
        airfoil = os.path.abspath(os.path.join(base, "..", "mh84-il.csv"))

        self.prob = om.Problem()
        self.prob.model = MassPremission()

        self.prob.setup()

        wing = self.prob.model.wing_mass
        htail = self.prob.model.horizontal_tail_mass
        vtail = self.prob.model.vertical_tail_mass
        fuse = self.prob.model.fuselage_mass

        #Setting rib parameters
        rib_materials = ['Balsa'] * 15 + ['Ply'] * 5
        rib_thicks = np.ones(20) * 0.125
        
        #Setting DBF defaults
        self.set_dbf_defaults(wing, Aircraft.Wing.Dbf)
        self.set_dbf_defaults(htail, Aircraft.HorizontalTail.Dbf)
        self.set_dbf_defaults(vtail, Aircraft.VerticalTail.Dbf)
        self.set_dbf_defaults(fuse, Aircraft.Fuselage.Dbf)

        #Setting necessary options
        wing.options[Aircraft.Wing.Dbf.RIB_MATERIALS] = rib_materials
        wing.set_option(Aircraft.Wing.Dbf.RIB_THICKNESS, rib_thicks, units="inch")
        wing.set_option(Aircraft.Wing.Dbf.RIB_LIGHTENING_FACTOR, val = 2/3, units = 'unitless')
        wing.options[Aircraft.Wing.Dbf.AIRFOIL_PATH] = airfoil

        htail.options[Aircraft.HorizontalTail.Dbf.RIB_MATERIALS] = rib_materials
        htail.set_option(Aircraft.HorizontalTail.Dbf.RIB_THICKNESS, rib_thicks, units="inch")
        htail.set_option(Aircraft.HorizontalTail.Dbf.RIB_LIGHTENING_FACTOR, val = 2/3, units = 'unitless')
        htail.options[Aircraft.HorizontalTail.Dbf.AIRFOIL_PATH] = airfoil

        vtail.options[Aircraft.VerticalTail.Dbf.RIB_MATERIALS] = rib_materials
        vtail.set_option(Aircraft.VerticalTail.Dbf.RIB_THICKNESS, rib_thicks, units="inch")
        vtail.set_option(Aircraft.VerticalTail.Dbf.RIB_LIGHTENING_FACTOR, val = 2/3, units = 'unitless')
        vtail.options[Aircraft.VerticalTail.Dbf.AIRFOIL_PATH] = airfoil
        
        fuse.options[Aircraft.Fuselage.Dbf.BULKHEAD_MATERIALS] = rib_materials
        fuse.set_option(Aircraft.Fuselage.Dbf.BULKHEAD_THICKNESS, rib_thicks, units="inch")

        #Setting geometry values:
        self.prob.set_val(Aircraft.Wing.SPAN, 4.0, units="m")
        self.prob.set_val(Aircraft.Wing.ROOT_CHORD, 1.0, units="m")
        self.prob.set_val(Aircraft.Wing.WETTED_AREA, 3.0, units="m**2")

        self.prob.set_val(Aircraft.HorizontalTail.SPAN, 2.0, units="m")
        self.prob.set_val(Aircraft.HorizontalTail.ROOT_CHORD, 0.5, units="m")
        self.prob.set_val(Aircraft.HorizontalTail.WETTED_AREA, 1.0, units="m**2")

        self.prob.set_val(Aircraft.VerticalTail.SPAN, 2.0, units="m")
        self.prob.set_val(Aircraft.VerticalTail.ROOT_CHORD, 0.5, units="m")
        self.prob.set_val(Aircraft.VerticalTail.WETTED_AREA, 1.0, units="m**2")

        self.prob.set_val(Aircraft.Fuselage.LENGTH, 1.2192, units="m")
        self.prob.set_val(Aircraft.Fuselage.AVG_HEIGHT, 0.127, units="m")
        self.prob.set_val(Aircraft.Fuselage.AVG_WIDTH, 0.1016, units="m")
        self.prob.set_val(Aircraft.Fuselage.WETTED_AREA, 0.58322464, units="m ** 2")

        self.prob.run_model()

    def test_outputs_exist(self):

        """Do all promoted mass outputs exist and are they positive?"""

        wing = self.prob.get_val(Aircraft.Wing.MASS)
        ht = self.prob.get_val(Aircraft.HorizontalTail.MASS)
        vt = self.prob.get_val(Aircraft.VerticalTail.MASS)
        fuse = self.prob.get_val(Aircraft.Fuselage.MASS)
        total = self.prob.get_val(Aircraft.Design.STRUCTURE_MASS)

        self.assertTrue(wing > 0)
        self.assertTrue(ht > 0)
        self.assertTrue(vt > 0)
        self.assertTrue(fuse > 0)
        self.assertTrue(total > 0)

    def test_mass_summation(self):
        total = self.prob.get_val(Aircraft.Design.STRUCTURE_MASS)
        expected = 3.56179953
        self.assertAlmostEqual(total[0], expected, places=6)
        print('Expected: ', expected)
        print('Actual: ', total[0])

if __name__ == "__main__":
    unittest.main()