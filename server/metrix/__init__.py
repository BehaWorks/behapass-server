from server.metrix.acceleration import Acceleration
from server.metrix.angular_velocity import AngularVelocity
from server.metrix.device_distance import DeviceDistance
from server.metrix.jerk import Jerk
from server.metrix.metrix_vector import MetrixVector
from server.metrix.velocity import Velocity

__all__ = ["acceleration", "angular_velocity", "device_distance", "jerk", "magnitude", "velocity"]

def create_Metrix_Vector(controller_data, headset_data) -> MetrixVector:
    velocity_result = Velocity().calculate(controller_data)
    acceleration_result = Acceleration().calculate(controller_data)
    jerk_result = Jerk().calculate(controller_data)
    angular_velocity_result = AngularVelocity().calculate(controller_data)
    device_distance_result = DeviceDistance().calculate(controller_data + headset_data)
    return MetrixVector(velocity_result, acceleration_result, jerk_result, angular_velocity_result,
                        device_distance_result, controller_data[0].session_id, controller_data[0].user_id)
