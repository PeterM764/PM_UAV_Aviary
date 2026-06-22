import numpy as np
import openmdao.api as om

from openmdao.utils.units import convert_units
from aviary.examples.external_subsystems.dbf_based_mass.materials_database import materials
from aviary.utils.utils import wrapped_convert_units
from aviary.variable_info.functions import add_aviary_input, add_aviary_output
from aviary.variable_info.variables import Aircraft
from aviary.variable_info.variable_meta_data import _MetaData

def make_units_option(var_key, units=None, default_val=None, desc=None, meta_data=_MetaData):
    meta = meta_data[var_key]
    default_units = meta['units']

    if units is None:
        units = default_units
    if desc is None:
        desc = meta['desc']
    if default_val is None:
        default_val = meta['default_value']

    # Capture units locally so it's always available
    def set_func(meta_unused, val):
        # val might be tuple or raw value
        if isinstance(val, tuple):
            return wrapped_convert_units(val, units)
        else:
            return wrapped_convert_units((val, units), units)

    return {'name': var_key, 'default': default_val, 'set_function': set_func, 'desc': desc,}
    
class DBFFuselageMass(om.ExplicitComponent):
    def initialize(self):
        self.options.declare(Aircraft.Fuselage.Dbf.BULKHEAD_MATERIALS, types=(list,))

        # Declare options using Aircraft.Fuselage.Dbf metadata keys
        # Note: These may need to be adjusted based on actual metadata keys available
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.NUM_SPARS, 'unitless'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.SPAR_OUTER_DIAMETER, 'm'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.SPAR_DENSITY, 'kg/m**3'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.SPAR_WALL_THICKNESS, 'm'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.BULKHEAD_THICKNESS, 'm'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.BULKHEAD_LIGHTENING_FACTOR, 'unitless'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.SKIN_DENSITY, 'kg/m**2'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.FLOOR_DENSITY, 'kg/m**3'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.FLOOR_THICKNESS, 'm'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.FLOOR_LENGTH, 'm'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.GLUE_FACTOR, 'unitless'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.STRINGER_DENSITY, 'kg/m**3'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.STRINGER_THICKNESS, 'm'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.SHEETING_THICKNESS, 'm'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.SHEETING_DENSITY, 'kg/m**3'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.SHEETING_COVERAGE, 'unitless'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.SHEETING_LIGHTENING_FACTOR, 'unitless'))
        self.options.declare(**make_units_option(Aircraft.Fuselage.Dbf.MISC_MASS, 'kg'))
    
    def _convert(self, val, units):
        """
        Convert a value with units into SI units.
        """
        if units is None:
            return val

        si_units = {
            'inch': 'm',
            'in': 'm',
            'ft': 'm',
            'g/cm**3': 'kg/m**3',
            'g/m**2': 'kg/m**2',
            'unitless': None,
        }

        target = si_units.get(units, units)

        if target is None:
            return val

        return convert_units(val, units, target)

    def setup(self):
        # Required geometry inputs
        add_aviary_input(self, Aircraft.Fuselage.LENGTH, units='m')
        add_aviary_input(self, Aircraft.Fuselage.AVG_HEIGHT, units='m')
        add_aviary_input(self, Aircraft.Fuselage.WETTED_AREA, units='m**2')
        add_aviary_input(self, Aircraft.Fuselage.AVG_WIDTH, units='m')

        add_aviary_output(self, Aircraft.Fuselage.MASS, units='kg',)

    def setup_partials(self):
        self.declare_partials(
            of=Aircraft.Fuselage.MASS,
            wrt=[
                Aircraft.Fuselage.LENGTH,
                Aircraft.Fuselage.AVG_HEIGHT,
                Aircraft.Fuselage.WETTED_AREA,
                Aircraft.Fuselage.AVG_WIDTH,
            ],
        )

    def set_option(self, key, val=None, units=None):
        """
        Store the option value in SI units.
        """
        if units is not None:
            val = self._convert(val, units)

        self.options[key] = val

    def compute(self, inputs, outputs):
        # Inputs
        length = inputs[Aircraft.Fuselage.LENGTH]
        height = inputs[Aircraft.Fuselage.AVG_HEIGHT]
        width = inputs[Aircraft.Fuselage.AVG_WIDTH]
        wetted_area = inputs[Aircraft.Fuselage.WETTED_AREA]

        # From options
        num_spars = self.options[Aircraft.Fuselage.Dbf.NUM_SPARS]
        spar_outer_diameter = self.options[Aircraft.Fuselage.Dbf.SPAR_OUTER_DIAMETER]
        rho_spar = self.options[Aircraft.Fuselage.Dbf.SPAR_DENSITY]
        spar_wall_thickness = self.options[Aircraft.Fuselage.Dbf.SPAR_WALL_THICKNESS]
        bulkhead_thickness = self.options[Aircraft.Fuselage.Dbf.BULKHEAD_THICKNESS]
        bulkhead_lightening_factor = self.options[Aircraft.Fuselage.Dbf.BULKHEAD_LIGHTENING_FACTOR]
        rho_skin = self.options[Aircraft.Fuselage.Dbf.SKIN_DENSITY]
        rho_floor = self.options[Aircraft.Fuselage.Dbf.FLOOR_DENSITY]
        floor_thickness = self.options[Aircraft.Fuselage.Dbf.FLOOR_THICKNESS]
        floor_length = self.options[Aircraft.Fuselage.Dbf.FLOOR_LENGTH]
        glue_factor = self.options[Aircraft.Fuselage.Dbf.GLUE_FACTOR]
        stringer_thickness = self.options[Aircraft.Fuselage.Dbf.STRINGER_THICKNESS]
        rho_stringer = self.options[Aircraft.Fuselage.Dbf.STRINGER_DENSITY]
        sheeting_thick = self.options[Aircraft.Fuselage.Dbf.SHEETING_THICKNESS]
        sheeting_coverage = self.options[Aircraft.Fuselage.Dbf.SHEETING_COVERAGE]
        rho_sheeting = self.options[Aircraft.Fuselage.Dbf.SHEETING_DENSITY]
        sheeting_lightening_factor = self.options[Aircraft.Fuselage.Dbf.SHEETING_LIGHTENING_FACTOR]
        bulkhead_materials = self.options[Aircraft.Fuselage.Dbf.BULKHEAD_MATERIALS]
        misc_mass = self.options[Aircraft.Fuselage.Dbf.MISC_MASS]

        rho_rib = np.array([(materials.get_item(m)[0]) for m in bulkhead_materials])
        cs_area = width * height * bulkhead_lightening_factor
        rib_volumes = cs_area * bulkhead_thickness
        rib_mass = np.sum(rib_volumes * rho_rib)

        # Spar volume
        spar_volume = (num_spars * length * np.pi 
                    * (spar_outer_diameter * spar_wall_thickness - spar_wall_thickness**2))

        # Other volumes
        sheeting_volume = (
            wetted_area * sheeting_coverage * sheeting_lightening_factor * sheeting_thick
        )
        stringer_volume = 4 * stringer_thickness**2 * (length + width + height)

        # Mass calculations
        sheeting_mass = sheeting_volume * rho_sheeting
        stringer_mass = stringer_volume * rho_stringer
        spar_mass = spar_volume * rho_spar
        skin_mass = rho_skin * wetted_area
        floor_mass = rho_floor * floor_length * width * floor_thickness

        # Total structural mass
        structural_mass = (
            rib_mass + spar_mass + floor_mass + stringer_mass + sheeting_mass + skin_mass
        )

        total_mass = structural_mass * (1 + glue_factor) + misc_mass

        outputs[Aircraft.Fuselage.MASS] = total_mass
        
    def compute_partials(self, inputs, J):
        # Inputs
        height = inputs[Aircraft.Fuselage.AVG_HEIGHT]
        width = inputs[Aircraft.Fuselage.AVG_WIDTH]

        # From options
        num_spars = self.options[Aircraft.Fuselage.Dbf.NUM_SPARS]
        spar_outer_diameter = self.options[Aircraft.Fuselage.Dbf.SPAR_OUTER_DIAMETER]
        rho_spar = self.options[Aircraft.Fuselage.Dbf.SPAR_DENSITY]
        spar_wall_thickness = self.options[Aircraft.Fuselage.Dbf.SPAR_WALL_THICKNESS]
        bulkhead_thickness = self.options[Aircraft.Fuselage.Dbf.BULKHEAD_THICKNESS]
        bulkhead_lightening_factor = self.options[Aircraft.Fuselage.Dbf.BULKHEAD_LIGHTENING_FACTOR]
        rho_skin = self.options[Aircraft.Fuselage.Dbf.SKIN_DENSITY]
        rho_floor = self.options[Aircraft.Fuselage.Dbf.FLOOR_DENSITY]
        floor_thickness = self.options[Aircraft.Fuselage.Dbf.FLOOR_THICKNESS]
        floor_length = self.options[Aircraft.Fuselage.Dbf.FLOOR_LENGTH]
        glue_factor = self.options[Aircraft.Fuselage.Dbf.GLUE_FACTOR]
        stringer_thickness = self.options[Aircraft.Fuselage.Dbf.STRINGER_THICKNESS]
        rho_stringer = self.options[Aircraft.Fuselage.Dbf.STRINGER_DENSITY]
        sheeting_thick = self.options[Aircraft.Fuselage.Dbf.SHEETING_THICKNESS]
        sheeting_coverage = self.options[Aircraft.Fuselage.Dbf.SHEETING_COVERAGE]
        rho_sheeting = self.options[Aircraft.Fuselage.Dbf.SHEETING_DENSITY]
        sheeting_lightening_factor = self.options[Aircraft.Fuselage.Dbf.SHEETING_LIGHTENING_FACTOR]
        bulkhead_materials = self.options[Aircraft.Fuselage.Dbf.BULKHEAD_MATERIALS]

        rho_rib = np.array([(materials.get_item(m)[0]) for m in bulkhead_materials])

        J[Aircraft.Fuselage.MASS, Aircraft.Fuselage.AVG_HEIGHT] = (
            4 * stringer_thickness**2 * rho_stringer
            + width * bulkhead_lightening_factor * np.sum(rho_rib * bulkhead_thickness)
        ) * (1 + glue_factor)

        J[Aircraft.Fuselage.MASS, Aircraft.Fuselage.AVG_WIDTH] = (
            4 * stringer_thickness**2 * rho_stringer
            + floor_length * floor_thickness * rho_floor
            + height * bulkhead_lightening_factor * np.sum(rho_rib * bulkhead_thickness)
        ) * (1 + glue_factor)

        J[Aircraft.Fuselage.MASS, Aircraft.Fuselage.LENGTH] = (
            num_spars
            * np.pi
            * (spar_outer_diameter * spar_wall_thickness - spar_wall_thickness**2)
            * rho_spar
            + 4 * stringer_thickness**2 * rho_stringer
        ) * (1 + glue_factor)

        J[Aircraft.Fuselage.MASS, Aircraft.Fuselage.WETTED_AREA] = (
            rho_skin
            + sheeting_coverage * sheeting_lightening_factor * sheeting_thick * rho_sheeting
        ) * (1 + glue_factor)