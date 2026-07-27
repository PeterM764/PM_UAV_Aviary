import unittest
import aviary.api as av

from aviary.subsystems.aerodynamics.UAV_aero.aero_builder import AeroBuilder
from aviary.variable_info.variables import Aircraft, Dynamic

class TestAeroBuilder(av.TestSubsystemBuilder):
    def setUp(self):
        self.subsystem_builder = AeroBuilder()
        self.aviary_values = av.AviaryValues()
   
        self.aviary_values.set_val(Aircraft.Wing.THICKNESS_TO_CHORD, 0.12, units='unitless')
        self.aviary_values.set_val(Aircraft.Wing.MAX_THICKNESS_LOCATION, 0.3, units='unitless')
        self.aviary_values.set_val(Aircraft.Wing.CENTER_DISTANCE, 1.0, units='unitless')
        self.aviary_values.set_val(Aircraft.Fuselage.LENGTH, 1.0, units='m')
        self.aviary_values.set_val(Aircraft.HorizontalTail.THICKNESS_TO_CHORD, 0.12, units='unitless')
        
if __name__ == '__main__':
    unittest.main()