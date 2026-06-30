import unittest
import numpy as np
import os

import openmdao.api as om
from aviary.examples.external_subsystems.dbf_based_mass.dbf_wing import DBFWingMass
from openmdao.utils.assert_utils import assert_near_equal, assert_check_partials
from aviary.examples.external_subsystems.dbf_based_mass.dbf_variable_info.dbf_mass_variables import Aircraft

class TestDBFWingMass(unittest.TestCase):
    def setUp(self):
        self.prob = om.Problem()
        self.dbf = DBFWingMass()

        self.prob.model.add_subsystem(
            'dbf_wing', self.dbf, promotes_inputs=['*'], promotes_outputs=['*']
        )

        # Set required options
        ribs = np.array([0] * 15 + [1] * 5)
        rib_materials = ['Balsa'] * 15 + ['Ply'] * 5
        rib_thicks = np.where(ribs != 0, 0.125, 0.125)
        
        self.dbf.options[Aircraft.Wing.Dbf.TYPE] = 'medium'
        self.dbf.set_option(Aircraft.Wing.Dbf.FOAM_DENSITY, val=2.0, units='kg/m**3')
        self.dbf.set_option(Aircraft.Wing.Dbf.ROD_DENSITY, val=1000, units='kg/m**3')
        self.dbf.set_option(Aircraft.Wing.Dbf.ROD_RADIUS, val=0.015, units='m')
        self.dbf.set_option(Aircraft.Wing.Dbf.ROD_THICKNESS, val=0.005, units='m')

        self.dbf.options[Aircraft.Wing.Dbf.RIB_MATERIALS] = rib_materials
        self.dbf.set_option(Aircraft.Wing.Dbf.RIB_THICKNESS, val=rib_thicks, units='inch')
        self.dbf.set_option(Aircraft.Wing.Dbf.RIB_LIGHTENING_FACTOR, val=2/3, units='unitless')
        self.dbf.set_option(Aircraft.Wing.Dbf.NUM_SPARS, val=1.1, units='unitless')
        self.dbf.set_option(Aircraft.Wing.Dbf.SPAR_OUTER_DIAMETER, val=1, units='inch')
        self.dbf.set_option(Aircraft.Wing.Dbf.SPAR_WALL_THICKNESS, val=0.0625, units='inch')
        self.dbf.set_option(Aircraft.Wing.Dbf.SPAR_DENSITY, val=2, units='g/cm**3')
        self.dbf.set_option(Aircraft.Wing.Dbf.SKIN_DENSITY, val=20, units='g/m**2')
        self.dbf.set_option(Aircraft.Wing.Dbf.GLUE_FACTOR, val=0.15, units='unitless')
        self.dbf.set_option(Aircraft.Wing.Dbf.STRINGER_THICKNESS, val=0.375, units='inch')
        self.dbf.set_option(Aircraft.Wing.Dbf.STRINGER_DENSITY, val=160, units='kg/m**3')
        self.dbf.set_option(Aircraft.Wing.Dbf.NUM_STRINGERS, val=2.5, units='unitless')
        self.dbf.set_option(Aircraft.Wing.Dbf.SHEETING_THICKNESS, val=0.03125, units='inch')
        self.dbf.set_option(Aircraft.Wing.Dbf.SHEETING_DENSITY, val=160, units='kg/m**3')
        self.dbf.set_option(Aircraft.Wing.Dbf.SHEETING_COVERAGE, val=0.4, units='unitless')
        self.dbf.set_option(Aircraft.Wing.Dbf.SHEETING_LIGHTENING_FACTOR, val=1.0, units='unitless')
        airfoil = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'option_info', 'mh84-il.csv')
        )  
        self.dbf.options[Aircraft.Wing.Dbf.AIRFOIL_PATH] = airfoil
        self.dbf.set_option(Aircraft.Wing.Dbf.MISC_MASS, val=0.0, units='kg')

        self.prob.setup(force_alloc_complex=True)

        # Inputs to the component (defined via add_aviary_input)
        self.prob.set_val(Aircraft.Wing.ROOT_CHORD, val=20, units='inch')
        self.prob.set_val(Aircraft.Wing.SPAN, val=4.667, units='ft')
        self.prob.set_val(Aircraft.Wing.WETTED_AREA, val=0.85, units='m**2')

    def test_mass_output(self):
        self.prob.run_model()

        actual_mass = self.prob.get_val(Aircraft.Wing.MASS, units='kg')
        print('Computed Mass:', actual_mass)

        expected_mass = 0.799  # <<< Update to match new output once verified
        tol = 1e-2

        assert_near_equal(actual_mass, expected_mass, tolerance=tol)

    def test_partials(self):
        self.prob.run_model() 
        partials_data = self.prob.check_partials(compact_print=False, method='cs')
        assert_check_partials(partials_data, atol=1e-6, rtol=1e-6)

if __name__ == '__main__':
    unittest.main()
