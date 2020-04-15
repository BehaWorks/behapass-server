from server.metrix.acceleration import Acceleration
from server.metrix.angular_velocity import AngularVelocity
from server.metrix.controller_rotation_distance import ControllerRotationDistance
from server.metrix.device_distance import DeviceDistance
from server.metrix.jerk import Jerk
from server.metrix.metrix_vector import MetrixVector
from server.metrix.straightness import Straightness
from server.metrix.stroke_length import StrokeLength
from server.metrix.time_length import TimeLength
from server.metrix.trigger_pressure_change import TriggerPressureChange
from server.metrix.velocity import Velocity

__all__ = ["acceleration", "angular_velocity", "device_distance", "jerk", "velocity", "controller_rotation_distance",
           "time_length", "create_metrix_vector", "trigger_pressure_change",
           "stroke_length", "straightness"]


def create_metrix_vector(controller_movements, headset_movements, controller_buttons) -> MetrixVector:
    velocity_result = Velocity().calculate(controller_movements)
    acceleration_result = Acceleration().calculate(controller_movements)
    jerk_result = Jerk().calculate(controller_movements)
    angular_velocity_result = AngularVelocity().calculate(controller_movements)
    device_distance_result = DeviceDistance().calculate(controller_movements + headset_movements)
    controller_rotation_distance_result = ControllerRotationDistance().calculate(controller_movements)
    time_length_result = TimeLength().calculate(controller_movements)
    trigger_pressure_change_result = TriggerPressureChange().calculate(controller_buttons)
    stroke_length_result = StrokeLength().calculate(controller_movements)
    straightness_result = Straightness().calculate(controller_movements)
    return MetrixVector(velocity=velocity_result, acceleration=acceleration_result, jerk=jerk_result,
                        angular_velocity=angular_velocity_result, device_distance=device_distance_result,
                        controller_rotation_distance=controller_rotation_distance_result,
                        time_length=time_length_result,
                        trigger_pressure_change=trigger_pressure_change_result, stroke_length=stroke_length_result,
                        straightness=straightness_result,
                        session_id=controller_movements[0].session_id, user_id=controller_movements[0].user_id)
