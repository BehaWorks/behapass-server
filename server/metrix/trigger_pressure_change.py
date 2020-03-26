from server.metrix.metric import Metric
from server.metrix.result import Result
from server.models.movement import CONTROLLER_1


class TriggerPressureChange(Metric):
    def calculate(self, buttons: list) -> Result:
        controller_trigger_pressures = self.extract_trigger_pressures(buttons, CONTROLLER_1)
        device_distances = self.distances_between_points(hmd_points, controller_points)
        return Result(device_distances)
