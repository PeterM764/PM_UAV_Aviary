import unittest
import openmdao.api as om
import numpy as np

from aviary.examples.external_subsystems.dbf_based_mass.dbf_mass_premission import MassPremission
from aviary.variable_info.variables import Aircraft

class TestMassPremission(unittest.TestCase):

    def setUp(self):
        self.prob = om.Problem(model=MassPremission())
        self.prob.setup()

        #minimal required dbf options and parameters below

        rib_materials = ["Balsa"] * 20
        rib_thicks = np.ones(20) * 0.125

        # Wing
        wing = self.prob.model.wing_mass
        wing.options[Aircraft.Wing.Dbf.RIB_MATERIALS] = rib_materials
        wing.set_option(Aircraft.Wing.Dbf.RIB_THICKNESS, rib_thicks, units="inch")
        wing.options[Aircraft.Wing.Dbf.AIRFOIL_PATH] = "aviary/examples/external_subsystems/dbf_based_mass/mh84-il.csv"

        # Horizontal tail
        htail = self.prob.model.horizontal_tail_mass
        htail.options[Aircraft.HorizontalTail.Dbf.RIB_MATERIALS] = rib_materials
        htail.set_option(Aircraft.HorizontalTail.Dbf.RIB_THICKNESS, rib_thicks, units="inch")
        htail.options[Aircraft.HorizontalTail.Dbf.AIRFOIL_PATH] = "aviary/examples/external_subsystems/dbf_based_mass/mh84-il.csv"

        # Vertical tail
        vtail = self.prob.model.vertical_tail_mass
        vtail.options[Aircraft.VerticalTail.Dbf.RIB_MATERIALS] = rib_materials
        vtail.set_option(Aircraft.VerticalTail.Dbf.RIB_THICKNESS, rib_thicks, units="inch")
        vtail.options[Aircraft.VerticalTail.Dbf.AIRFOIL_PATH] = "aviary/examples/external_subsystems/dbf_based_mass/mh84-il.csv"

        # Fuselage (bulkheads instead of ribs)
        fuse = self.prob.model.fuselage_mass
        fuse.options[Aircraft.Fuselage.Dbf.BULKHEAD_MATERIALS] = rib_materials
        fuse.set_option(Aircraft.Fuselage.Dbf.BULKHEAD_THICKNESS, rib_thicks, units="inch")

        # --- MINIMAL GEOMETRY ---
        self.prob.set_val(Aircraft.Wing.SPAN, 4.0, units="m")
        self.prob.set_val(Aircraft.Wing.ROOT_CHORD, 1.0, units="m")
        self.prob.set_val(Aircraft.Wing.WETTED_AREA, 3.0, units="m**2")

        self.prob.set_val(Aircraft.HorizontalTail.SPAN, 2.0, units="m")
        self.prob.set_val(Aircraft.HorizontalTail.ROOT_CHORD, 0.5, units="m")
        self.prob.set_val(Aircraft.HorizontalTail.WETTED_AREA, 1.0, units="m**2")

        self.prob.set_val(Aircraft.VerticalTail.SPAN, 2.0, units="m")
        self.prob.set_val(Aircraft.VerticalTail.ROOT_CHORD, 0.5, units="m")
        self.prob.set_val(Aircraft.VerticalTail.WETTED_AREA, 1.0, units="m**2")

        self.prob.set_val(Aircraft.Fuselage.LENGTH, 1.2, units="m")
        self.prob.set_val(Aircraft.Fuselage.AVG_HEIGHT, 0.12, units="m")
        self.prob.set_val(Aircraft.Fuselage.AVG_WIDTH, 0.10, units="m")
        self.prob.set_val(Aircraft.Fuselage.WETTED_AREA, 0.58, units="m**2")

        self.prob.run_model()

    def test_outputs_exist(self):
        wing = self.prob.get_val(Aircraft.Wing.MASS)[0]
        htail   = self.prob.get_val(Aircraft.HorizontalTail.MASS)[0]
        vtail   = self.prob.get_val(Aircraft.VerticalTail.MASS)[0]
        fuselage = self.prob.get_val(Aircraft.Fuselage.MASS)[0]
        total = self.prob.get_val(Aircraft.Design.STRUCTURE_MASS)[0]

        self.assertTrue(wing > 0)
        self.assertTrue(htail > 0)
        self.assertTrue(vtail > 0)
        self.assertTrue(fuselage > 0)
        self.assertTrue(total > 0)

    def test_sum(self):
        wing = self.prob.get_val(Aircraft.Wing.MASS)[0]
        htail   = self.prob.get_val(Aircraft.HorizontalTail.MASS)[0]
        vtail   = self.prob.get_val(Aircraft.VerticalTail.MASS)[0]
        fuselage = self.prob.get_val(Aircraft.Fuselage.MASS)[0]
        total = self.prob.get_val(Aircraft.Design.STRUCTURE_MASS)[0]

        self.assertAlmostEqual(total, 50.1555346, places=6)

if __name__ == "__main__":
    unittest.main()