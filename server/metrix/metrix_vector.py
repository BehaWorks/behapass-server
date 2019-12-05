from server.metrix.result import Result


class MetrixVector:
    VECTOR_LENGTH = 31

    def __init__(self, velocity: Result, acceleration: Result, jerk: Result, angular_velocity: Result,
                 device_distance: Result, session_id, user_id) -> None:
        self.data = {
            "user_id": user_id,
            "session_id": session_id,
            "velocity_average": velocity.average,
            "velocity_median": velocity.median,
            "velocity_minimum": velocity.minimum,
            "velocity_maximum": velocity.maximum,
            "velocity_std_dev": velocity.std_dev,
            "velocity_iqr": velocity.upper_q - velocity.lower_q,
            "acceleration_average": acceleration.average,
            "acceleration_median": acceleration.median,
            "acceleration_minimum": acceleration.minimum,
            "acceleration_maximum": acceleration.maximum,
            "acceleration_std_dev": acceleration.std_dev,
            "acceleration_iqr": acceleration.upper_q - acceleration.lower_q,
            "jerk_average": jerk.average,
            "jerk_median": jerk.median,
            "jerk_minimum": jerk.minimum,
            "jerk_maximum": jerk.maximum,
            "jerk_std_dev": jerk.std_dev,
            "jerk_iqr": jerk.upper_q - jerk.lower_q,
            "angular_velocity_average": angular_velocity.average,
            "angular_velocity_median": angular_velocity.median,
            "angular_velocity_minimum": angular_velocity.minimum,
            "angular_velocity_maximum": angular_velocity.maximum,
            "angular_velocity_std_dev": angular_velocity.std_dev,
            "angular_velocity_iqr": angular_velocity.upper_q - angular_velocity.lower_q,
            "device_distance_average": device_distance.average,
            "device_distance_median": device_distance.median,
            "device_distance_minimum": device_distance.minimum,
            "device_distance_maximum": device_distance.maximum,
            "device_distance_std_dev": device_distance.std_dev,
            "device_distance_iqr": device_distance.upper_q - device_distance.lower_q
        }
        pass

    def to_dict(self):
        return self.data
