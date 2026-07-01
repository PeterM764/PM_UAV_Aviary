from aviary.examples.external_subsystems.dbf_based_mass.dbf_variable_info.dbf_mass_variables import Aircraft
from aviary.subsystems.subsystem_builder import SubsystemBuilder
from aviary.examples.external_subsystems.dbf_based_mass.dbf_mass_premission import MassPremission

class DBFMassBuilder(SubsystemBuilder):
    
    """
    Builder for DBF mass models (wing, htail, vtail, fuselage, ...)
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
    def __init__(self, name='dbf_mass'):
        if name is None:
            name = _default_name

        super().__init__(name=name)

    def build_pre_mission(self, aviary_inputs, subsystem_options=None, **kwargs):
        group = om.Group()

        # Add mass subsystems first, promote outputs to group
        group.add_subsystem(
            'wing_mass',
            DBFWingMass(),
            promotes_inputs=['aircraft:*'],
            promotes_outputs=[Aircraft.Wing.MASS],
        )

        group.add_subsystem(
            'horizontal_tail_mass',
            DBFHorizontalTailMass(),
            promotes_inputs=['aircraft:*'],
            promotes_outputs=[Aircraft.HorizontalTail.MASS],
        )

        group.add_subsystem(
            'vertical_tail_mass',
            DBFVerticalTailMass(),
            promotes_inputs=['aircraft:*'],
            promotes_outputs=[Aircraft.VerticalTail.MASS],
        )

        group.add_subsystem(
            'fuselage_mass',
            DBFFuselageMass(),
            promotes_inputs=['aircraft:*'],
            promotes_outputs=[Aircraft.Fuselage.MASS],
        )

        group.add_subsystem(
            'total_mass',
            om.ExecComp(
                'engine_mass = n_batt * batt_mass + n_mot * motor_mass',
                batt_mass={'val': 0.0, 'units': 'kg'},
                motor_mass={'val': 0.0, 'units': 'kg'},
                engine_mass={'val': 0.0, 'units': 'kg'},
                n_mot={'val': 1.0},
                n_batt={'val': 1.0} #TODO Alex change
            ),
            promotes_inputs=[('batt_mass', Aircraft.Battery.MASS), ('motor_mass', Aircraft.Engine.Motor.MASS), ('n_mot', 'aircraft:engine:num_engines')],
            promotes_outputs=[('engine_mass', Aircraft.Propulsion.MASS)]
        )

        return group

