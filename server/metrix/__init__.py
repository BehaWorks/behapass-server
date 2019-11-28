import numpy as np
import vg


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
        return np.linalg.norm(a - b)

    @staticmethod
    def angle(a, b):
        return vg.angle(a, b)
