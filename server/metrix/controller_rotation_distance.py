from server.metrix.metric import Metric
from server.metrix.result import Result


class ControllerRotationDistance(Metric):
    def calculate(self, movements: list) -> Result:
        euler_angles = self.extract_euler_angles(movements)
        quaternions = self.euler_angles_to_quaternions(euler_angles)
        quaternions_distances = self.calculate_quaternions_distances(quaternions)
        return Result(quaternions_distances)
