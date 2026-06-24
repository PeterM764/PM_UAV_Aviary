from aviary.examples.external_subsystems.dbf_based_mass.variable_info.dbf_mass_variables import Aircraft
from aviary.subsystems.subsystem_builder import SubsystemBuilder
from aviary.examples.external_subsystems.dbf_based_mass.dbf_mass_premission import MassPremission

class DBFMassBuilder(SubsystemBuilder):
    
    """
    Builder for DBF mass models including wing, horizontal tail,
    vertical tail, and fuselage.
    """

    def build_pre_mission(self, aviary_inputs, subsystem_options=None):
        subsystem_options = subsystem_options or {}

        return MassPremission(
            aviary_inputs = aviary_inputs,
            subsystem_options = subsystem_options,
        )

    def get_inputs(self):
        return [
            Aircraft.Wing.SPAN,
            Aircraft.Wing.ROOT_CHORD,
            Aircraft.Wing.WETTED_AREA,
            Aircraft.Fuselage.LENGTH,
            Aircraft.Fuselage.AVG_HEIGHT,
            Aircraft.Fuselage.AVG_WIDTH,
            Aircraft.Fuselage.WETTED_AREA,
            Aircraft.HorizontalTail.SPAN,
            Aircraft.HorizontalTail.ROOT_CHORD,
            Aircraft.HorizontalTail.WETTED_AREA,
            Aircraft.VerticalTail.SPAN,
            Aircraft.VerticalTail.ROOT_CHORD,
            Aircraft.VerticalTail.WETTED_AREA,
        ]

    def get_outputs(self):
        return [
            Aircraft.Wing.MASS,
            Aircraft.HorizontalTail.MASS,
            Aircraft.VerticalTail.MASS,
            Aircraft.Fuselage.MASS,
            Aircraft.Design.STRUCTURE_MASS,
        ]