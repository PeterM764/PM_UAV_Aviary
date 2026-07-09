import unittest
import numpy as np
import os
import openmdao.api as om

from aviary.examples.external_subsystems.dbf_based_mass.dbf_verticaltail import DBFVerticalTailMass
from openmdao.utils.assert_utils import assert_near_equal, assert_check_partials
from aviary.examples.external_subsystems.dbf_based_mass.dbf_variable_info.dbf_mass_variables import Aircraft

class TestDBFVerticalTailMass(unittest.TestCase):
    def setUp(self):
        self.prob = om.Problem()
        self.dbf = DBFVerticalTailMass()

        self.prob.model.add_subsystem(
            'dbf_wing', self.dbf, promotes_inputs=['*'], promotes_outputs=['*']
        )

        # Set required options
        ribs = np.array([0] * 15 + [1] * 5)
        rib_materials = ['Balsa'] * 15 + ['Ply'] * 5
        rib_thicks = np.where(ribs != 0, 0.125, 0.125)

        self.dbf.options[Aircraft.VerticalTail.Dbf.STRINGER_THICKNESS] = (0.375, 'inch')
        self.dbf.options[Aircraft.VerticalTail.Dbf.RIB_MATERIALS] = rib_materials
        self.dbf.options[Aircraft.VerticalTail.Dbf.RIB_THICKNESS] = (rib_thicks, 'inch')
        self.dbf.options[Aircraft.VerticalTail.Dbf.RIB_LIGHTENING_FACTOR] = 2/3
        self.dbf.options[Aircraft.VerticalTail.Dbf.NUM_SPARS] = 1.1
        self.dbf.options[Aircraft.VerticalTail.Dbf.SPAR_OUTER_DIAMETER] = (1,'inch')
        self.dbf.options[Aircraft.VerticalTail.Dbf.SPAR_WALL_THICKNESS] = (0.0625, 'inch')
        self.dbf.options[Aircraft.VerticalTail.Dbf.SPAR_DENSITY] = (2.0, 'g/cm**3')
        self.dbf.options[Aircraft.VerticalTail.Dbf.SKIN_DENSITY] = (20.0, 'g/m**3')
        self.dbf.options[Aircraft.VerticalTail.Dbf.GLUE_FACTOR] = 0.15
        self.dbf.options[Aircraft.VerticalTail.Dbf.STRINGER_DENSITY] = (160, 'kg/m**3')
        self.dbf.options[Aircraft.VerticalTail.Dbf.NUM_STRINGERS] = 2.5
        self.dbf.options[Aircraft.VerticalTail.Dbf.SHEETING_THICKNESS] = (0.03125, 'inch')
        self.dbf.options[Aircraft.VerticalTail.Dbf.SHEETING_DENSITY] = (160.0, 'kg/m**3')
        self.dbf.options[Aircraft.VerticalTail.Dbf.SHEETING_COVERAGE] = 0.4
        self.dbf.options[Aircraft.VerticalTail.Dbf.SHEETING_LIGHTENING_FACTOR] = 1.0
        airfoil = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'option_info', 'mh84-il.csv')
        )        
        self.dbf.options[Aircraft.VerticalTail.Dbf.AIRFOIL_PATH] = airfoil
        self.dbf.options[Aircraft.VerticalTail.Dbf.MISC_MASS] = (0.0, 'kg')

        self.prob.setup(force_alloc_complex=True)

        # Inputs to the component (defined via add_aviary_input)
        self.prob.set_val(Aircraft.VerticalTail.ROOT_CHORD, val=20, units='inch')
        self.prob.set_val(Aircraft.VerticalTail.SPAN, val=4.667, units='ft')
        self.prob.set_val(Aircraft.VerticalTail.WETTED_AREA, val=0.85, units='m**2')

    def test_mass_output(self):
        self.prob.run_model()

        actual_mass = self.prob.get_val(Aircraft.VerticalTail.MASS, units='kg')
        print('Computed Mass:', actual_mass)

        expected_mass = 0.79854936 # <<< Update to match new output once verified
        tol = 1e-6

        assert_near_equal(actual_mass, expected_mass, tolerance=tol)

    def test_partials(self):
        self.prob.run_model()
        partials_data = self.prob.check_partials(compact_print=True, method='cs')
        assert_check_partials(partials_data, atol=1e-6, rtol=1e-6)


if __name__ == '__main__':
    unittest.main()
