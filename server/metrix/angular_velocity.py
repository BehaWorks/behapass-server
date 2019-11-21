from . import Metric, Result


class AngularVelocity(Metric):
    def calculate(self, movements) -> Result:
        points, timestamps = self.extract_points_timestamps(movements)
        angular_velocities = self.derivative_wrt_time(self.angle, points, timestamps)
        return Result(angular_velocities)
