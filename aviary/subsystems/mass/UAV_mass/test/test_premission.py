import unittest
import numpy as np
import openmdao.api as om
import os 

from aviary.subsystems.mass.UAV_mass.mass_premission import MassPremission
from aviary.subsystems.mass.UAV_mass.variable_info.mass_variables import Aircraft

class TestMassPremission(unittest.TestCase):
    def set_defaults(self, comp, Aircraft):
        # Spars
        comp.options[Aircraft.NUM_SPARS] = 0.5
        comp.options[Aircraft.SPAR_OUTER_DIAMETER] = (1, "inch")
        comp.options[Aircraft.SPAR_WALL_THICKNESS] = (0.0625, 'inch')
        comp.options[Aircraft.SPAR_DENSITY] = (2.0, 'g/cm**3')

        # Options that only exist for certain mass components
        if hasattr(Aircraft, "NUM_STRINGERS"):
            comp.options[Aircraft.NUM_STRINGERS] = 4.0
        if hasattr(Aircraft, "FLOOR_THICKNESS"):
            comp.options[Aircraft.FLOOR_THICKNESS] = (0.125, 'inch')
        if hasattr(Aircraft, "FLOOR_DENSITY"):
            comp.options[Aircraft.FLOOR_DENSITY] = (340.0, 'kg/m**3')
        if hasattr(Aircraft, "FLOOR_LENGTH"):
            comp.options[Aircraft.FLOOR_LENGTH] = (2.0, 'ft')
        if hasattr(Aircraft, "STRINGER_THICKNESS"):
            comp.options[Aircraft.STRINGER_THICKNESS] = (0.375, 'inch')
        if hasattr(Aircraft, "STRINGER_DENSITY"):
            comp.options[Aircraft.STRINGER_DENSITY] = (160, 'kg/m**3')
        if hasattr(Aircraft, "BULKHEAD_LIGHTENING_FACTOR"):
            comp.options[Aircraft.BULKHEAD_LIGHTENING_FACTOR] = 0.18
        if hasattr(Aircraft, "FOAM_DENSITY"):
            comp.options[Aircraft.FOAM_DENSITY] = (2.0, 'lb/ft**3')
        if hasattr(Aircraft, "ROD_DENSITY"):
            comp.options[Aircraft.ROD_DENSITY] = (0.056, 'lb/inch**3')
        if hasattr(Aircraft, "ROD_RADIUS"):
            comp.options[Aircraft.ROD_RADIUS] = (0.000529,'ft')
        if hasattr(Aircraft, "ROD_THICKNESS"):
            comp.options[Aircraft.ROD_THICKNESS] = (0.000106,'ft')

        # Sheeting
        comp.options[Aircraft.SHEETING_THICKNESS] = (0.03125, 'inch')
        comp.options[Aircraft.SHEETING_DENSITY] = (160.0, 'kg/m**3')
        comp.options[Aircraft.SHEETING_COVERAGE] = 1.0
        comp.options[Aircraft.SHEETING_LIGHTENING_FACTOR] = 0.3

        # Skin + glue
        comp.options[Aircraft.SKIN_DENSITY] = (20.0, 'g/m**3')
        comp.options[Aircraft.GLUE_FACTOR] = 0.08

        # Misc
        comp.options[Aircraft.MISC_MASS] = (0.0, 'kg')

    def setUp(self):
        base = os.path.dirname(os.path.dirname(__file__))
        airfoil_dir = os.path.join(base, "utils")
        airfoil = os.path.abspath(os.path.join(airfoil_dir, "mh84-il.csv"))

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
        
        #Setting UAV defaults
        self.set_defaults(wing, Aircraft.Wing)
        self.set_defaults(htail, Aircraft.HorizontalTail)
        self.set_defaults(vtail, Aircraft.VerticalTail)
        self.set_defaults(fuse, Aircraft.Fuselage)

        #Setting necessary options
        wing.options[Aircraft.Wing.RIB_MATERIALS] = rib_materials
        wing.options[Aircraft.Wing.RIB_THICKNESS] = (rib_thicks, "inch")
        wing.options[Aircraft.Wing.RIB_LIGHTENING_FACTOR] = 2/3
        wing.options[Aircraft.Wing.AIRFOIL_PATH] = airfoil
        wing.options[Aircraft.Wing.TYPE] = 'medium'

        htail.options[Aircraft.HorizontalTail.RIB_MATERIALS] = rib_materials
        htail.options[Aircraft.HorizontalTail.RIB_THICKNESS] = (rib_thicks, "inch")
        htail.options[Aircraft.HorizontalTail.RIB_LIGHTENING_FACTOR] = 2/3
        htail.options[Aircraft.HorizontalTail.AIRFOIL_PATH] = airfoil

        vtail.options[Aircraft.VerticalTail.RIB_MATERIALS] = rib_materials
        vtail.options[Aircraft.VerticalTail.RIB_THICKNESS] = (rib_thicks, "inch")
        vtail.options[Aircraft.VerticalTail.RIB_LIGHTENING_FACTOR] = 2/3
        vtail.options[Aircraft.VerticalTail.AIRFOIL_PATH] = airfoil
        
        fuse.options[Aircraft.Fuselage.BULKHEAD_MATERIALS] = rib_materials
        fuse.options[Aircraft.Fuselage.BULKHEAD_THICKNESS] = (rib_thicks, "inch")

        #Setting geometry values:
        self.prob.set_val(Aircraft.Wing.SPAN, 4.667, units="ft")
        self.prob.set_val(Aircraft.Wing.ROOT_CHORD, 20, units="inch")
        self.prob.set_val(Aircraft.Wing.WETTED_AREA, 0.85, units="m**2")

        self.prob.set_val(Aircraft.HorizontalTail.ROOT_CHORD, 20.0, units="inch")
        self.prob.set_val(Aircraft.HorizontalTail.SPAN, 4.667, units="ft")
        self.prob.set_val(Aircraft.HorizontalTail.WETTED_AREA, 0.85, units="m**2")

        self.prob.set_val(Aircraft.VerticalTail.ROOT_CHORD, 20.0, units="inch")
        self.prob.set_val(Aircraft.VerticalTail.SPAN, 4.667, units="ft")
        self.prob.set_val(Aircraft.VerticalTail.WETTED_AREA, 0.85, units="m**2")

        self.prob.set_val(Aircraft.Fuselage.LENGTH, 4.0, units="ft")
        self.prob.set_val(Aircraft.Fuselage.AVG_HEIGHT, 5.0, units="inch")
        self.prob.set_val(Aircraft.Fuselage.AVG_WIDTH, 4.0, units="inch")
        self.prob.set_val(Aircraft.Fuselage.WETTED_AREA, 0.583, units="m**2")

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
        expected = 2.0545581

        self.assertAlmostEqual(total[0], expected, places=6)
        print('Expected: ', expected)
        print('Actual: ', total[0])

if __name__ == "__main__":
    unittest.main()