from unittest import TestCase

from server.metrix.acceleration import Acceleration
from server.metrix.velocity import Velocity
from server.models.movement import Movement

movements = [Movement.from_dict({"session_id": "test",
                                 "user_id": "test",
                                 "timestamp": i,
                                 "controller_id": "test",
                                 "x": 2 ** i,
                                 "y": 2 ** i,
                                 "z": 2 ** i,
                                 "yaw": "test",
                                 "pitch": "test",
                                 "roll": "test",
                                 "r_x": "test",
                                 "r_y": "test",
                                 "r_z": "test",
                                 }) for i in range(11)]


class TestMetrix(TestCase):
    inputs = [
        {"instance": Velocity(), "input": movements,
         "output": [1.732050808, 3.464101615, 6.92820323, 13.85640646, 27.71281292, 55.42562584, 110.8512517,
                    221.7025034, 443.4050067, 886.8100135]},
        {"instance": Acceleration(), "input": movements,
         "output": [1.732050808, 3.464101615, 6.92820323, 13.85640646, 27.71281292, 55.42562584, 110.8512517,
                    221.7025034, 443.4050067, 886.8100135]},
    ]

    def test_calculate(self):
        for i in self.inputs:
            result = i["instance"].calculate(i["input"])
            for actual, expected in zip(result.data, i["output"]):
                self.assertAlmostEqual(actual, expected)
