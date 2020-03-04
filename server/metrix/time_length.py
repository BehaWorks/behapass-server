from server.metrix.metric import Metric
from server.metrix.result import Result


class TimeLength(Metric):
    def calculate(self, movements: list) -> Result:
        timestamps = self.extract_timestamps(movements)
        time_length = timestamps[-1]
        return Result(time_length)
