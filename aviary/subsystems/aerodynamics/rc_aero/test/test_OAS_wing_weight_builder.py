import importlib.util
import unittest

import aviary.api as av
from PM_UAV_Aviary.aviary.subsystems.aerodynamics.rc_aero.OAS_Weight.OAS_wing_weight_builder import OASWingWeightBuilder
path_to_builder = 'OAS_weight.OAS_wing_weight_builder.OASWingWeightBuilder'

class TestOASWingWeightBuilder(av.TestSubsystemBuilder):
    def setup(self):
        self.subsystem_builder = OASWingWeightBuilder()
        self.aviary_values = av.AviaryValues()

if __name__ == '__main__':
    unittest.main()