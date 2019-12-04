from server.models.movement import HEADSET, CONTROLLER_1, CONTROLLER_2
from . import Metric, Result


class DeviceDistance(Metric):
    def calculate(self, movements: list) -> Result:
        hmd_points = self.extract_device_points(movements, HEADSET)
        controller_points = self.extract_device_points(movements, CONTROLLER_1)
        device_distances = self.distances_between_points(hmd_points, controller_points)
        return Result(device_distances)
