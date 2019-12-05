from server.metrix.result import Result
from .acceleration import Acceleration


class Jerk(Acceleration):
    def calculate(self, movements: list) -> Result:
        accelerations, timestamps = self.extract_accelerations_timestamps(movements)
        jerks = self.derivative_wrt_time(self.distance, accelerations, timestamps)
        return Result(jerks)
