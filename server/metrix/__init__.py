from server.metrix.acceleration import Acceleration
from server.metrix.angular_velocity import AngularVelocity
from server.metrix.controller_rotation_distance import ControllerRotationDistance
from server.metrix.device_distance import DeviceDistance
from server.metrix.jerk import Jerk
from server.metrix.metrix_vector import MetrixVector
from server.metrix.time_length import TimeLength
from server.metrix.velocity import Velocity

__all__ = ["acceleration", "angular_velocity", "device_distance", "jerk", "velocity", "controller_rotation_distance",
           "time_length", "create_metrix_vector"]


def create_metrix_vector(controller_data, headset_data) -> MetrixVector:
    velocity_result = Velocity().calculate(controller_data)
    acceleration_result = Acceleration().calculate(controller_data)
    jerk_result = Jerk().calculate(controller_data)
    angular_velocity_result = AngularVelocity().calculate(controller_data)
    device_distance_result = DeviceDistance().calculate(controller_data + headset_data)
    controller_rotation_distance_result = ControllerRotationDistance().calculate(controller_data)
    time_length_result = TimeLength().calculate(controller_data)
    return MetrixVector(velocity_result, acceleration_result, jerk_result, angular_velocity_result,
                        device_distance_result, controller_rotation_distance_result, time_length_result,
                        controller_data[0].session_id, controller_data[0].user_id)
