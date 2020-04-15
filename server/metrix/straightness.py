from server.metrix.result import Result
from .stroke_length import StrokeLength


class Straightness(StrokeLength):
    def calculate(self, movements: list) -> Result:
        points, timestamps = self.extract_points_timestamps(movements)

        stroke_lenghts = Straightness.partial_lenghts(self, points)

        try:
            straight_length = StrokeLength.distance(points[0], points[-1])
        except IndexError:
            print("CHYBA")
            return Result([0] * 10)

        suma = [(straight_length/sum(stroke_lenghts))]*(len(stroke_lenghts))
        return Result(suma)
