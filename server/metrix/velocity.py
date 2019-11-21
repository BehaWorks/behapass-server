from . import Metric, Result


class Velocity(Metric):
    def calculate(self, movements: list) -> Result:
        velocities = self.extract_velocities_timestamps(movements)[0]
        return Result(velocities)

    def extract_velocities_timestamps(self, movements):
        points, timestamps = self.extract_points_timestamps(movements)
        velocities = self.derivative_wrt_time(self.distance, points, timestamps)
        return velocities, timestamps
