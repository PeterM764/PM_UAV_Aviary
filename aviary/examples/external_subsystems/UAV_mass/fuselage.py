import numpy as np
import openmdao.api as om
import jax.numpy as jnp

from PM_UAV_Aviary.aviary.examples.external_subsystems.UAV_mass.utils.materials_database import materials
from aviary.variable_info.functions import add_aviary_input, add_aviary_output, add_aviary_option

from PM_UAV_Aviary.aviary.examples.external_subsystems.UAV_mass.variable_info.mass_variables import Aircraft
from PM_UAV_Aviary.aviary.examples.external_subsystems.UAV_mass.variable_info.mass_variable_metadata import (
    ExtendedMetaData,
)

class DBFFuselageMass(om.JaxExplicitComponent):
    def initialize(self):
        add_aviary_option(self, Aircraft.Fuselage.Dbf.FLOOR_DENSITY, units='kg/m**3', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.NUM_SPARS, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.SPAR_OUTER_DIAMETER, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.SPAR_DENSITY, units='kg/m**3', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.SPAR_WALL_THICKNESS, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.BULKHEAD_THICKNESS, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.BULKHEAD_LIGHTENING_FACTOR, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.SKIN_DENSITY, units='kg/m**3', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.FLOOR_THICKNESS, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.FLOOR_LENGTH, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.GLUE_FACTOR, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.STRINGER_THICKNESS, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.STRINGER_DENSITY, units='kg/m**3', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.SHEETING_THICKNESS, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.SHEETING_COVERAGE, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.SHEETING_DENSITY, units='kg/m**3', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.SHEETING_LIGHTENING_FACTOR, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.BULKHEAD_MATERIALS, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Fuselage.Dbf.MISC_MASS, units='kg', meta_data=ExtendedMetaData)

    def setup(self):
        add_aviary_input(self, Aircraft.Fuselage.LENGTH, units='m', meta_data=ExtendedMetaData, primal_name='length')
        add_aviary_input(self, Aircraft.Fuselage.AVG_HEIGHT, units='m', meta_data=ExtendedMetaData, primal_name='avg_height')
        add_aviary_input(self, Aircraft.Fuselage.WETTED_AREA, units='m**2', meta_data=ExtendedMetaData, primal_name='wetted_area')
        add_aviary_input(self, Aircraft.Fuselage.AVG_WIDTH, units='m', meta_data=ExtendedMetaData, primal_name='avg_width')

        add_aviary_output(self, Aircraft.Fuselage.MASS, units='kg', meta_data=ExtendedMetaData, primal_name='mass')

    def compute_primal(self, length, avg_height, wetted_area, avg_width):
        rho_floor, units = self.options[Aircraft.Fuselage.Dbf.FLOOR_DENSITY]
        num_spars = self.options[Aircraft.Fuselage.Dbf.NUM_SPARS]
        spar_outer_diameter, units = self.options[Aircraft.Fuselage.Dbf.SPAR_OUTER_DIAMETER]
        rho_spar, units = self.options[Aircraft.Fuselage.Dbf.SPAR_DENSITY]
        spar_wall_thickness, units = self.options[Aircraft.Fuselage.Dbf.SPAR_WALL_THICKNESS]
        bulkhead_thickness, units = self.options[Aircraft.Fuselage.Dbf.BULKHEAD_THICKNESS]
        bulkhead_lightening_factor = self.options[Aircraft.Fuselage.Dbf.BULKHEAD_LIGHTENING_FACTOR]
        rho_skin, units = self.options[Aircraft.Fuselage.Dbf.SKIN_DENSITY]
        floor_thickness, units = self.options[Aircraft.Fuselage.Dbf.FLOOR_THICKNESS]
        floor_length, units = self.options[Aircraft.Fuselage.Dbf.FLOOR_LENGTH]
        glue_factor = self.options[Aircraft.Fuselage.Dbf.GLUE_FACTOR]
        stringer_thickness, units = self.options[Aircraft.Fuselage.Dbf.STRINGER_THICKNESS]
        rho_stringer, units = self.options[Aircraft.Fuselage.Dbf.STRINGER_DENSITY]
        sheeting_thick, units = self.options[Aircraft.Fuselage.Dbf.SHEETING_THICKNESS]
        sheeting_coverage = self.options[Aircraft.Fuselage.Dbf.SHEETING_COVERAGE]
        rho_sheeting, units = self.options[Aircraft.Fuselage.Dbf.SHEETING_DENSITY]
        sheeting_lightening_factor = self.options[Aircraft.Fuselage.Dbf.SHEETING_LIGHTENING_FACTOR]
        bulkhead_materials = self.options[Aircraft.Fuselage.Dbf.BULKHEAD_MATERIALS]
        misc_mass, units = self.options[Aircraft.Fuselage.Dbf.MISC_MASS]

        rho_rib = jnp.array([(materials.get_item(m)[0]) for m in bulkhead_materials])
        cs_area = avg_width * avg_height * bulkhead_lightening_factor
        rib_volumes = cs_area * bulkhead_thickness
        rib_mass = jnp.sum(rib_volumes * rho_rib)

        # Spar volume
        spar_volume = (num_spars * length * jnp.pi 
                    * (spar_outer_diameter * spar_wall_thickness - spar_wall_thickness**2))

        # Other volumes
        sheeting_volume = (
            wetted_area * sheeting_coverage * sheeting_lightening_factor * sheeting_thick
        )
        stringer_volume = 4 * stringer_thickness**2 * (length + avg_width + avg_height)

        # Mass calculations
        sheeting_mass = sheeting_volume * rho_sheeting
        stringer_mass = stringer_volume * rho_stringer
        spar_mass = spar_volume * rho_spar
        skin_mass = rho_skin * wetted_area
        floor_mass = rho_floor * floor_length * avg_width * floor_thickness

        # Total structural mass
        structural_mass = (
            rib_mass + spar_mass + floor_mass + stringer_mass + sheeting_mass + skin_mass
        )

        total_mass = structural_mass * (1 + glue_factor) + misc_mass

        return total_mass