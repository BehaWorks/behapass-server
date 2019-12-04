import numpy as np
import vg

from . import *

__all__ = ["acceleration", "angular_velocity", "device_distance", "jerk", "magnitude", "velocity"]


class Result:
    data = None

    def __init__(self, data) -> None:
        self.data = data

    @property
    def average(self):
        return np.average(self.data)

    @property
    def median(self):
        return np.median(self.data)

    @property
    def std_dev(self):
        return np.std(self.data)

    @property
    def upper_q(self):
        return np.quantile(self.data, 0.75)

    @property
    def lower_q(self):
        return np.quantile(self.data, 0.25)

    @property
    def minimum(self):
        return np.min(self.data)

    @property
    def maximum(self):
        return np.max(self.data)

    @property
    def interquartile_range(self):
        return self.upper_q - self.lower_q


class Metric:
    """
    Base class for metrics. Subclass this class for individual metrics.
    """

    def calculate(self, movements) -> Result:
        """
        :type movements: list[Movement]
        :return:
        """
        raise AttributeError('This is a base class. Subclass this class for individual metrics.')

    @staticmethod
    def extract_points_timestamps(movements):
        points = [np.array([movement.x, movement.y, movement.z]) for movement in movements]
        timestamps = [np.array(movement.timestamp) for movement in movements]
        return points, timestamps

    @staticmethod
    def derivative_wrt_time(function, values, timestamps):
        derivatives = []
        try:
            actual_values = values.pop(0)
            actual_timestamp = timestamps.pop(0)
        except IndexError:
            return []
        for next_values, next_timestamp in zip(values, timestamps):
            timestamp_dif = next_timestamp - actual_timestamp
            derivatives.append(function(next_values, actual_values) / timestamp_dif)
            actual_timestamp = next_timestamp
            actual_values = next_values
        return derivatives

    @classmethod
    def extract_device_points(cls, movements, device_id):
        device_movements = [movement for movement in movements if movement.controller_id == device_id]
        return cls.extract_points_timestamps(device_movements)[0]

    @classmethod
    def distances_between_points(cls, points1, points2):
        return [cls.distance(point1, point2) for point1, point2 in zip(points1, points2)]

    @staticmethod
    def distance(a, b):
        a = np.array(a)
        b = np.array(b)
        dif = a - b
        squared = dif ** 2
        try:
            return np.sqrt(sum(squared))
        except TypeError:
            return np.sqrt(squared)

    @staticmethod
    def angle(a, b):
        a = np.array(a)
        b = np.array(b)
        return vg.angle(a, b)


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


def create_Metrix_Vector(controller_data, headset_data) -> MetrixVector:
    velocity_result = velocity.Velocity().calculate(controller_data)
    acceleration_result = acceleration.Acceleration().calculate(controller_data)
    # jerk_result = jerk.Jerk().calculate(controller_data)
    # angular_velocity_result = angular_velocity.AngularVelocity().calculate(controller_data)
    # device_distance_result = device_distance.DeviceDistance().calculate(controller_data + headset_data)
    return MetrixVector(velocity_result, acceleration_result, acceleration_result, velocity_result,
                        acceleration_result, controller_data[0].session_id, controller_data[0].user_id)
