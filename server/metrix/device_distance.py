from . import Metric, Result


class DeviceDistance(Metric):
    def calculate(self, movements: list) -> Result:
        hmd_points = self.extract_device_points(movements, "LHR-BE784403")
        controller_points = self.extract_device_points(movements, "LHR-FDEB3942")
        device_distances = self.distances_between_points(hmd_points, controller_points)
        return Result(device_distances)
