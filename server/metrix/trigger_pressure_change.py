from server.metrix.metric import Metric
from server.metrix.result import Result


class TriggerPressureChange(Metric):
    def calculate(self, buttons: list) -> Result:
        timestamps = self.extract_timestamps(buttons)
        controller_trigger_pressures = self.extract_trigger_pressures(buttons)

        controller_trigger_pressure_difference_velocity = self.derivative_wrt_time(lambda a, b: a - b,
                                                                                   controller_trigger_pressures,
                                                                                   timestamps)
        return Result(controller_trigger_pressure_difference_velocity)
