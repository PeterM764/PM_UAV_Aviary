import unittest
import numpy as np
import os
import openmdao.api as om

from aviary.subsystems.mass.UAV_mass.wing import WingMass
from openmdao.utils.assert_utils import assert_near_equal, assert_check_partials
from aviary.subsystems.mass.UAV_mass.variable_info.mass_variables import Aircraft

class TestWingMass(unittest.TestCase):
    #Creates a separate problem for tests for each wing design
    def build_problem(self, wing_type):
        prob = om.Problem()
        wm = WingMass()
        prob.model.add_subsystem('wing', wm, promotes_inputs=['*'], promotes_outputs=['*'])

        #Rib definitions
        ribs = np.array([0] * 15 + [1] * 5)
        rib_materials = ['Balsa'] * 15 + ['Ply'] * 5
        rib_thicks = np.where(ribs != 0, 0.125, 0.125)

        wm.options[Aircraft.Wing.RIB_MATERIALS] = rib_materials
        wm.options[Aircraft.Wing.RIB_THICKNESS] = (rib_thicks, 'inch')

        #Airfoil path
        airfoil = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils', 'mh84-il.csv'))

        #Tests for the simple wing design
        if wing_type == "simple":
            wm.options[Aircraft.Wing.TYPE] = 'simple'
            wm.options[Aircraft.Wing.FOAM_DENSITY] = (2.0, 'lb/ft**3')
            wm.options[Aircraft.Wing.ROD_DENSITY] = (0.056, 'lb/inch**3')
            wm.options[Aircraft.Wing.ROD_RADIUS] = (0.00635, 'inch')
            wm.options[Aircraft.Wing.ROD_THICKNESS] = (0.00127, 'inch')
            wm.options[Aircraft.Wing.AIRFOIL_PATH] = airfoil

        #Tests for the medium wing design
        elif wing_type == "medium":
            wm.options[Aircraft.Wing.TYPE] = 'medium'
            wm.options[Aircraft.Wing.RIB_LIGHTENING_FACTOR] = 2/3
            wm.options[Aircraft.Wing.NUM_SPARS] = 1.1
            wm.options[Aircraft.Wing.SPAR_OUTER_DIAMETER] = (1, 'inch')       
            wm.options[Aircraft.Wing.SPAR_WALL_THICKNESS] = (0.0625, 'inch')            
            wm.options[Aircraft.Wing.SPAR_DENSITY] = (2, 'g/cm**3')          
            wm.options[Aircraft.Wing.SKIN_DENSITY] = (20, 'g/m**3')          
            wm.options[Aircraft.Wing.GLUE_FACTOR] = 0.15
            wm.options[Aircraft.Wing.STRINGER_THICKNESS] = (0.375, 'inch')           
            wm.options[Aircraft.Wing.STRINGER_DENSITY] = (160, 'kg/m**3')            
            wm.options[Aircraft.Wing.NUM_STRINGERS] = 2.5
            wm.options[Aircraft.Wing.SHEETING_THICKNESS] = (0.03125, 'inch')
            wm.options[Aircraft.Wing.SHEETING_DENSITY] = (160, 'kg/m**3')            
            wm.options[Aircraft.Wing.SHEETING_COVERAGE] = 0.4
            wm.options[Aircraft.Wing.SHEETING_LIGHTENING_FACTOR] = 1.0
            wm.options[Aircraft.Wing.AIRFOIL_PATH] = airfoil
            wm.options[Aircraft.Wing.MISC_MASS] = (0.0, 'kg')

        # Inputs
        prob.setup(force_alloc_complex=True)
        prob.set_val(Aircraft.Wing.ROOT_CHORD, 20, units='inch')
        prob.set_val(Aircraft.Wing.SPAN, 4.667, units='ft')
        prob.set_val(Aircraft.Wing.WETTED_AREA, 0.85, units='m**2')

        return prob

    #Simple wing test
    def test_simple_mass(self):
        prob = self.build_problem("simple")
        prob.run_model()

        actual = prob.get_val(Aircraft.Wing.MASS, units='kg')
        expected = 0.89953798
        assert_near_equal(actual, expected, tolerance=1e-6)

    #Medium wing test
    def test_medium_mass(self):
        prob = self.build_problem("medium")
        prob.run_model()

        actual = prob.get_val(Aircraft.Wing.MASS, units='kg')
        expected = 0.7985493

        assert_near_equal(actual, expected, tolerance=1e-6)

    #Partials test
    def test_partials_1(self):
        prob = self.build_problem("medium")
        prob.run_model()
        partials = prob.check_partials(compact_print=False, method='cs')
        assert_check_partials(partials, atol=1e-6, rtol=1e-6)

    def test_partials_2(self):
        prob = self.build_problem("simple")
        prob.run_model()
        partials = prob.check_partials(compact_print=False, method='cs')
        assert_check_partials(partials, atol=1e-6, rtol=1e-6)


if __name__ == '__main__':
    unittest.main()