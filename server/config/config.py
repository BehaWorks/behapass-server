import os

DB_HOST = "mongodb://" + os.environ["db_host"] + ":" + os.environ["db_port"] + "/"
DB_NAME = "behaworks_logger_v10"
DB_PORT = ""
URL_PREFIX = "/api"
MINIMUM_RECORDS = 10
MAXIMAL_DISTANCE = 23
try:
    METRIX_CHUNKS = int(os.environ["metrix_chunks"])
except (ValueError, KeyError):
    METRIX_CHUNKS = 3

try:
    NEIGHBOURS = int(os.environ["neighbours"])
except (ValueError, KeyError):
    NEIGHBOURS = 1

FEATURE_SELECTION = [
    # ACC: 0.8823529411764706
    # FPR: 0.21568627450980393
    # FNR: 0.0117647058823529
    ['velocity_average', 'velocity_median', 'acceleration_median', 'acceleration_iqr', 'jerk_median', 'jerk_iqr',
     'angular_velocity_average', 'angular_velocity_median', 'device_distance_average', 'device_distance_median',
     'device_distance_maximum', 'device_distance_std_dev', 'device_distance_iqr',
     'controller_rotation_distance_average', 'controller_rotation_distance_median',
     'controller_rotation_distance_maximum', 'controller_rotation_distance_std_dev', 'controller_rotation_distance_iqr',
     'velocity_average_0', 'velocity_median_0', 'velocity_maximum_0', 'velocity_std_dev_0', 'velocity_iqr_0',
     'acceleration_average_0', 'acceleration_median_0', 'acceleration_std_dev_0', 'acceleration_iqr_0',
     'jerk_average_0', 'jerk_median_0', 'angular_velocity_average_0', 'angular_velocity_median_0',
     'angular_velocity_maximum_0', 'angular_velocity_std_dev_0', 'angular_velocity_iqr_0', 'device_distance_average_0',
     'device_distance_median_0', 'device_distance_minimum_0', 'device_distance_maximum_0', 'device_distance_std_dev_0',
     'device_distance_iqr_0', 'controller_rotation_distance_average_0', 'controller_rotation_distance_median_0',
     'controller_rotation_distance_maximum_0', 'controller_rotation_distance_std_dev_0', 'velocity_average_1',
     'velocity_median_1', 'velocity_minimum_1', 'acceleration_median_1', 'angular_velocity_average_1',
     'angular_velocity_median_1', 'angular_velocity_minimum_1', 'device_distance_maximum_1',
     'controller_rotation_distance_average_1', 'controller_rotation_distance_median_1',
     'controller_rotation_distance_minimum_1', 'controller_rotation_distance_maximum_1',
     'controller_rotation_distance_std_dev_1', 'velocity_average_2', 'velocity_median_2', 'velocity_minimum_2',
     'velocity_maximum_2', 'velocity_std_dev_2', 'acceleration_average_2', 'acceleration_median_2',
     'acceleration_iqr_2', 'jerk_median_2', 'jerk_iqr_2', 'angular_velocity_average_2', 'angular_velocity_median_2',
     'angular_velocity_minimum_2', 'angular_velocity_maximum_2', 'angular_velocity_std_dev_2', 'angular_velocity_iqr_2',
     'device_distance_average_2', 'device_distance_median_2', 'device_distance_maximum_2', 'device_distance_std_dev_2',
     'device_distance_iqr_2', 'controller_rotation_distance_average_2', 'controller_rotation_distance_median_2',
     'controller_rotation_distance_minimum_2'],

    # ACC: 0.8676470588235294
    # FPR: 0.21568627450980393
    # FNR: 0.05882352941176472
    ['velocity_average', 'velocity_median', 'acceleration_median', 'acceleration_iqr', 'jerk_median', 'jerk_iqr',
     'angular_velocity_average', 'angular_velocity_median', 'device_distance_average', 'device_distance_median',
     'device_distance_maximum', 'device_distance_std_dev', 'device_distance_iqr',
     'controller_rotation_distance_average', 'controller_rotation_distance_median',
     'controller_rotation_distance_maximum', 'controller_rotation_distance_std_dev', 'controller_rotation_distance_iqr',
     'velocity_average_0', 'velocity_maximum_0', 'velocity_std_dev_0', 'velocity_iqr_0', 'acceleration_average_0',
     'acceleration_median_0', 'acceleration_std_dev_0', 'acceleration_iqr_0', 'jerk_average_0',
     'angular_velocity_average_0', 'angular_velocity_median_0', 'angular_velocity_maximum_0',
     'angular_velocity_std_dev_0', 'angular_velocity_iqr_0', 'device_distance_average_0', 'device_distance_median_0',
     'device_distance_minimum_0', 'device_distance_maximum_0', 'device_distance_std_dev_0',
     'controller_rotation_distance_average_0', 'controller_rotation_distance_median_0', 'velocity_average_1',
     'velocity_median_1', 'velocity_minimum_1', 'angular_velocity_average_1', 'angular_velocity_median_1',
     'angular_velocity_minimum_1', 'device_distance_maximum_1', 'controller_rotation_distance_average_1',
     'controller_rotation_distance_median_1', 'controller_rotation_distance_minimum_1',
     'controller_rotation_distance_maximum_1', 'controller_rotation_distance_std_dev_1', 'velocity_average_2',
     'velocity_median_2', 'velocity_minimum_2', 'velocity_maximum_2', 'acceleration_average_2', 'acceleration_median_2',
     'acceleration_iqr_2', 'jerk_median_2', 'jerk_iqr_2', 'angular_velocity_average_2', 'angular_velocity_median_2',
     'angular_velocity_minimum_2', 'angular_velocity_maximum_2', 'angular_velocity_std_dev_2', 'angular_velocity_iqr_2',
     'device_distance_average_2', 'device_distance_median_2', 'device_distance_maximum_2', 'device_distance_std_dev_2',
     'device_distance_iqr_2', 'controller_rotation_distance_average_2', 'controller_rotation_distance_median_2',
     'controller_rotation_distance_minimum_2'],

    # ACC: 0.8676470588235294
    # FPR: 0.3333333333333333
    # FNR: 0.0
    ['velocity_average', 'velocity_median', 'acceleration_median', 'acceleration_iqr', 'jerk_median', 'jerk_iqr',
     'angular_velocity_average', 'angular_velocity_median', 'angular_velocity_std_dev', 'device_distance_average',
     'device_distance_median', 'device_distance_maximum', 'device_distance_std_dev', 'device_distance_iqr',
     'controller_rotation_distance_average', 'controller_rotation_distance_median',
     'controller_rotation_distance_minimum', 'controller_rotation_distance_maximum',
     'controller_rotation_distance_std_dev', 'controller_rotation_distance_iqr', 'stroke_length', 'velocity_average_0',
     'velocity_median_0', 'velocity_maximum_0', 'velocity_std_dev_0', 'velocity_iqr_0', 'acceleration_average_0',
     'acceleration_median_0', 'acceleration_std_dev_0', 'acceleration_iqr_0', 'jerk_average_0', 'jerk_median_0',
     'angular_velocity_average_0', 'angular_velocity_median_0', 'angular_velocity_maximum_0',
     'angular_velocity_std_dev_0', 'angular_velocity_iqr_0', 'device_distance_average_0', 'device_distance_median_0',
     'device_distance_minimum_0', 'device_distance_maximum_0', 'device_distance_std_dev_0', 'device_distance_iqr_0',
     'controller_rotation_distance_average_0', 'controller_rotation_distance_median_0',
     'controller_rotation_distance_maximum_0', 'controller_rotation_distance_std_dev_0', 'stroke_length0',
     'velocity_average_1', 'velocity_median_1', 'velocity_minimum_1', 'acceleration_median_1',
     'angular_velocity_average_1', 'angular_velocity_median_1', 'angular_velocity_minimum_1',
     'device_distance_maximum_1', 'controller_rotation_distance_average_1', 'controller_rotation_distance_median_1',
     'controller_rotation_distance_minimum_1', 'controller_rotation_distance_maximum_1',
     'controller_rotation_distance_std_dev_1', 'stroke_length1', 'velocity_average_2', 'velocity_median_2',
     'velocity_minimum_2', 'velocity_maximum_2', 'velocity_std_dev_2', 'acceleration_average_2',
     'acceleration_median_2', 'acceleration_iqr_2', 'jerk_median_2', 'jerk_iqr_2', 'angular_velocity_average_2',
     'angular_velocity_median_2', 'angular_velocity_minimum_2', 'angular_velocity_maximum_2',
     'angular_velocity_std_dev_2', 'angular_velocity_iqr_2', 'device_distance_average_2', 'device_distance_median_2',
     'device_distance_minimum_2', 'device_distance_maximum_2', 'device_distance_std_dev_2', 'device_distance_iqr_2',
     'controller_rotation_distance_average_2', 'controller_rotation_distance_median_2',
     'controller_rotation_distance_minimum_2', 'stroke_length2'],

    None

]
