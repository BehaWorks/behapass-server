import numpy as np
import vg
from pyquaternion import Quaternion

from server.metrix.result import Result


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
    def extract_timestamps(movements):
        timestamps = [np.array(movement.timestamp) for movement in movements]
        return timestamps

    @staticmethod
    def extract_trigger_pressures(buttons):
        pressures = [np.array(button.trigger) for button in buttons]
        return pressures

    @staticmethod
    def extract_euler_angles(movements):
        angles = [np.array([movement.yaw, movement.pitch, movement.roll]) * np.pi / 180. for movement in movements]
        return angles

    @staticmethod
    def to_quaternion(angle):  # yaw (Z), pitch (Y), roll (X)
        cy = np.cos(angle[0] * 0.5)
        sy = np.sin(angle[0] * 0.5)
        cp = np.cos(angle[1] * 0.5)
        sp = np.sin(angle[1] * 0.5)
        cr = np.cos(angle[2] * 0.5)
        sr = np.sin(angle[2] * 0.5)

        this_quaternion = Quaternion(w=cy * cp * cr + sy * sp * sr,
                                     x=cy * cp * sr - sy * sp * cr,
                                     y=sy * cp * sr + cy * sp * cr,
                                     z=sy * cp * cr - cy * sp * sr)
        return this_quaternion

    @staticmethod
    def euler_angles_to_quaternions(euler_angles):
        quaternions = [Metric.to_quaternion(euler_angle) for euler_angle in euler_angles]
        return quaternions

    @staticmethod
    def calculate_quaternions_distances(quaternions):
        quaternions_distance = []
        try:
            actual_quaternion = quaternions.pop(0)
        except IndexError:
            return []
        for next_quaternion in quaternions:
            quaternions_distance.append(Quaternion.distance(actual_quaternion, next_quaternion))
            actual_quaternion = next_quaternion
        return quaternions_distance

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
