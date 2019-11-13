from unittest import TestCase

from server.metrix.acceleration import Acceleration
from server.metrix.velocity import Velocity

movements = [{'session_id': 'test',
              'user_id': 'test',
              'timestamp': i,
              'controller_id': 'test',
              'x': 2 ** i,
              'y': 2 ** i,
              'z': 2 ** i,
              'yaw': 'test',
              'pitch': 'test',
              'roll': 'test',
              'r_x': 'test',
              'r_y': 'test',
              'r_z': 'test',
              } for i in range(11)]


class TestMetrix(TestCase):
    inputs = [
        {"instance": Velocity(), "input": movements, "output": 177.1887976},
        {"instance": Acceleration(), "input": movements, "output": 98.34199585},
    ]

    def test_calculate(self):
        for i in self.inputs:
            self.assertAlmostEqual(i["instance"].calculate(i["input"]), i["output"])
