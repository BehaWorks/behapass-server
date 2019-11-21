import numpy as np

from . import Metric, Result


class Magnitude(Metric):
    def calculate(self, movements: list) -> Result:
        points = self.extract_points_timestamps(movements)[0]
        magnitudes = []
        for point in points:
            magnitude = np.linalg.norm(point)
            magnitudes.append(magnitude)
        return Result(magnitudes)
