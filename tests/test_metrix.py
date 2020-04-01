from unittest import TestCase

from server.metrix.acceleration import Acceleration
from server.metrix.angular_velocity import AngularVelocity
from server.metrix.controller_rotation_distance import ControllerRotationDistance
from server.metrix.device_distance import DeviceDistance
from server.metrix.jerk import Jerk
from server.metrix.time_length import TimeLength
from server.metrix.trigger_pressure_change import TriggerPressureChange
from server.metrix.velocity import Velocity
from server.models.button import Button
from server.models.movement import Movement, HEADSET, CONTROLLER_1

movements = [Movement.from_dict({"session_id": "test",
                                 "user_id": "test",
                                 "timestamp": i,
                                 "controller_id": HEADSET if i < 5 else CONTROLLER_1,
                                 "x": 2 ** i,
                                 "y": 2 ** i,
                                 "z": 2 ** i,
                                 "yaw": 10 if i < 5 else 50,
                                 "pitch": 10 if i < 5 else 50,
                                 "roll": 10 if i < 5 else 50,
                                 "r_x": "test",
                                 "r_y": "test",
                                 "r_z": "test",
                                 }) for i in range(11)]

buttons = [Button.from_dict({"session_id": "string",
                             "user_id": "string",
                             "timestamp": 0,
                             "controller_id": "string",
                             "trigger": 0 if i < 5 else 0.5,
                             "trackpad_x": 0,
                             "trackpad_y": 0,
                             "button_pressed": 0,
                             "button_touched": 0,
                             "menu_button": True,
                             "trackpad_pressed": True,
                             "trackpad_touched": True,
                             "grip_button": True,
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
         "output": [0.0, 0.0, 0.0, 0.0, 0.47725676001698336, 1.1102230246251565e-16, 1.1102230246251565e-16,
                    1.1102230246251565e-16, 1.1102230246251565e-16, 1.1102230246251565e-16]},
        {"instance": TimeLength(), "input": movements,
         "output": [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]},
        {"instance": TriggerPressureChange(), "input": buttons,
         "output": [0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0]},
    ]

    def test_calculate(self):
        for i in self.inputs:
            result = i["instance"].calculate(i["input"])
            expected: float
            for actual, expected in zip(result.data, i["output"]):
                self.assertAlmostEqual(actual, expected, msg=i["instance"].__class__.__name__)
