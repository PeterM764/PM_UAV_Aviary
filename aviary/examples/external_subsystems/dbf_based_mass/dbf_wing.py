import numpy as np
import os

import openmdao.api as om
from openmdao.utils.cs_safe import abs as cs_abs
import jax.numpy as jnp

from openmdao.utils.units import convert_units
from aviary.examples.external_subsystems.dbf_based_mass.materials_database import materials
from aviary.utils.utils import wrapped_convert_units
from aviary.variable_info.functions import add_aviary_input, add_aviary_output, add_aviary_option

from aviary.examples.external_subsystems.dbf_based_mass.dbf_variable_info.dbf_mass_variables import Aircraft
from aviary.examples.external_subsystems.dbf_based_mass.dbf_variable_info.dbf_mass_variable_metadata import (
    ExtendedMetaData,
)

class DBFWingMass(om.JaxExplicitComponent):
    def initialize(self):
        self.options.declare(Aircraft.Wing.Dbf.AIRFOIL_PATH, types=str, allow_none=False)
        self.options.declare(Aircraft.Wing.Dbf.RIB_MATERIALS, types=(list,))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.NUM_SPARS, 'unitless'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.SPAR_OUTER_DIAMETER, 'm'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.SPAR_DENSITY, 'kg/m**3'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.SPAR_WALL_THICKNESS, 'm'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.RIB_THICKNESS, 'm'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.RIB_LIGHTENING_FACTOR, 'unitless'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.SKIN_DENSITY, 'kg/m**2'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.GLUE_FACTOR, 'unitless'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.STRINGER_DENSITY, 'kg/m**3'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.STRINGER_THICKNESS, 'm'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.SHEETING_THICKNESS, 'm'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.SHEETING_DENSITY, 'kg/m**3'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.SHEETING_COVERAGE, 'unitless'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.SHEETING_LIGHTENING_FACTOR, 'unitless'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.NUM_STRINGERS, 'unitless'))
        self.options.declare(**make_units_option(Aircraft.Wing.Dbf.MISC_MASS, 'kg'))
        self._airfoil_loaded = False

    def setup(self):
        add_aviary_input(self, Aircraft.Wing.SPAN, units='m', meta_data=ExtendedMetaData, primal_name='span')
        add_aviary_input(self, Aircraft.Wing.ROOT_CHORD, units='m', meta_data=ExtendedMetaData, primal_name='root_chord')
        add_aviary_input(self, Aircraft.Wing.WETTED_AREA, units='m**2', meta_data=ExtendedMetaData, primal_name='wetted_area')

        add_aviary_output(self, Aircraft.Wing.MASS, units='kg', meta_data=ExtendedMetaData, primal_name='mass')
    
    def compute_primal(self, span, root_chord, wetted_area):
        self._load_airfoil_if_needed()
        chord = root_chord
        num_spars = self.options[Aircraft.Wing.Dbf.NUM_SPARS]
        rib_lightening_factor = self.options[Aircraft.Wing.Dbf.RIB_LIGHTENING_FACTOR]
        rib_thickness = jnp.atleast_1d(self.options[Aircraft.Wing.Dbf.RIB_THICKNESS]).reshape(-1)
        rho_skin = self.options[Aircraft.Wing.Dbf.SKIN_DENSITY]
        spar_outer_diameter = self.options[Aircraft.Wing.Dbf.SPAR_OUTER_DIAMETER]
        rho_spar = self.options[Aircraft.Wing.Dbf.SPAR_DENSITY]
        spar_wall_thickness = self.options[Aircraft.Wing.Dbf.SPAR_WALL_THICKNESS]
        glue_factor = self.options[Aircraft.Wing.Dbf.GLUE_FACTOR]
        stringer_thickness = self.options[Aircraft.Wing.Dbf.STRINGER_THICKNESS]
        rho_stringer = self.options[Aircraft.Wing.Dbf.STRINGER_DENSITY]
        sheeting_thickness = self.options[Aircraft.Wing.Dbf.SHEETING_THICKNESS]
        sheeting_coverage = self.options[Aircraft.Wing.Dbf.SHEETING_COVERAGE]
        rho_sheeting = self.options[Aircraft.Wing.Dbf.SHEETING_DENSITY]
        sheeting_lightening_factor = self.options[Aircraft.Wing.Dbf.SHEETING_LIGHTENING_FACTOR]
        num_stringer = self.options[Aircraft.Wing.Dbf.NUM_STRINGERS]
        misc_mass = self.options[Aircraft.Wing.Dbf.MISC_MASS]

        cs_area = self.n_area * (chord**2) * rib_lightening_factor
        rho_rib = self.rho_rib.reshape(-1)

        rib_volumes = cs_area * rib_thickness
        spar_volume = (
            num_spars
            * span
            * jnp.pi
            * (spar_outer_diameter * spar_wall_thickness - spar_wall_thickness**2)
        )
        sheeting_volume = (
            wetted_area * sheeting_coverage * sheeting_lightening_factor * sheeting_thickness
        )
        stringer_volume = stringer_thickness**2 * num_stringer * span

        rib_mass = jnp.sum(rib_volumes * rho_rib)
        sheeting_mass = sheeting_volume * rho_sheeting
        stringer_mass = stringer_volume * rho_stringer
        spar_mass = spar_volume * rho_spar
        skin_mass = rho_skin * wetted_area

        structural_mass = stringer_mass + sheeting_mass + rib_mass + spar_mass + skin_mass
        total_mass = (1 + glue_factor) * structural_mass + misc_mass

        return total_mass
    
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
    
    def set_option(self, key, val=None, units=None):
        """
        Store the option value in SI units.
        """
        if units is not None:
            val = self._convert(val, units)

        self.options[key] = val

    def load_airfoil_csv(self, file_path, delimiter=',', header=False):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Airfoil CSV file '{file_path}' not found.")

        skip = 1 if header else 0
        data = np.loadtxt(file_path, delimiter=delimiter, skiprows=skip)

        if data.shape[1] < 2:
            raise ValueError('CSV must contain at least two columns for x and y coordinates.')

        x = data[:, 0]
        y = data[:, 1]

        x_min = np.min(x)
        x_max = np.max(x)
        chord_length = x_max - x_min

        if chord_length <= 0:
            raise ValueError('Invalid airfoil: chord length must be > 0.')

        x_normalized = (x - x_min) / chord_length
        y_normalized = y / chord_length

        return np.array(x_normalized), np.array(y_normalized)
    
    def _load_airfoil_if_needed(self):

        if getattr(self, "_airfoil_loaded", False):
            return

        path = self.options[Aircraft.Wing.Dbf.AIRFOIL_PATH]
        path = os.path.abspath(path)

        x, y = self.load_airfoil_csv(path, header=True)
        self.n_area = 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

        rib_materials = self.options[Aircraft.Wing.Dbf.RIB_MATERIALS]
        self.rho_rib = np.array([materials.get_item(m)[0] for m in rib_materials])

        rib_thickness = self.options[Aircraft.Wing.Dbf.RIB_THICKNESS]
        if len(rib_materials) != len(rib_thickness):
            raise ValueError("Mismatch in rib materials/thicknesses")

        self._airfoil_loaded = True
        
def make_units_option(var_key, units=None, default_val=None, desc=None, meta_data=ExtendedMetaData):
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

    return {
        'name': var_key,
        'default': default_val,
        'set_function': set_func,
        'desc': desc,
    }