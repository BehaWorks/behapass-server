import numpy as np
import math

from . import Metric, Result

class Device_distance(Metric):
    def calculate(self, data: list) -> Result:
        controller_coordinates, hmd_coordinates = self.extract_coordinates_timestamps(data)
        device_distance = self.calculate_distance(controller_coordinates, hmd_coordinates)
        device_distance = Result(device_distance)
        return device_distance

    def extract_coordinates_timestamps(self, movements):
        controller_coordinates = []
        hmd_coordinates = []

        for movement in movements:
            if movement.controller_id == 'LHR-BE784403':
                hmd_coordinates.append([movement.x, movement.y, movement.z])
            else:
                controller_coordinates.append([movement.x, movement.y, movement.z])

        return controller_coordinates, hmd_coordinates


    def calculate_distance(self, controller_coordinates, hmd_coordinates):
        device_distances = []

        for hmd,controller in zip(hmd_coordinates, controller_coordinates):
            x_diff = hmd[0] - controller[0]
            y_diff = hmd[1] - controller[1]
            z_diff = hmd[2] - controller[2]

            distance_pow_2 = x_diff**2 + y_diff**2 + z_diff**2
            distance = math.sqrt(distance_pow_2)
            device_distances.append(distance)

        return device_distances
