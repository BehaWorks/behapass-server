from server import config
from server.metrix.result import Result


class MetrixVector:
    CHUNKS = config["METRIX_CHUNKS"]
    VECTOR_LENGTH = 29 * CHUNKS + 2

    def __init__(self, velocity: Result, acceleration: Result, jerk: Result, angular_velocity: Result,
                 device_distance: Result, session_id, user_id) -> None:
        self.data = {
            "user_id": user_id,
            "session_id": session_id,
            "velocity_average": velocity.average,
            "velocity_median": velocity.median,
            "velocity_minimum": velocity.minimum,
            "velocity_maximum": velocity.maximum,
            "velocity_std_dev": velocity.std_dev,
            "velocity_iqr": velocity.interquartile_range,
            "acceleration_average": acceleration.average,
            "acceleration_median": acceleration.median,
            "acceleration_minimum": acceleration.minimum,
            "acceleration_maximum": acceleration.maximum,
            "acceleration_std_dev": acceleration.std_dev,
            "acceleration_iqr": acceleration.interquartile_range,
            "jerk_average": jerk.average,
            "jerk_median": jerk.median,
            "jerk_minimum": jerk.minimum,
            "jerk_maximum": jerk.maximum,
            "jerk_std_dev": jerk.std_dev,
            "jerk_iqr": jerk.upper_q - jerk.lower_q,
            "angular_velocity_average": angular_velocity.average,
            "angular_velocity_median": angular_velocity.median,
            "angular_velocity_minimum": angular_velocity.minimum,
            "angular_velocity_maximum": angular_velocity.maximum,
            "angular_velocity_std_dev": angular_velocity.std_dev,
            "angular_velocity_iqr": angular_velocity.interquartile_range,
            "device_distance_average": device_distance.average,
            "device_distance_median": device_distance.median,
            "device_distance_minimum": device_distance.minimum,
            "device_distance_maximum": device_distance.maximum,
            "device_distance_std_dev": device_distance.std_dev,
            "device_distance_iqr": device_distance.interquartile_range
        }
        self.create_chunks_part(velocity, acceleration, jerk, angular_velocity, device_distance)

    def create_chunks_part(self, velocity: Result, acceleration: Result, jerk: Result, angular_velocity: Result,
                           device_distance: Result):
        for i in range(self.CHUNKS):
            self.data = {
                **self.data,
                "velocity_average_" + str(i): velocity.average_chunk(self.CHUNKS, i),
                "velocity_median_" + str(i): velocity.median_chunk(self.CHUNKS, i),
                "velocity_minimum_" + str(i): velocity.minimum_chunk(self.CHUNKS, i),
                "velocity_maximum_" + str(i): velocity.maximum_chunk(self.CHUNKS, i),
                "velocity_std_dev_" + str(i): velocity.std_dev_chunk(self.CHUNKS, i),
                "velocity_iqr_" + str(i): velocity.interquartile_range_chunk(self.CHUNKS, i),
                "acceleration_average_" + str(i): acceleration.average_chunk(self.CHUNKS, i),
                "acceleration_median_" + str(i): acceleration.median_chunk(self.CHUNKS, i),
                "acceleration_minimum_" + str(i): acceleration.minimum_chunk(self.CHUNKS, i),
                "acceleration_maximum_" + str(i): acceleration.maximum_chunk(self.CHUNKS, i),
                "acceleration_std_dev_" + str(i): acceleration.std_dev_chunk(self.CHUNKS, i),
                "acceleration_iqr_" + str(i): acceleration.interquartile_range_chunk(self.CHUNKS, i),
                "jerk_average_" + str(i): jerk.average_chunk(self.CHUNKS, i),
                "jerk_median_" + str(i): jerk.median_chunk(self.CHUNKS, i),
                "jerk_minimum_" + str(i): jerk.minimum_chunk(self.CHUNKS, i),
                "jerk_maximum_" + str(i): jerk.maximum_chunk(self.CHUNKS, i),
                "jerk_std_dev_" + str(i): jerk.std_dev_chunk(self.CHUNKS, i),
                "jerk_iqr_" + str(i): jerk.interquartile_range_chunk(self.CHUNKS, i),
                "angular_velocity_average_" + str(i): angular_velocity.average_chunk(self.CHUNKS, i),
                "angular_velocity_median_" + str(i): angular_velocity.median_chunk(self.CHUNKS, i),
                "angular_velocity_minimum_" + str(i): angular_velocity.minimum_chunk(self.CHUNKS, i),
                "angular_velocity_maximum_" + str(i): angular_velocity.maximum_chunk(self.CHUNKS, i),
                "angular_velocity_std_dev_" + str(i): angular_velocity.std_dev_chunk(self.CHUNKS, i),
                "angular_velocity_iqr_" + str(i): angular_velocity.interquartile_range_chunk(self.CHUNKS, i),
                "device_distance_average_" + str(i): device_distance.average_chunk(self.CHUNKS, i),
                "device_distance_median_" + str(i): device_distance.median_chunk(self.CHUNKS, i),
                "device_distance_minimum_" + str(i): device_distance.minimum_chunk(self.CHUNKS, i),
                "device_distance_maximum_" + str(i): device_distance.maximum_chunk(self.CHUNKS, i),
                "device_distance_std_dev_" + str(i): device_distance.std_dev_chunk(self.CHUNKS, i),
                "device_distance_iqr_" + str(i): device_distance.interquartile_range_chunk(self.CHUNKS, i)
            }

    def to_dict(self):
        return self.data
