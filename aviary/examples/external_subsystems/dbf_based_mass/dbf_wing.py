#This tests the mass pre-mission file with the simple wing design
import numpy as np
import os

import openmdao.api as om
import jax.numpy as jnp

from aviary.examples.external_subsystems.dbf_based_mass.option_info.materials_database import materials
from aviary.variable_info.functions import add_aviary_input, add_aviary_output, add_aviary_option
from aviary.examples.external_subsystems.dbf_based_mass.utils.load_airfoil import load_airfoil_if_needed

from aviary.examples.external_subsystems.dbf_based_mass.dbf_variable_info.dbf_mass_variables import Aircraft
from aviary.examples.external_subsystems.dbf_based_mass.dbf_variable_info.dbf_mass_variable_metadata import (
    ExtendedMetaData,
)

class DBFWingMass(om.JaxExplicitComponent):
    def initialize(self):
        #simple wing options
        add_aviary_option(self, Aircraft.Wing.Dbf.TYPE, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.FOAM_DENSITY, units='kg/m**3', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.ROD_DENSITY, units='kg/m**3', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.ROD_RADIUS, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.ROD_THICKNESS, units='m', meta_data=ExtendedMetaData)

        #medium wing options
        add_aviary_option(self, Aircraft.Wing.Dbf.AIRFOIL_PATH, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.RIB_MATERIALS, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.NUM_SPARS, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.SPAR_OUTER_DIAMETER, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.SPAR_DENSITY, units='kg/m**3', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.SPAR_WALL_THICKNESS, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.RIB_THICKNESS, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.RIB_LIGHTENING_FACTOR, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.SKIN_DENSITY, units='kg/m**3', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.GLUE_FACTOR, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.STRINGER_DENSITY, units='kg/m**3', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.STRINGER_THICKNESS, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.SHEETING_THICKNESS, units='m', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.SHEETING_DENSITY, units='kg/m**3', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.SHEETING_COVERAGE, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.SHEETING_LIGHTENING_FACTOR, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.NUM_STRINGERS, units='unitless', meta_data=ExtendedMetaData)
        add_aviary_option(self, Aircraft.Wing.Dbf.MISC_MASS, units='kg', meta_data=ExtendedMetaData)

        self._airfoil_loaded = False

    def setup(self):
        add_aviary_input(self, Aircraft.Wing.SPAN, units='m', meta_data=ExtendedMetaData, primal_name='span')
        add_aviary_input(self, Aircraft.Wing.ROOT_CHORD, units='m', meta_data=ExtendedMetaData, primal_name='root_chord')
        add_aviary_input(self, Aircraft.Wing.WETTED_AREA, units='m**2', meta_data=ExtendedMetaData, primal_name='wetted_area')

        add_aviary_output(self, Aircraft.Wing.MASS, units='kg', meta_data=ExtendedMetaData, primal_name='mass')
    
    def compute_primal(self, span, root_chord, wetted_area):
        load_airfoil_if_needed(self, Aircraft.Wing.Dbf)
        chord = root_chord
        type = self.options[Aircraft.Wing.Dbf.TYPE]

        if type == 'simple':

            #Simple wing design mass calculation
            rod_thickness, units = self.options[Aircraft.Wing.Dbf.ROD_THICKNESS]
            foam_density, units = self.options[Aircraft.Wing.Dbf.FOAM_DENSITY]
            radius, units = self.options[Aircraft.Wing.Dbf.ROD_RADIUS]
            rod_density, units = self.options[Aircraft.Wing.Dbf.ROD_DENSITY]

            airfoil_area = self.n_area * chord**2            
            foam_volume = airfoil_area * span
            foam_mass_prelim = foam_volume * foam_density
            cross_section_rod_area = jnp.pi * radius**2 - jnp.pi * (radius - rod_thickness)**2
            
            #Assumes fixed number of 2 rods in the simple wing design:
            rod_volume = (2.0 * span * cross_section_rod_area)

            foam_mass_final = foam_mass_prelim - 2 * foam_density * rod_volume
            rod_mass = 2 * rod_volume * rod_density

            total_mass = foam_mass_final + rod_mass

            return total_mass
        
        if type == 'medium':

            #medium wing design mass calculation
            num_spars = self.options[Aircraft.Wing.Dbf.NUM_SPARS]
            rib_lightening_factor = self.options[Aircraft.Wing.Dbf.RIB_LIGHTENING_FACTOR]
            rib_thickness, units = self.options[Aircraft.Wing.Dbf.RIB_THICKNESS]
            rho_skin, units = self.options[Aircraft.Wing.Dbf.SKIN_DENSITY]
            spar_outer_diameter, units = self.options[Aircraft.Wing.Dbf.SPAR_OUTER_DIAMETER]
            rho_spar, units = self.options[Aircraft.Wing.Dbf.SPAR_DENSITY]
            spar_wall_thickness, units = self.options[Aircraft.Wing.Dbf.SPAR_WALL_THICKNESS]
            glue_factor = self.options[Aircraft.Wing.Dbf.GLUE_FACTOR]
            stringer_thickness, units = self.options[Aircraft.Wing.Dbf.STRINGER_THICKNESS]
            rho_stringer, units = self.options[Aircraft.Wing.Dbf.STRINGER_DENSITY]
            sheeting_thickness, units = self.options[Aircraft.Wing.Dbf.SHEETING_THICKNESS]
            sheeting_coverage = self.options[Aircraft.Wing.Dbf.SHEETING_COVERAGE]
            rho_sheeting, units = self.options[Aircraft.Wing.Dbf.SHEETING_DENSITY]
            sheeting_lightening_factor = self.options[Aircraft.Wing.Dbf.SHEETING_LIGHTENING_FACTOR]
            num_stringer = self.options[Aircraft.Wing.Dbf.NUM_STRINGERS]
            #This is used to calculate rho_rib in other components but done differently here
            #rib_materials = self.options[Aircraft.Wing.Dbf.RIB_MATERIALS]
            misc_mass, units = self.options[Aircraft.Wing.Dbf.MISC_MASS]

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
        
        #raise error if invalid option is given
        else:
            raise ValueError("Invalid wing TYPE option: must be 'simple' or 'medium'")