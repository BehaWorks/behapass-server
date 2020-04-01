from server.metrix.metric import Metric
from server.metrix.result import Result


class TriggerPressureChange(Metric):
    def calculate(self, buttons: list) -> Result:
        controller_trigger_pressures = self.extract_trigger_pressures(buttons)
        controller_trigger_pressure_differences = self.differences_between_pressures(controller_trigger_pressures)
        return Result(controller_trigger_pressure_differences)
