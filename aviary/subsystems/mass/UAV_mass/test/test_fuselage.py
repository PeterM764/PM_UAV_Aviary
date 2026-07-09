import unittest
import numpy as np
import openmdao.api as om

from PM_UAV_Aviary.aviary.subsystems.mass.UAV_mass.fuselage import DBFFuselageMass
from openmdao.utils.assert_utils import assert_near_equal, assert_check_partials
from PM_UAV_Aviary.aviary.subsystems.mass.UAV_mass.variable_info.mass_variables import Aircraft

class TestDBFFuselageMass(unittest.TestCase):
    def setUp(self):
        self.prob = om.Problem()
        self.dbf = DBFFuselageMass()

        self.prob.model.add_subsystem(
            'dbf_fuselage', self.dbf, promotes_inputs=['*'], promotes_outputs=['*']
        )

        ribs = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2])
        bulkhead_materials = np.where(ribs != 0, 'Ply', 'Balsa').tolist()
        rib_thicks = np.where(ribs == 2, 0.25, 0.125)

        self.dbf.options[Aircraft.Fuselage.Dbf.STRINGER_THICKNESS] = (0.375, 'inch')
        self.dbf.options[Aircraft.Fuselage.Dbf.BULKHEAD_MATERIALS] = bulkhead_materials
        self.dbf.options[Aircraft.Fuselage.Dbf.BULKHEAD_THICKNESS] = (rib_thicks, 'inch')
        self.dbf.options[Aircraft.Fuselage.Dbf.BULKHEAD_LIGHTENING_FACTOR] = 0.18
        self.dbf.options[Aircraft.Fuselage.Dbf.NUM_SPARS] = 0.5
        self.dbf.options[Aircraft.Fuselage.Dbf.SPAR_OUTER_DIAMETER] = (1,'inch')
        self.dbf.options[Aircraft.Fuselage.Dbf.SPAR_WALL_THICKNESS] = (0.0625, 'inch')
        self.dbf.options[Aircraft.Fuselage.Dbf.SPAR_DENSITY] = (2.0, 'g/cm**3')
        self.dbf.options[Aircraft.Fuselage.Dbf.SKIN_DENSITY] = (20.0, 'g/m**3')
        self.dbf.options[Aircraft.Fuselage.Dbf.GLUE_FACTOR] = 0.08
        self.dbf.options[Aircraft.Fuselage.Dbf.STRINGER_DENSITY] = (160, 'kg/m**3')
        self.dbf.options[Aircraft.Fuselage.Dbf.SHEETING_THICKNESS] = (0.03125, 'inch')
        self.dbf.options[Aircraft.Fuselage.Dbf.SHEETING_DENSITY] = (160.0, 'kg/m**3')
        self.dbf.options[Aircraft.Fuselage.Dbf.SHEETING_COVERAGE] = 1.0
        self.dbf.options[Aircraft.Fuselage.Dbf.SHEETING_LIGHTENING_FACTOR] = 0.3
        self.dbf.options[Aircraft.Fuselage.Dbf.FLOOR_LENGTH] = (2.0, 'ft')
        self.dbf.options[Aircraft.Fuselage.Dbf.FLOOR_DENSITY] = (340.0, 'kg/m**3')
        self.dbf.options[Aircraft.Fuselage.Dbf.FLOOR_THICKNESS] = (0.125, 'inch')
        self.dbf.options[Aircraft.Fuselage.Dbf.MISC_MASS] = (0.0, 'kg')

        self.prob.setup(force_alloc_complex=True)

        #inputs
        self.prob.set_val(Aircraft.Fuselage.LENGTH, 4.0, units='ft')
        self.prob.set_val(Aircraft.Fuselage.AVG_HEIGHT, 5.0, units='inch')
        self.prob.set_val(Aircraft.Fuselage.AVG_WIDTH, 4.0, units='inch')
        self.prob.set_val(Aircraft.Fuselage.WETTED_AREA, 0.583, units='m**2')

    def test_mass_output(self):
        self.prob.run_model()

        actual_mass = self.prob.get_val(Aircraft.Fuselage.MASS, units='kg')
        print('Computed Mass:', actual_mass)

        expected_mass = 0.40501486
        tol = 1e-6

        assert_near_equal(actual_mass, expected_mass, tolerance=tol)

    def test_partials(self):
        self.prob.run_model()
        partials_data = self.prob.check_partials(compact_print=True, method='cs')
        assert_check_partials(partials_data, atol=1e-6, rtol=1e-6)


if __name__ == '__main__':
    unittest.main()