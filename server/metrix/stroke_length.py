from server.metrix.metric import Metric
from server.metrix.result import Result


class StrokeLength(Metric):
    def calculate(self, movements: list) -> Result:
        points, timestamps = self.extract_points_timestamps(movements)

        length = self.partial_lenghts(points)
        suma = [sum(length)]*len(length)

        return Result(suma)

    def partial_lenghts(self, points):
        return list(map(Metric.distance, points[1:], points[:-1]))
