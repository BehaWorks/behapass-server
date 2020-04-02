from server.metrix.metric import Metric
from server.metrix.result import Result


class TimeLength(Metric):
    def calculate(self, movements: list) -> Result:
        timestamps = self.extract_timestamps(movements)

        timestamps_unified = [timestamps[-1]]*len(timestamps)

        return Result(timestamps_unified)
