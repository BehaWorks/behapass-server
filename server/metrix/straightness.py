from .stroke_length import StrokeLength
from server.metrix.result import Result


class Straightness(StrokeLength):
    def calculate(self, movements: list) -> Result:
        points, timestamps = self.extract_points_timestamps(movements)

        stroke_lenghts = Straightness.partial_lenghts(self, points)
        straight_length = StrokeLength.distance(points[0], points[-1])

        suma = [(straight_length/sum(stroke_lenghts))]*(len(stroke_lenghts))
        return Result(suma)
