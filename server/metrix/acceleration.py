from server.metrix import Result
from .velocity import Velocity


class Acceleration(Velocity):
    def calculate(self, movements: list) -> Result:
        accelerations = self.extract_accelerations_timestamps(movements)[0]
        return Result(accelerations)

    def extract_accelerations_timestamps(self, movements):
        velocities, timestamps = self.extract_velocities_timestamps(movements)
        accelerations = self.derivative_wrt_time(self.distance, velocities, timestamps)
        return accelerations, timestamps
