from server.metrix.metric import Metric
from server.metrix.result import Result


class TimeLength(Metric):
    def calculate(self, movements: list) -> Result:
        timestamps = self.extract_timestamps(movements)

        try:
            timestamps_unified = [timestamps[-1]] * len(timestamps)
        except IndexError:
            print("CHYBA: dlzka movements = " + str(len(movements)))
            return Result([0] * 10)

        return Result(timestamps_unified)
