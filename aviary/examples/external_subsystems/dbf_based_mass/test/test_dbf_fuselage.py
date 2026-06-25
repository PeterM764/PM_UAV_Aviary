import unittest
import numpy as np
import openmdao.api as om

from aviary.examples.external_subsystems.dbf_based_mass.dbf_fuselage import DBFFuselageMass
from openmdao.utils.assert_utils import assert_near_equal, assert_check_partials
from aviary.examples.external_subsystems.dbf_based_mass.dbf_variable_info.dbf_mass_variables import Aircraft

class TestDBFFuselageMass(unittest.TestCase):
    def setUp(self):
        self.prob = om.Problem()
        self.dbf = DBFFuselageMass()

        self.prob.model.add_subsystem(
            'dbf_fuselage', self.dbf, promotes_inputs=['*'], promotes_outputs=['*']
        )

        #Define the rib layout
        ribs = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2])
        bulkhead_materials = np.where(ribs != 0, 'Ply', 'Balsa').tolist()
        rib_thicks = np.where(ribs == 2, 0.25, 0.125)

        # Using Aircraft.Fuselage.Dbf.* keys instead of string names
        self.dbf.options[Aircraft.Fuselage.Dbf.BULKHEAD_MATERIALS] = bulkhead_materials
        self.dbf.set_option(Aircraft.Fuselage.Dbf.BULKHEAD_THICKNESS, val=rib_thicks, units='inch')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.NUM_SPARS, val = 0.5, units='unitless')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.BULKHEAD_LIGHTENING_FACTOR, val=0.18, units='unitless')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.SHEETING_COVERAGE, val=1, units='unitless')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.SHEETING_DENSITY, val=160, units='kg/m**3')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.SHEETING_LIGHTENING_FACTOR, val=0.3, units='unitless')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.SHEETING_THICKNESS, val=0.03125, units='inch')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.GLUE_FACTOR, val=0.08, units='unitless')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.STRINGER_DENSITY, val=160, units='kg/m**3')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.STRINGER_THICKNESS, val=0.375, units='inch')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.FLOOR_LENGTH, val=2, units='ft')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.FLOOR_DENSITY, val=340, units='kg/m**3')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.FLOOR_THICKNESS, val=0.125, units='inch')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.SKIN_DENSITY, val=20, units='g/m**2')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.SPAR_DENSITY, val = 2, units='g/cm**3')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.SPAR_OUTER_DIAMETER, val=1, units='inch')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.SPAR_WALL_THICKNESS, val=0.0625, units='inch')
        self.dbf.set_option(Aircraft.Fuselage.Dbf.MISC_MASS, val=0.0, units='kg')

        self.prob.setup(force_alloc_complex=True)

        #inputs
        self.prob.set_val(Aircraft.Fuselage.LENGTH, val=4, units='ft')
        self.prob.set_val(Aircraft.Fuselage.AVG_HEIGHT, val=5, units='inch')
        self.prob.set_val(Aircraft.Fuselage.AVG_WIDTH, val=4, units='inch')
        self.prob.set_val(Aircraft.Fuselage.WETTED_AREA, val=904, units='inch**2')
        
    def test_mass_output(self):
        self.prob.run_model()

        actual_mass = self.prob.get_val(Aircraft.Fuselage.MASS, units='kg')
        print('Computed Mass:', actual_mass)

        # Update expected_mass based on verified value
        expected_mass = 0.405
        tol = 1e-3

        assert_near_equal(actual_mass, expected_mass, tolerance=tol)
        print('Fuselage mass: ', expected_mass)
        
    def test_partials(self):
        self.prob.run_model()
        partials_data = self.prob.check_partials(compact_print=True, method='cs')
        assert_check_partials(partials_data, atol=1e-6, rtol=1e-6)

if __name__ == '__main__':
    unittest.main()