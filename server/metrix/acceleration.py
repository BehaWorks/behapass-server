from server.metrix import Result

from .velocity import Velocity


class Acceleration(Velocity):

    def calculate(self, data: list) -> Result:
        coordinates, timestamps = self.extract_coordinates_timestamps(data)
        velocities = self.derivate_wrt_time(coordinates, timestamps)
        accelerations = self.derivate_wrt_time(velocities, timestamps)
        return Result(accelerations)
