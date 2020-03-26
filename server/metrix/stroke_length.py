from server.metrix.metric import Metric
from server.metrix.result import Result


class StrokeLength(Metric):
    def calculate(self, movements: list) -> Result:
        points, timestamps = self.extract_points_timestamps(movements)
        length = self.calculate_length(self.distance, points)
        suma = [sum(length)]*len(length)

        return Result(suma)
