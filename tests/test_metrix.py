from unittest import TestCase

from server.metrix.acceleration import Acceleration
from server.metrix.angular_velocity import AngularVelocity
from server.metrix.controller_rotation_distance import ControllerRotationDistance
from server.metrix.device_distance import DeviceDistance
from server.metrix.jerk import Jerk
from server.metrix.velocity import Velocity
from server.models.movement import Movement, HEADSET, CONTROLLER_1

movements = [Movement.from_dict({"session_id": "test",
                                 "user_id": "test",
                                 "timestamp": i,
                                 "controller_id": HEADSET if i < 5 else CONTROLLER_1,
                                 "x": 2 ** i,
                                 "y": 2 ** i,
                                 "z": 2 ** i,
                                 "yaw": 10 * i,
                                 "pitch": 10 * i,
                                 "roll": 10 * i,
                                 "r_x": "test",
                                 "r_y": "test",
                                 "r_z": "test",
                                 }) for i in range(11)]


class TestMetrix(TestCase):
    inputs = [
        {"instance": Acceleration(), "input": movements,
         "output": [1.732050808, 3.464101615, 6.92820323, 13.85640646, 27.71281292, 55.42562584, 110.8512517,
                    221.7025034, 443.4050067, 886.8100135]},
        {"instance": AngularVelocity(), "input": movements,
         "output": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
        {"instance": DeviceDistance(), "input": movements,
         "output": [53.69357503, 107.3871501, 214.7743001, 429.5486003, 859.0972006]},
        {"instance": Jerk(), "input": movements,
         "output": [1.732050808, 3.464101615, 6.92820323, 13.85640646, 27.71281292, 55.42562584, 110.8512517,
                    221.7025034, 443.4050067, 886.8100135]},
        {"instance": Velocity(), "input": movements,
         "output": [1.732050808, 3.464101615, 6.92820323, 13.85640646, 27.71281292, 55.42562584, 110.8512517,
                    221.7025034, 443.4050067, 886.8100135]},
        {"instance": ControllerRotationDistance(), "input": movements,
         "output": [2.60399337378509, 2.421506186837233, 1.7349783800532632, 0.5937117361875303, 0.23922660394788026,
                    2.8608599752896566, 2.5261398206886003, 1.4535037983135297, 0.705858391200047, 0.4939327415621836]}
    ]

    def test_calculate(self):
        for i in self.inputs:
            result = i["instance"].calculate(i["input"])
            expected: float
            for actual, expected in zip(result.data, i["output"]):
                self.assertAlmostEqual(actual, expected, msg=i["instance"].__class__.__name__)
