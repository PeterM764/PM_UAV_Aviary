import unittest
import numpy as np
import os

import openmdao.api as om

from aviary.variable_info.variables import Aircraft
from aviary.examples.external_subsystems.dbf_based_mass.dbf_verticaltail import DBFVerticalTailMass
from openmdao.utils.assert_utils import assert_near_equal, assert_check_partials


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

        self.dbf.options[Aircraft.VerticalTail.Dbf.RIB_MATERIALS] = rib_materials
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.RIB_THICKNESS, val=rib_thicks, units='inch')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.RIB_LIGHTENING_FACTOR, val=2/3, units='unitless')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.NUM_SPARS, val=1.1, units='unitless')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.SPAR_OUTER_DIAMETER, val=1, units='inch')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.SPAR_WALL_THICKNESS, val=0.0625, units='inch')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.SPAR_DENSITY, val=2, units='g/cm**3')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.SKIN_DENSITY, val=20, units='g/m**2')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.GLUE_FACTOR, val=0.15, units='unitless')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.STRINGER_THICKNESS, val=0.375, units='inch')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.STRINGER_DENSITY, val=160, units='kg/m**3')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.NUM_STRINGERS, val=2.5, units='unitless')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.SHEETING_THICKNESS, val=0.03125, units='inch')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.SHEETING_DENSITY, val=160, units='kg/m**3')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.SHEETING_COVERAGE, val=0.4, units='unitless')
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.SHEETING_LIGHTENING_FACTOR, val=1.0, units='unitless')
        airfoil = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'mh84-il.csv'))
        self.dbf.options[Aircraft.VerticalTail.Dbf.AIRFOIL_PATH] = airfoil
        self.dbf.set_option(Aircraft.VerticalTail.Dbf.MISC_MASS, val=0.0, units='kg')

        self.prob.setup(force_alloc_complex=True)

        # Inputs to the component (defined via add_aviary_input)
        self.prob.set_val(Aircraft.VerticalTail.ROOT_CHORD, val=20, units='inch')
        self.prob.set_val(Aircraft.VerticalTail.SPAN, val=4.667, units='ft')
        self.prob.set_val(Aircraft.VerticalTail.WETTED_AREA, val=0.85, units='m**2')

    def test_mass_output(self):
        self.prob.run_model()

        actual_mass = self.prob.get_val(Aircraft.VerticalTail.MASS, units='kg')
        print('Computed Mass:', actual_mass)

        expected_mass = 0.798549  # <<< Update to match new output once verified
        tol = 1e-2

        assert_near_equal(actual_mass, expected_mass, tolerance=tol)

    def test_partials(self):
        self.prob.run_model()
        partials_data = self.prob.check_partials(compact_print=True, method='cs')
        assert_check_partials(partials_data, atol=1e-6, rtol=1e-6)


if __name__ == '__main__':
    unittest.main()
