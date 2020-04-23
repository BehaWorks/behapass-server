import os

DB_HOST = "mongodb://" + os.environ["db_host"] + ":" + os.environ["db_port"] + "/"
DB_NAME = "behaworks_logger_v8"
DB_PORT = ""
URL_PREFIX = "/api"
MINIMUM_RECORDS = 10
MAXIMAL_DISTANCE = 16
try:
    METRIX_CHUNKS = int(os.environ["metrix_chunks"])
except (ValueError, KeyError):
    METRIX_CHUNKS = 3

try:
    NEIGHBOURS = int(os.environ["neighbours"])
except (ValueError, KeyError):
    NEIGHBOURS = 1

FEATURE_SELECTION = [
 # accuracy: 0.7972027972027972
 # f1-micro: 0.7972027972027973
 # f1-macro: 0.6882422402159245
 # TPR:      0.5961538461538461
 # FPR:      0.08791208791208792
 # TNR:      0.9120879120879121
 # FNR:      0.40384615384615385
 ['velocity_minimum', 'velocity_maximum', 'velocity_std_dev', 'acceleration_minimum',
  'acceleration_maximum',
  'acceleration_std_dev', 'velocity_minimum_0', 'velocity_maximum_0', 'velocity_std_dev_0',
  'acceleration_minimum_0', 'acceleration_maximum_0', 'acceleration_std_dev_0',
  'velocity_minimum_1',
  'velocity_maximum_1', 'velocity_std_dev_1', 'acceleration_minimum_1', 'acceleration_maximum_1',
  'acceleration_std_dev_1', 'velocity_minimum_2', 'velocity_maximum_2', 'velocity_std_dev_2',
  'acceleration_minimum_2', 'acceleration_maximum_2', 'acceleration_std_dev_2', 'jerk_minimum',
  'jerk_maximum', 'jerk_std_dev', 'jerk_minimum_0', 'jerk_maximum_0', 'jerk_std_dev_0',
  'jerk_minimum_1',
  'jerk_maximum_1', 'jerk_std_dev_1', 'jerk_minimum_2', 'jerk_maximum_2', 'jerk_std_dev_2',
  'angular_velocity_iqr', 'angular_velocity_iqr_0', 'angular_velocity_iqr_1',
  'angular_velocity_iqr_2',
  'device_distance_average', 'device_distance_median', 'device_distance_average_0',
  'device_distance_median_0', 'device_distance_average_1', 'device_distance_median_1',
  'device_distance_average_2', 'device_distance_median_2', 'device_distance_minimum',
  'device_distance_maximum', 'device_distance_std_dev', 'device_distance_minimum_0',
  'device_distance_maximum_0', 'device_distance_std_dev_0', 'device_distance_minimum_1',
  'device_distance_maximum_1', 'device_distance_std_dev_1', 'device_distance_minimum_2',
  'device_distance_maximum_2', 'device_distance_std_dev_2', 'device_distance_iqr',
  'device_distance_iqr_0',
  'device_distance_iqr_1', 'device_distance_iqr_2', 'controller_rotation_distance_average',
  'controller_rotation_distance_median', 'controller_rotation_distance_average_0',
  'controller_rotation_distance_median_0', 'controller_rotation_distance_average_1',
  'controller_rotation_distance_median_1', 'controller_rotation_distance_average_2',
  'controller_rotation_distance_median_2'],

 # accuracy  0.8156028369
 # f1_micro  0.8156028369
 # f1_macro  0.6411109827
 # TPR       0.5192307692
 # FPR       0.01123595506
 # TNR       0.9887640449
 # FNR       0.4807692308
 ['stroke_length', 'stroke_length0', 'stroke_length1', 'stroke_length2', 'velocity_minimum',
  'velocity_maximum', 'velocity_std_dev', 'acceleration_minimum', 'acceleration_maximum',
  'acceleration_std_dev', 'velocity_minimum_0', 'velocity_maximum_0', 'velocity_std_dev_0',
  'acceleration_minimum_0', 'acceleration_maximum_0', 'acceleration_std_dev_0',
  'velocity_minimum_1', 'velocity_maximum_1', 'velocity_std_dev_1', 'acceleration_minimum_1',
  'acceleration_maximum_1', 'acceleration_std_dev_1', 'velocity_minimum_2', 'velocity_maximum_2',
  'velocity_std_dev_2', 'acceleration_minimum_2', 'acceleration_maximum_2',
  'acceleration_std_dev_2', 'jerk_minimum', 'jerk_maximum', 'jerk_std_dev', 'jerk_minimum_0',
  'jerk_maximum_0', 'jerk_std_dev_0', 'jerk_minimum_1', 'jerk_maximum_1', 'jerk_std_dev_1',
  'jerk_minimum_2', 'jerk_maximum_2', 'jerk_std_dev_2', 'angular_velocity_iqr',
  'angular_velocity_iqr_0', 'angular_velocity_iqr_1', 'angular_velocity_iqr_2',
  'device_distance_average', 'device_distance_median', 'device_distance_average_0',
  'device_distance_median_0', 'device_distance_average_1', 'device_distance_median_1',
  'device_distance_average_2', 'device_distance_median_2', 'device_distance_minimum',
  'device_distance_maximum', 'device_distance_std_dev', 'device_distance_minimum_0',
  'device_distance_maximum_0', 'device_distance_std_dev_0', 'device_distance_minimum_1',
  'device_distance_maximum_1', 'device_distance_std_dev_1', 'device_distance_minimum_2',
  'device_distance_maximum_2', 'device_distance_std_dev_2', 'device_distance_iqr',
  'device_distance_iqr_0', 'device_distance_iqr_1', 'device_distance_iqr_2',
  'controller_rotation_distance_average', 'controller_rotation_distance_median',
  'controller_rotation_distance_average_0', 'controller_rotation_distance_median_0',
  'controller_rotation_distance_average_1', 'controller_rotation_distance_median_1',
  'controller_rotation_distance_average_2', 'controller_rotation_distance_median_2'],

 # best results so far, origin uncertain
 ['velocity_average', 'velocity_median', 'velocity_minimum', 'velocity_maximum', 'velocity_std_dev',
  'velocity_iqr', 'velocity_average_0', 'velocity_median_0', 'velocity_minimum_0', 'velocity_maximum_0',
  'velocity_std_dev_0', 'velocity_iqr_0', 'velocity_average_1', 'velocity_median_1', 'velocity_minimum_1',
  'velocity_maximum_1', 'velocity_std_dev_1', 'velocity_iqr_1', 'velocity_average_2', 'velocity_median_2',
  'velocity_minimum_2', 'velocity_maximum_2', 'velocity_std_dev_2', 'velocity_iqr_2', 'angular_velocity_average',
  'angular_velocity_median', 'angular_velocity_minimum', 'angular_velocity_maximum', 'angular_velocity_std_dev',
  'angular_velocity_iqr', 'angular_velocity_average_0', 'angular_velocity_median_0', 'angular_velocity_minimum_0',
  'angular_velocity_maximum_0', 'angular_velocity_std_dev_0', 'angular_velocity_iqr_0',
  'angular_velocity_average_1', 'angular_velocity_median_1', 'angular_velocity_minimum_1',
  'angular_velocity_maximum_1', 'angular_velocity_std_dev_1', 'angular_velocity_iqr_1',
  'angular_velocity_average_2', 'angular_velocity_median_2', 'angular_velocity_minimum_2',
  'angular_velocity_maximum_2', 'angular_velocity_std_dev_2', 'angular_velocity_iqr_2', 'device_distance_average',
  'device_distance_median', 'device_distance_minimum', 'device_distance_maximum', 'device_distance_std_dev',
  'device_distance_iqr', 'device_distance_average_0', 'device_distance_median_0', 'device_distance_minimum_0',
  'device_distance_maximum_0', 'device_distance_std_dev_0', 'device_distance_iqr_0', 'device_distance_average_1',
  'device_distance_median_1', 'device_distance_minimum_1', 'device_distance_maximum_1',
  'device_distance_std_dev_1', 'device_distance_iqr_1', 'device_distance_average_2', 'device_distance_median_2',
  'device_distance_minimum_2', 'device_distance_maximum_2', 'device_distance_std_dev_2', 'device_distance_iqr_2']]
