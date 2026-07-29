import unittest
import aviary.api as av
import openmdao.api as om
import numpy as np

from aviary.subsystems.aerodynamics.UAV_aero.aero_builder import AeroBuilder
from aviary.variable_info.variables import Aircraft, Dynamic, Settings
from aviary.utils.aviary_values import AviaryValues
from aviary.subsystems.aerodynamics.UAV_aero.aero_model import TotalAircraftAero
from aviary.variable_info.functions import setup_model_options

class TestAeroBuilder(av.TestSubsystemBuilder):
    def setUp(self):
        self.subsystem_builder = AeroBuilder()
        self.aviary_values = av.AviaryValues()

        #wing
        self.aviary_values.set_val(Aircraft.Wing.THICKNESS_TO_CHORD, 0.06, units='unitless')
        self.aviary_values.set_val(Aircraft.Wing.MAX_THICKNESS_LOCATION, 0.3, units='unitless')
        self.aviary_values.set_val(Aircraft.Wing.CENTER_DISTANCE, 0.4, units='unitless')
        self.aviary_values.set_val(Aircraft.Wing.SPAN, 1.5, units='ft')
        self.aviary_values.set_val(Aircraft.Wing.ROOT_CHORD, 0.3, units='m')
        self.aviary_values.set_val(Aircraft.Wing.SWEEP, 5.0, units='deg')
        self.aviary_values.set_val(Aircraft.Wing.INCIDENCE, 2.0, units='deg')
        self.aviary_values.set_val(Aircraft.Wing.AREA, 0.45, units='m**2')
        self.aviary_values.set_val(Aircraft.Wing.FUSELAGE_INTERFERENCE_FACTOR, 1.2, units='unitless')

        #Horizontal tail
        self.aviary_values.set_val(Aircraft.HorizontalTail.SPAN, 0.6, units='m')
        self.aviary_values.set_val(Aircraft.HorizontalTail.ROOT_CHORD, 0.2, units='m')
        self.aviary_values.set_val(Aircraft.HorizontalTail.SWEEP, 10.0, units='deg')
        self.aviary_values.set_val(Aircraft.HorizontalTail.THICKNESS_TO_CHORD, 0.06, units='unitless')


        # Vertical tail
        self.aviary_values.set_val(Aircraft.VerticalTail.SPAN, 0.4, units='m')
        self.aviary_values.set_val(Aircraft.VerticalTail.ROOT_CHORD, 0.2, units='m')
        self.aviary_values.set_val(Aircraft.VerticalTail.TAPER_RATIO, 0.6, units='unitless')
        self.aviary_values.set_val(Aircraft.VerticalTail.THICKNESS_TO_CHORD, 0.06, units='unitless')

        # Fuselage
        self.aviary_values.set_val(Aircraft.Fuselage.MAX_HEIGHT, 0.15, units='m')
        self.aviary_values.set_val(Aircraft.Fuselage.MAX_WIDTH, 0.12, units='m')
        self.aviary_values.set_val(Aircraft.Fuselage.LENGTH, 1.0, units='m')


        # Landing gear
        self.aviary_values.set_val(Aircraft.LandingGear.DRAG_COEFFICIENT, 0.02, units='unitless')

# The test below is more effective but currently results in a NaN error

# class TestAeroBuilder_2(unittest.TestCase):
#     def test_aero_results(self):
#         nn = 1
#         av_inputs = AviaryValues()
#         av_inputs.set_val(Settings.VERBOSITY, 0)

#         # Wing
#         av_inputs.set_val(Aircraft.Wing.SPAN, 1.5, units='ft')
#         av_inputs.set_val(Aircraft.Wing.ROOT_CHORD, 0.3, units='m')
#         av_inputs.set_val(Aircraft.Wing.SWEEP, 5.0, units='deg')
#         av_inputs.set_val(Aircraft.Wing.INCIDENCE, 2.0, units='deg')
#         av_inputs.set_val(Aircraft.Wing.AREA, 0.45, units='m**2')
#         av_inputs.set_val(Aircraft.Wing.THICKNESS_TO_CHORD, 0.06, units='unitless')
#         av_inputs.set_val(Aircraft.Wing.MAX_THICKNESS_LOCATION, 0.3, units='unitless')
#         av_inputs.set_val(Aircraft.Wing.CENTER_DISTANCE, 0.4, units='unitless')
#         av_inputs.set_val(Aircraft.Wing.FUSELAGE_INTERFERENCE_FACTOR, 1.2, units='unitless')

#         # Horizontal tail
#         av_inputs.set_val(Aircraft.HorizontalTail.SPAN, 0.6, units='m')
#         av_inputs.set_val(Aircraft.HorizontalTail.ROOT_CHORD, 0.2, units='m')
#         av_inputs.set_val(Aircraft.HorizontalTail.SWEEP, 10.0, units='deg')
#         av_inputs.set_val(Aircraft.HorizontalTail.THICKNESS_TO_CHORD, 0.06, units='unitless')

#         # Vertical tail
#         av_inputs.set_val(Aircraft.VerticalTail.SPAN, 0.4, units='m')
#         av_inputs.set_val(Aircraft.VerticalTail.ROOT_CHORD, 0.2, units='m')
#         av_inputs.set_val(Aircraft.VerticalTail.TAPER_RATIO, 0.6, units='unitless')
#         av_inputs.set_val(Aircraft.VerticalTail.THICKNESS_TO_CHORD, 0.06, units='unitless')

#         # Fuselage
#         av_inputs.set_val(Aircraft.Fuselage.LENGTH, 1.2, units='m')
#         av_inputs.set_val(Aircraft.Fuselage.MAX_HEIGHT, 0.15, units='m')
#         av_inputs.set_val(Aircraft.Fuselage.MAX_WIDTH, 0.12, units='m')

#         #Landing Gear
#         av_inputs.set_val(Aircraft.LandingGear.DRAG_COEFFICIENT, 0.02, units='unitless')
        
#         builder = AeroBuilder()

#         aerogroup = builder.build_mission(num_nodes = nn, aviary_inputs = av_inputs)

#         prob = om.Problem(model = aerogroup)

#         prob.setup(force_alloc_complex = True)

#         prob.set_val(Dynamic.Mission.ALTITUDE, np.ones(nn)*1000.0, units='m')
#         prob.set_val(Dynamic.Mission.VELOCITY, np.ones(nn)*30.0, units='m/s')
#         prob.set_val(Dynamic.Vehicle.MASS, np.ones(nn)*10.0, units='kg')

#         prob.final_setup()
#         prob.model.list_inputs(units=True)
#         prob.model.list_outputs(units=True)

#         prob.run_model()

#         try:
#             prob.run_model()
#         except Exception as e:
#             mtx = prob.get_val('OAS_aero.aero_point_0.aero_states.mtx')
#             print("mtx has NaN:", np.isnan(mtx).any(), "Inf:", np.isinf(mtx).any())
#             print("mtx:", mtx)
#             raise

#         #final values of things:
#         #... = prob.get_val('...', units='...')

if __name__ == '__main__':
    unittest.main()
