import numpy as np

from . import Metric, Result


class Velocity(Metric):
    def calculate(self, data: list) -> Result:
        coordinates, timestamps = self.extract_coordinates_timestamps(data)
        speeds = self.derivate_wrt_time(coordinates, timestamps)
        velocity = Result(speeds)
        return velocity

    def extract_coordinates_timestamps(self, movements):
        coordinates = [np.array([movement['x'], movement['y'], movement['z']]) for movement in movements]
        timestamps = [np.array(movement['timestamp']) for movement in movements]
        return coordinates, timestamps

    def derivate_wrt_time(self, coordinates, timestamps):
        derivatives = []
        coordinates1 = coordinates.pop(0)
        timestamp1 = timestamps.pop(0)
        for coordinates2, timestamp2 in zip(coordinates, timestamps):
            time_dif = timestamp2 - timestamp1
            derivatives.append(self.distance(coordinates2, coordinates1) / time_dif)
            timestamp1 = timestamp2
            coordinates1 = coordinates2
        return derivatives

    def distance(self, a, b):
        a = np.array(a)
        b = np.array(b)
        dif = a - b
        squared = dif ** 2
        try:
            return np.sqrt(sum(squared))
        except TypeError:
            return np.sqrt(squared)
