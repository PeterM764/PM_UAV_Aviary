import unittest
import numpy as np
import os

import openmdao.api as om
from aviary.examples.external_subsystems.dbf_based_mass.dbf_wing import DBFWingMass
from openmdao.utils.assert_utils import assert_near_equal, assert_check_partials
from aviary.examples.external_subsystems.dbf_based_mass.dbf_variable_info.dbf_mass_variables import Aircraft


class TestDBFWingMass(unittest.TestCase):
    def build_problem(self, wing_type):

        #Creates a problem for each test

        prob = om.Problem()
        dbf = DBFWingMass()
        prob.model.add_subsystem('dbf_wing', dbf, promotes_inputs=['*'], promotes_outputs=['*'])

        #Rib definitions
        ribs = np.array([0] * 15 + [1] * 5)
        rib_materials = ['Balsa'] * 15 + ['Ply'] * 5
        rib_thicks = np.where(ribs != 0, 0.125, 0.125)
        dbf.options[Aircraft.Wing.Dbf.RIB_MATERIALS] = rib_materials
        dbf.set_option(Aircraft.Wing.Dbf.RIB_THICKNESS, val=rib_thicks, units='inch')

        #Airfoil path
        airfoil = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'option_info', 'mh84-il.csv'))

        #Tests for the simple wing design
        if wing_type == "simple":
            dbf.options[Aircraft.Wing.Dbf.TYPE] = 'simple'
            dbf.set_option(Aircraft.Wing.Dbf.FOAM_DENSITY, val=2.0, units='lb/ft**3')
            dbf.set_option(Aircraft.Wing.Dbf.ROD_DENSITY, val=0.056, units='lb/inch**3')
            dbf.set_option(Aircraft.Wing.Dbf.ROD_RADIUS, val=0.00635, units='inch')
            dbf.set_option(Aircraft.Wing.Dbf.ROD_THICKNESS, val=0.00127, units='inch')
            dbf.options[Aircraft.Wing.Dbf.AIRFOIL_PATH] = airfoil

        #Tests for the medium wing design
        elif wing_type == "medium":
            dbf.options[Aircraft.Wing.Dbf.TYPE] = 'medium'
            dbf.set_option(Aircraft.Wing.Dbf.RIB_LIGHTENING_FACTOR, val=2/3, units='unitless')
            dbf.set_option(Aircraft.Wing.Dbf.NUM_SPARS, val=1.1, units='unitless')
            dbf.set_option(Aircraft.Wing.Dbf.SPAR_OUTER_DIAMETER, val=1, units='inch')
            dbf.set_option(Aircraft.Wing.Dbf.SPAR_WALL_THICKNESS, val=0.0625, units='inch')
            dbf.set_option(Aircraft.Wing.Dbf.SPAR_DENSITY, val=2, units='g/cm**3')
            dbf.set_option(Aircraft.Wing.Dbf.SKIN_DENSITY, val=20, units='g/m**2')
            dbf.set_option(Aircraft.Wing.Dbf.GLUE_FACTOR, val=0.15, units='unitless')
            dbf.set_option(Aircraft.Wing.Dbf.STRINGER_THICKNESS, val=0.375, units='inch')
            dbf.set_option(Aircraft.Wing.Dbf.STRINGER_DENSITY, val=160, units='kg/m**3')
            dbf.set_option(Aircraft.Wing.Dbf.NUM_STRINGERS, val=2.5, units='unitless')
            dbf.set_option(Aircraft.Wing.Dbf.SHEETING_THICKNESS, val=0.03125, units='inch')
            dbf.set_option(Aircraft.Wing.Dbf.SHEETING_DENSITY, val=160, units='kg/m**3')
            dbf.set_option(Aircraft.Wing.Dbf.SHEETING_COVERAGE, val=0.4, units='unitless')
            dbf.set_option(Aircraft.Wing.Dbf.SHEETING_LIGHTENING_FACTOR, val=1.0, units='unitless')
            dbf.options[Aircraft.Wing.Dbf.AIRFOIL_PATH] = airfoil
            dbf.set_option(Aircraft.Wing.Dbf.MISC_MASS, val=0.0, units='kg')

        # Inputs
        prob.setup(force_alloc_complex=True)
        prob.set_val(Aircraft.Wing.ROOT_CHORD, val=20, units='inch')
        prob.set_val(Aircraft.Wing.SPAN, val=4.667, units='ft')
        prob.set_val(Aircraft.Wing.WETTED_AREA, val=0.85, units='m**2')

        return prob

    #Simple wing test
    def test_simple_mass(self):
        prob = self.build_problem("simple")
        prob.run_model()

        actual = prob.get_val(Aircraft.Wing.MASS, units='kg')
        expected = 0.89953798
        assert_near_equal(actual, expected, tolerance=1e-3)

    #Medium wing test
    def test_medium_mass(self):
        prob = self.build_problem("medium")
        prob.run_model()

        actual = prob.get_val(Aircraft.Wing.MASS, units='kg')
        expected = 0.799
        assert_near_equal(actual, expected, tolerance=1e-3)

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
