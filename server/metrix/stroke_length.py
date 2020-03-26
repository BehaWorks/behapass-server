from server.metrix.metric import Metric
from server.metrix.result import Result


class StrokeLength(Metric):
    def calculate(self, movements: list) -> Result:
        points, timestamps = self.extract_points_timestamps(movements)
        distances = self.calculate_distance(self.distance, points)
        suma = [sum(distances)]*10

        return Result(suma)
