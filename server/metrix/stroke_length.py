from server.metrix.metric import Metric
from server.metrix.result import Result


class StrokeLength(Metric):
    def calculate(self, movements: list) -> Result:
        points, timestamps = self.extract_points_timestamps(movements)

        length = list(map(Metric.distance, points[1:], points[:-1]))
        suma = [sum(length)]*len(length)

        return Result(suma)
