from . import Metric, Result

class DeviceDistance(Metric):
    def calculate(self, data: list) -> Result:
        controller_coordinates, hmd_coordinates = self.extract_coordinates_of_both_devices(data)
        device_distance = self.calculate_device_distance(self.distance, controller_coordinates, hmd_coordinates)
        device_distance = Result(device_distance)
        return device_distance

