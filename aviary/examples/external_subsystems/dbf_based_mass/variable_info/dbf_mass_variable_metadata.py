"""
Metadata for DBF variables defined in dbf_mass_variables.py
"""
from copy import deepcopy

import aviary.api as av
from aviary.examples.external_subsystems.dbf_based_mass.variable_info.dbf_mass_variables import Aircraft

ExtendedMetaData = deepcopy(av.CoreMetaData)

# ================================================================================================================================================================
# .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.
# | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
# | |      __      | || |     _____    | || |  _______     | || |     ______   | || |  _______     | || |      __      | || |  _________   | || |  _________   | |
# | |     /  \     | || |    |_   _|   | || | |_   __ \    | || |   .' ___  |  | || | |_   __ \    | || |     /  \     | || | |_   ___  |  | || | |  _   _  |  | |
# | |    / /\ \    | || |      | |     | || |   | |__) |   | || |  / .'   \_|  | || |   | |__) |   | || |    / /\ \    | || |   | |_  \_|  | || | |_/ | | \_|  | |
# | |   / ____ \   | || |      | |     | || |   |  __ /    | || |  | |         | || |   |  __ /    | || |   / ____ \   | || |   |  _|      | || |     | |      | |
# | | _/ /    \ \_ | || |     _| |_    | || |  _| |  \ \_  | || |  \ `.___.'\  | || |  _| |  \ \_  | || | _/ /    \ \_ | || |  _| |_       | || |    _| |_     | |
# | ||____|  |____|| || |    |_____|   | || | |____| |___| | || |   `._____.'  | || | |____| |___| | || ||____|  |____|| || | |_____|      | || |   |_____|    | |
# | |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | |
# | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
#  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'
# ================================================================================================================================================================

#  ______                        _
# |  ____|                      | |
# | |__     _   _   ___    ___  | |   __ _    __ _    ___
# |  __|   | | | | / __|  / _ \ | |  / _` |  / _` |  / _ \
# | |      | |_| | \__ \ |  __/ | | | (_| | | (_| | |  __/
# |_|       \__,_| |___/  \___| |_|  \__,_|  \__, |  \___|
#                                             __/ |
#                                            |___/
# ========================================================

av.add_meta_data(
    Aircraft.Fuselage.AVG_HEIGHT,
    units='inch',
    desc='Height of fuselage (assumed rectangular prism shape)',
    default_value=12,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.AVG_WIDTH,
    units='inch',
    desc='Width of fuselage (assumed rectangular prism shape)',
    default_value=12,
    meta_data = ExtendedMetaData,
    option=True,
)

#   ___    _       __ 
#  |   \  | |__   / _|
#  | |) | | '_ \ |  _|
#  |___/  |_.__/ |_|  
# ====================

av.add_meta_data(
    Aircraft.Fuselage.Dbf.BULKHEAD_DENSITY,
    units='lbm/ft**3',
    types=float,
    desc='Material density of the rib',
    default_value=[0.0],
    meta_data = ExtendedMetaData,
    multivalue=True,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.BULKHEAD_LIGHTENING_FACTOR,
    units='unitless',
    desc='Fraction of the rib area that remains after lightening cuts',
    default_value=0.5,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.BULKHEAD_MATERIALS,
    units='unitless',
    types=str,
    desc='Material density of the bulkhead',
    default_value=[''],
    meta_data = ExtendedMetaData,
    multivalue=True,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.BULKHEAD_THICKNESS,
    units='inch',
    types=float,
    desc='Thickness of a single rib',
    default_value=[0.0],
    meta_data = ExtendedMetaData,
    multivalue=True,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.FLOOR_DENSITY,
    units='lbm/inch**3',
    desc='Density of fuselage floor',
    default_value=0.02,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.FLOOR_LENGTH,
    units='ft',
    desc='length of fuselage floor',
    default_value=2.0,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.FLOOR_THICKNESS,
    units='inch',
    desc='Thickness of fuselage floor',
    default_value=0.0125,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.GLUE_FACTOR,
    units='unitless',
    desc='Added margin for glue. Only added to ribs, spars, and stringers',
    default_value=0.15,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.MISC_MASS,
    units='kg',
    desc='Mass made up of smaller, non structural components. Can be used for higher fidelity options as well',
    default_value=0.0,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.NUM_BULKHEADS,
    units='unitless',
    desc='Number of fuselage ribs',
    default_value=10,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.NUM_SPARS,
    units='unitless',
    desc='Number of fuselage spars',
    default_value=2,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.SHEETING_COVERAGE,
    units='unitless',
    desc='Fraction of the wetted area covered by sheeting',
    default_value=1.0,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.SHEETING_DENSITY,
    units='lbm/ft**3',
    desc='Material density of the sheeting',
    default_value=250,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.SHEETING_LIGHTENING_FACTOR,
    units='unitless',
    desc='Fraction of the sheeting area that remains after lightening cuts',
    default_value=0.5,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.SHEETING_THICKNESS,
    units='inch',
    desc='Thickness of sheeting',
    default_value=0.03125,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.SKIN_DENSITY,
    units='lbm/inch**2',
    desc='Surface density of fuselage skin',
    default_value=0.02,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.SPAR_DENSITY,
    units='lbm/ft**3',
    desc='Material density of the spar',
    default_value=0.015,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.SPAR_OUTER_DIAMETER,
    units='inch',
    desc='Diameter/thickness of a single spar (assumed cylindrical)',
    default_value=0.25,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.SPAR_WALL_THICKNESS,
    units='inch',
    desc='Thickness of spar wall',
    default_value=0.0625,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.STRINGER_DENSITY,
    units='lbm/ft**3',
    desc='Material density of the stringer',
    default_value=250,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Fuselage.Dbf.STRINGER_THICKNESS,
    units='inch',
    desc='Thickness of stringers',
    default_value=0.0625,
    meta_data = ExtendedMetaData,
    option=True,
)

#  _    _                  _                         _             _   _______           _   _
# | |  | |                (_)                       | |           | | |__   __|         (_) | |
# | |__| |   ___    _ __   _   ____   ___    _ __   | |_    __ _  | |    | |      __ _   _  | |
# |  __  |  / _ \  | '__| | | |_  /  / _ \  | '_ \  | __|  / _` | | |    | |     / _` | | | | |
# | |  | | | (_) | | |    | |  / /  | (_) | | | | | | |_  | (_| | | |    | |    | (_| | | | | |
# |_|  |_|  \___/  |_|    |_| /___|  \___/  |_| |_|  \__|  \__,_| |_|    |_|     \__,_| |_| |_|
# =============================================================================================

#   ___    _       __ 
#  |   \  | |__   / _|
#  | |) | | '_ \ |  _|
#  |___/  |_.__/ |_|  
# ====================

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.AIRFOIL_PATH,
    units='unitless',
    types=str,
    desc='Path to csv file containing airfoil data',
    default_value='',
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.GLUE_FACTOR,
    units='unitless',
    desc='Added margin for glue. Only added to ribs, spars, and stringers',
    default_value=0.15,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.MISC_MASS,
    units='kg',
    desc='Mass made up of smaller, non structural components. Can be used for higher fidelity options as well',
    default_value=0.0,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.NUM_RIBS,
    units='unitless',
    desc='Number of wing ribs',
    default_value=10,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.NUM_SPARS,
    units='unitless',
    desc='Number of wing spars',
    default_value=2,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.NUM_STRINGERS,
    units='unitless',
    desc='Number of stringers(assumed length=span)',
    default_value=2.0,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.RIB_DENSITY,
    units='lbm/ft**3',
    types=float,
    desc='Material density of the rib',
    default_value=[0.0],
    meta_data = ExtendedMetaData,
    multivalue=True,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.RIB_LIGHTENING_FACTOR,
    units='unitless',
    desc='Fraction of the rib area that remains after lightening cuts',
    default_value=0.5,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.RIB_MATERIALS,
    units='unitless',
    types=str,
    desc='Material of the rib',
    default_value=[''],
    meta_data = ExtendedMetaData,
    multivalue=True,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.RIB_THICKNESS,
    units='inch',
    types=float,
    desc='Thickness of a single rib',
    default_value=[0.0],
    meta_data = ExtendedMetaData,
    multivalue=True,
    option=True,
)



av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.SHEETING_COVERAGE,
    units='unitless',
    desc='Fraction of the wetted area covered by sheeting',
    default_value=1.0,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.SHEETING_DENSITY,
    units='lbm/ft**3',
    desc='Material density of the sheeting',
    default_value=250,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.SHEETING_LIGHTENING_FACTOR,
    units='unitless',
    desc='Fraction of the sheeting area that remains after lightening cuts',
    default_value=0.5,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.SHEETING_THICKNESS,
    units='inch',
    desc='Thickness of sheeting',
    default_value=0.03125,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.SKIN_DENSITY,
    units='lbm/inch**2',
    desc='Surface density of wing skin',
    default_value=0.02,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.SPAR_DENSITY,
    units='lbm/ft**3',
    desc='Material density of the spar',
    default_value=0.015,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.SPAR_OUTER_DIAMETER,
    units='inch',
    desc='Diameter/thickness of a single spar (assumed cylindrical)',
    default_value=0.25,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.SPAR_WALL_THICKNESS,
    units='inch',
    desc='Thickness of spar wall',
    default_value=0.0625,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.STRINGER_DENSITY,
    units='lbm/ft**3',
    desc='Material density of the stringer',
    default_value=250,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.HorizontalTail.Dbf.STRINGER_THICKNESS,
    units='inch',
    desc='Thickness of stringers',
    default_value=0.0625,
    meta_data = ExtendedMetaData,
    option=True,
)

# __      __                _     _                  _   _______           _   _
# \ \    / /               | |   (_)                | | |__   __|         (_) | |
#  \ \  / /    ___   _ __  | |_   _    ___    __ _  | |    | |      __ _   _  | |
#   \ \/ /    / _ \ | '__| | __| | |  / __|  / _` | | |    | |     / _` | | | | |
#    \  /    |  __/ | |    | |_  | | | (__  | (_| | | |    | |    | (_| | | | | |
#     \/      \___| |_|     \__| |_|  \___|  \__,_| |_|    |_|     \__,_| |_| |_|
# ===============================================================================

#   ___    _       __ 
#  |   \  | |__   / _|
#  | |) | | '_ \ |  _|
#  |___/  |_.__/ |_|  
# ====================

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.AIRFOIL_PATH,
    units='unitless',
    types=str,
    desc='Path to csv file containing airfoil data',
    default_value='',
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.GLUE_FACTOR,
    units='unitless',
    desc='Added margin for glue. Only added to ribs, spars, and stringers',
    default_value=0.15,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.MISC_MASS,
    units='kg',
    desc='Mass made up of smaller, non structural components. Can be used for higher fidelity options as well',
    default_value=0.0,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.NUM_RIBS,
    units='unitless',
    desc='Number of wing ribs',
    default_value=10,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.NUM_SPARS,
    units='unitless',
    desc='Number of wing spars',
    default_value=2,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.NUM_STRINGERS,
    units='unitless',
    desc='Number of stringers(assumed length=span)',
    default_value=2.0,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.RIB_DENSITY,
    units='lbm/ft**3',
    types=float,
    desc='Material density of the rib',
    default_value=[0.0],
    meta_data = ExtendedMetaData,
    multivalue=True,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.RIB_LIGHTENING_FACTOR,
    units='unitless',
    desc='Fraction of the rib area that remains after lightening cuts',
    default_value=0.5,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.RIB_MATERIALS,
    units='unitless',
    types=str,
    desc='Material of the rib',
    default_value=[''],
    meta_data = ExtendedMetaData,
    multivalue=True,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.RIB_THICKNESS,
    units='inch',
    types=float,
    desc='Thickness of a single rib',
    default_value=[0.0],
    meta_data = ExtendedMetaData,
    multivalue=True,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.SHEETING_COVERAGE,
    units='unitless',
    desc='Fraction of the wetted area covered by sheeting',
    default_value=1.0,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.SHEETING_DENSITY,
    units='lbm/ft**3',
    desc='Material density of the sheeting',
    default_value=250,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.SHEETING_LIGHTENING_FACTOR,
    units='unitless',
    desc='Fraction of the sheeting area that remains after lightening cuts',
    default_value=0.5,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.SHEETING_THICKNESS,
    units='inch',
    desc='Thickness of sheeting',
    default_value=0.03125,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.SKIN_DENSITY,
    units='lbm/inch**2',
    desc='Surface density of wing skin',
    default_value=0.02,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.SPAR_DENSITY,
    units='lbm/ft**3',
    desc='Material density of the spar',
    default_value=0.015,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.SPAR_OUTER_DIAMETER,
    units='inch',
    desc='Diameter/thickness of a single spar (assumed cylindrical)',
    default_value=0.25,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.SPAR_WALL_THICKNESS,
    units='inch',
    desc='Thickness of spar wall',
    default_value=0.0625,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.STRINGER_DENSITY,
    units='lbm/ft**3',
    desc='Material density of the stringer',
    default_value=250,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.VerticalTail.Dbf.STRINGER_THICKNESS,
    units='inch',
    desc='Thickness of stringers',
    default_value=0.0625,
    meta_data = ExtendedMetaData,
    option=True,
)

# __          __  _
# \ \        / / (_)
#  \ \  /\  / /   _   _ __     __ _
#   \ \/  \/ /   | | | '_ \   / _` |
#    \  /\  /    | | | | | | | (_| |
#     \/  \/     |_| |_| |_|  \__, |
#                              __/ |
#                             |___/
# ==================================

#   ___    _       __ 
#  |   \  | |__   / _|
#  | |) | | '_ \ |  _|
#  |___/  |_.__/ |_|  
# ====================

av.add_meta_data(
    Aircraft.Wing.Dbf.AIRFOIL_PATH,
    units='unitless',
    types=str,
    desc='Path to csv file containing airfoil data',
    default_value='',
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.GLUE_FACTOR,
    units='unitless',
    desc='Added margin for glue. Only added to ribs, spars, and stringers',
    default_value=0.15,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.MISC_MASS,
    units='kg',
    desc='Mass made up of smaller, non structural components. Can be used for higher fidelity options as well',
    default_value=0.0,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.NUM_RIBS,
    units='unitless',
    desc='Number of wing ribs',
    default_value=10,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.NUM_SPARS,
    units='unitless',
    desc='Number of wing spars',
    default_value=2,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.NUM_STRINGERS,
    units='unitless',
    desc='Number of stringers(assumed length=span)',
    default_value=2.0,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.RIB_DENSITY,
    units='lbm/ft**3',
    types=float,
    desc='Material density of the rib',
    default_value=[0.0],
    meta_data = ExtendedMetaData,
    multivalue=True,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.RIB_LIGHTENING_FACTOR,
    units='unitless',
    desc='Fraction of the rib area that remains after lightening cuts',
    default_value=0.5,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.RIB_MATERIALS,
    units='unitless',
    types=str,
    desc='Material of the rib',
    default_value=[''],
    meta_data = ExtendedMetaData,
    multivalue=True,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.RIB_THICKNESS,
    units='inch',
    types=float,
    desc='Thickness of a single rib',
    default_value=[0.0],
    meta_data = ExtendedMetaData,
    multivalue=True,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.SHEETING_COVERAGE,
    units='unitless',
    desc='Fraction of the wetted area covered by sheeting',
    default_value=1.0,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.SHEETING_DENSITY,
    units='lbm/ft**3',
    desc='Material density of the sheeting',
    default_value=250,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.SHEETING_LIGHTENING_FACTOR,
    units='unitless',
    desc='Fraction of the sheeting area that remains after lightening cuts',
    default_value=0.5,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.SHEETING_THICKNESS,
    units='inch',
    desc='Thickness of sheeting',
    default_value=0.03125,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.SKIN_DENSITY,
    units='lbm/inch**2',
    desc='Surface density of wing skin',
    default_value=0.02,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.SPAR_DENSITY,
    units='lbm/ft**3',
    desc='Material density of the spar',
    default_value=0.015,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.SPAR_OUTER_DIAMETER,
    units='inch',
    desc='Diameter/thickness of a single spar (assumed cylindrical)',
    default_value=0.25,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.SPAR_WALL_THICKNESS,
    units='inch',
    desc='Thickness of spar wall',
    default_value=0.0625,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.STRINGER_DENSITY,
    units='lbm/ft**3',
    desc='Material density of the stringer',
    default_value=250,
    meta_data = ExtendedMetaData,
    option=True,
)

av.add_meta_data(
    Aircraft.Wing.Dbf.STRINGER_THICKNESS,
    units='inch',
    desc='Thickness of stringers',
    default_value=0.0625,
    meta_data = ExtendedMetaData,
    option=True,
)