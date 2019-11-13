import numpy as np

from .velocity import Velocity


class Acceleration(Velocity):

    def calculate(self, data: list) -> float:
        coordinates, timestamps = self.extract_coordinates_timestamps(data)
        velocities = self.derivate_wrt_time(coordinates, timestamps)
        accelerations = self.derivate_wrt_time(velocities, timestamps)
        velocity = np.average(accelerations)
        return velocity
