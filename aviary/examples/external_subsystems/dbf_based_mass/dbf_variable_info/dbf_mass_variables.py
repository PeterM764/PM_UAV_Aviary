from aviary.variable_info.variables import Aircraft as av_Aircraft

"""
This is an extension of the variable hierarchy that adds variables for dbf aircraft mass calculations.
"""

AviaryAircraft = av_Aircraft

class Aircraft(AviaryAircraft):

    class Fuselage(AviaryAircraft.Fuselage):
        AVG_HEIGHT = 'aircraft:fuselage:average_height'
        AVG_WIDTH = 'aircraft:fuselage:average_width'

        class Dbf:
            BULKHEAD_DENSITY = 'aircraft:fuselage:dbf:bulkhead_density'
            BULKHEAD_LIGHTENING_FACTOR = 'aircraft:fuselage:dbf:bulkhead_lightening_factor'
            BULKHEAD_MATERIALS = 'aircraft:fuselage:dbf:bulkhead_materials'
            BULKHEAD_THICKNESS = 'aircraft:fuselage:dbf:bulkhead_thickness'
            FLOOR_DENSITY = 'aircraft:fuselage:dbf:floor_density'
            FLOOR_LENGTH = 'aircraft:fuselage:dbf:floor_length'
            FLOOR_THICKNESS = 'aircraft:fuselage:dbf:floor_thickness'
            GLUE_FACTOR = 'aircraft:fuselage:dbf:glue_factor'
            MISC_MASS = 'aircraft:fuselage:dbf:misc_mass'
            NUM_BULKHEADS = 'aircraft:fuselage:dbf:number_of_bulkheads'
            NUM_SPARS = 'aircraft:fuselage:dbf:number_of_spars'
            SHEETING_COVERAGE = 'aircraft:fuselage:dbf:sheeting_coverage'
            SHEETING_DENSITY = 'aircraft:fuselage:dbf:sheeting_density'
            SHEETING_LIGHTENING_FACTOR = 'aircraft:fuselage:dbf:sheeting_lightening_factor'
            SHEETING_THICKNESS = 'aircraft:fuselage:dbf:sheeting_thickness'
            SKIN_DENSITY = 'aircraft:fuselage:dbf:skin_density'
            SPAR_DENSITY = 'aircraft:fuselage:dbf:spar_density'
            SPAR_OUTER_DIAMETER = 'aircraft:fuselage:dbf:spar_outer_diameter'
            SPAR_WALL_THICKNESS = 'aircraft:fuselage:dbf:spar_wall_thickness'
            STRINGER_DENSITY = 'aircraft:fuselage:dbf:stringer_density'
            STRINGER_THICKNESS = 'aircraft:fuselage:dbf:stringer_thickness'

    class HorizontalTail(AviaryAircraft.HorizontalTail):

        class Dbf:
            AIRFOIL_PATH = 'aircraft:horizontal_tail:dbf:airfoil_path'
            GLUE_FACTOR = 'aircraft:horizontal_tail:dbf:glue_factor'
            MISC_MASS = 'aircraft:horizontal_tail:dbf:misc_mass'
            NUM_RIBS = 'aircraft:horizontal_tail:dbf:number_of_ribs'
            NUM_SPARS = 'aircraft:horizontal_tail:dbf:number_of_spars'
            NUM_STRINGERS = 'aircraft:horizontal_tail:dbf:number_of_stringers'
            RIB_DENSITY = 'aircraft:horizontal_tail:dbf:rib_density'
            RIB_LIGHTENING_FACTOR = 'aircraft:horizontal_tail:dbf:rib_lightening_factor'
            RIB_MATERIALS = 'aircraft:horizontal_tail:dbf:rib_materials'
            RIB_THICKNESS = 'aircraft:horizontal_tail:dbf:rib_thickness'
            SHEETING_COVERAGE = 'aircraft:horizontal_tail:dbf:sheeting_coverage'
            SHEETING_DENSITY = 'aircraft:horizontal_tail:dbf:sheeting_density'
            SHEETING_LIGHTENING_FACTOR = 'aircraft:horizontal_tail:dbf:sheeting_lightening_factor'
            SHEETING_THICKNESS = 'aircraft:horizontal_tail:dbf:sheeting_thickness'
            SKIN_DENSITY = 'aircraft:horizontal_tail:dbf:skin_density'
            SPAR_DENSITY = 'aircraft:horizontal_tail:dbf:spar_density'
            SPAR_OUTER_DIAMETER = 'aircraft:horizontal_tail:dbf:spar_outer_diameter'
            SPAR_WALL_THICKNESS = 'aircraft:horizontal_tail:dbf:spar_wall_thickness'
            STRINGER_DENSITY = 'aircraft:horizontal_tail:dbf:stringer_density'
            STRINGER_THICKNESS = 'aircraft:horizontal_tail:dbf:stringer_thickness'

    class VerticalTail(AviaryAircraft.VerticalTail):

        class Dbf:
            AIRFOIL_PATH = 'aircraft:vertical_tail:dbf:airfoil_path'
            GLUE_FACTOR = 'aircraft:vertical_tail:dbf:glue_factor'
            MISC_MASS = 'aircraft:vertical_tail:dbf:misc_mass'
            NUM_RIBS = 'aircraft:vertical_tail:dbf:number_of_ribs'
            NUM_SPARS = 'aircraft:vertical_tail:dbf:number_of_spars'
            NUM_STRINGERS = 'aircraft:vertical_tail:dbf:number_of_stringers'
            RIB_DENSITY = 'aircraft:vertical_tail:dbf:rib_density'
            RIB_LIGHTENING_FACTOR = 'aircraft:vertical_tail:dbf:rib_lightening_factor'
            RIB_MATERIALS = 'aircraft:vertical_tail:dbf:rib_materials'
            RIB_THICKNESS = 'aircraft:vertical_tail:dbf:rib_thickness'
            SHEETING_COVERAGE = 'aircraft:vertical_tail:dbf:sheeting_coverage'
            SHEETING_DENSITY = 'aircraft:vertical_tail:dbf:sheeting_density'
            SHEETING_LIGHTENING_FACTOR = 'aircraft:vertical_tail:dbf:sheeting_lightening_factor'
            SHEETING_THICKNESS = 'aircraft:vertical_tail:dbf:sheeting_thickness'
            SKIN_DENSITY = 'aircraft:vertical_tail:dbf:skin_density'
            SPAR_DENSITY = 'aircraft:vertical_tail:dbf:spar_density'
            SPAR_OUTER_DIAMETER = 'aircraft:vertical_tail:dbf:spar_outer_diameter'
            SPAR_WALL_THICKNESS = 'aircraft:vertical_tail:dbf:spar_wall_thickness'
            STRINGER_DENSITY = 'aircraft:vertical_tail:dbf:stringer_density'
            STRINGER_THICKNESS = 'aircraft:vertical_tail:dbf:stringer_thickness'

    class Wing(AviaryAircraft.Wing):

        class Dbf:
            AIRFOIL_PATH = 'aircraft:wing:dbf:airfoil_path'
            GLUE_FACTOR = 'aircraft:wing:dbf:glue_factor'
            MISC_MASS = 'aircraft:wing:dbf:misc_mass'
            NUM_RIBS = 'aircraft:wing:dbf:number_of_ribs'
            NUM_SPARS = 'aircraft:wing:dbf:number_of_spars'
            NUM_STRINGERS = 'aircraft:wing:dbf:number_of_stringers'
            RIB_DENSITY = 'aircraft:wing:dbf:rib_density'
            RIB_LIGHTENING_FACTOR = 'aircraft:wing:dbf:rib_lightening_factor'
            RIB_MATERIALS = 'aircraft:wing:dbf:rib_materials'
            RIB_THICKNESS = 'aircraft:wing:dbf:rib_thickness'
            SHEETING_COVERAGE = 'aircraft:wing:dbf:sheeting_coverage'
            SHEETING_DENSITY = 'aircraft:wing:dbf:sheeting_density'
            SHEETING_LIGHTENING_FACTOR = 'aircraft:wing:dbf:sheeting_lightening_factor'
            SHEETING_THICKNESS = 'aircraft:wing:dbf:sheeting_thickness'
            SKIN_DENSITY = 'aircraft:wing:dbf:skin_density'
            SPAR_DENSITY = 'aircraft:wing:dbf:spar_density'
            SPAR_OUTER_DIAMETER = 'aircraft:wing:dbf:spar_outer_diameter'
            SPAR_WALL_THICKNESS = 'aircraft:wing:dbf:spar_wall_thickness'
            STRINGER_DENSITY = 'aircraft:wing:dbf:stringer_density'
            STRINGER_THICKNESS = 'aircraft:wing:dbf:stringer_thickness'