import os

DB_HOST = "mongodb://" + os.environ["db_host"] + ":" + os.environ["db_port"] + "/"
DB_NAME = "behaworks_logger_v10"
DB_PORT = ""
REDIS_HOST = os.environ["redis_host"]
try:
 REDIS_PORT = os.environ["redis_port"]
except KeyError:
 REDIS_PORT = 6379
try:
 REGISTRATION_EXPIRE = int(os.environ["registration_expire"])
except (ValueError, KeyError):
 REGISTRATION_EXPIRE = 600
URL_PREFIX = "/api"
MINIMUM_RECORDS = 10
MAXIMAL_DISTANCE = 12
try:
 METRIX_CHUNKS = int(os.environ["metrix_chunks"])
except (ValueError, KeyError):
 METRIX_CHUNKS = 3

try:
 NEIGHBOURS = int(os.environ["neighbours"])
except (ValueError, KeyError):
    NEIGHBOURS = 1

FEATURE_SELECTION = [

 #56
 # accuracy    0.776106
 # f1_micro    0.776106
 # f1_macro    0.734777
 # TPR         0.787764
 # FPR         0.214602
 # TNR         0.785398
 # FNR         0.212236
 ['velocity_average', 'velocity_median', 'acceleration_median', 'acceleration_iqr', 'jerk_median', 'jerk_iqr', 'angular_velocity_average', 'angular_velocity_median', 'device_distance_average', 'device_distance_median', 'device_distance_maximum', 'device_distance_std_dev', 'controller_rotation_distance_average', 'controller_rotation_distance_median', 'controller_rotation_distance_maximum', 'controller_rotation_distance_std_dev', 'controller_rotation_distance_iqr', 'velocity_maximum_0', 'velocity_std_dev_0', 'velocity_iqr_0', 'acceleration_average_0', 'acceleration_median_0', 'acceleration_std_dev_0', 'acceleration_iqr_0', 'angular_velocity_average_0', 'angular_velocity_median_0', 'angular_velocity_maximum_0', 'angular_velocity_std_dev_0', 'angular_velocity_iqr_0', 'device_distance_average_0', 'device_distance_median_0', 'device_distance_minimum_0', 'device_distance_maximum_0', 'velocity_average_1', 'velocity_median_1', 'angular_velocity_average_1', 'angular_velocity_median_1', 'angular_velocity_minimum_1', 'controller_rotation_distance_median_1', 'velocity_average_2', 'velocity_median_2', 'velocity_maximum_2', 'acceleration_median_2', 'jerk_median_2', 'angular_velocity_average_2', 'angular_velocity_median_2', 'angular_velocity_minimum_2', 'angular_velocity_maximum_2', 'angular_velocity_std_dev_2', 'angular_velocity_iqr_2', 'device_distance_average_2', 'device_distance_median_2', 'device_distance_maximum_2', 'device_distance_std_dev_2', 'device_distance_iqr_2', 'controller_rotation_distance_median_2'],

 #55
 # accuracy    0.755859
 # f1_micro    0.755859
 # f1_macro    0.718521
 # TPR         0.755496
 # FPR         0.213054
 # TNR         0.786946
 # FNR         0.244504
 ['velocity_average', 'velocity_median', 'acceleration_median', 'acceleration_iqr', 'jerk_median', 'jerk_iqr', 'angular_velocity_average', 'angular_velocity_median', 'device_distance_average', 'device_distance_median', 'device_distance_maximum', 'device_distance_std_dev', 'controller_rotation_distance_average', 'controller_rotation_distance_median', 'controller_rotation_distance_maximum', 'controller_rotation_distance_std_dev', 'velocity_maximum_0', 'velocity_std_dev_0', 'velocity_iqr_0', 'acceleration_average_0', 'acceleration_median_0', 'acceleration_std_dev_0', 'acceleration_iqr_0', 'angular_velocity_average_0', 'angular_velocity_median_0', 'angular_velocity_maximum_0', 'angular_velocity_std_dev_0', 'angular_velocity_iqr_0', 'device_distance_average_0', 'device_distance_median_0', 'device_distance_minimum_0', 'device_distance_maximum_0', 'velocity_average_1', 'velocity_median_1', 'angular_velocity_average_1', 'angular_velocity_median_1', 'angular_velocity_minimum_1', 'controller_rotation_distance_median_1', 'velocity_average_2', 'velocity_median_2', 'velocity_maximum_2', 'acceleration_median_2', 'jerk_median_2', 'angular_velocity_average_2', 'angular_velocity_median_2', 'angular_velocity_minimum_2', 'angular_velocity_maximum_2', 'angular_velocity_std_dev_2', 'angular_velocity_iqr_2', 'device_distance_average_2', 'device_distance_median_2', 'device_distance_maximum_2', 'device_distance_std_dev_2', 'device_distance_iqr_2', 'controller_rotation_distance_median_2'],

 #58
 # accuracy    0.767858
 # f1_micro    0.767858
 # f1_macro    0.716326
 # TPR         0.790936
 # FPR         0.243215
 # TNR         0.756785
 # FNR         0.209064
 ['velocity_average', 'velocity_median', 'acceleration_median', 'acceleration_iqr', 'jerk_median', 'jerk_iqr', 'angular_velocity_average', 'angular_velocity_median', 'device_distance_average', 'device_distance_median', 'device_distance_maximum', 'device_distance_std_dev', 'controller_rotation_distance_average', 'controller_rotation_distance_median', 'controller_rotation_distance_maximum', 'controller_rotation_distance_std_dev', 'controller_rotation_distance_iqr', 'velocity_maximum_0', 'velocity_std_dev_0', 'velocity_iqr_0', 'acceleration_average_0', 'acceleration_median_0', 'acceleration_std_dev_0', 'acceleration_iqr_0', 'angular_velocity_average_0', 'angular_velocity_median_0', 'angular_velocity_maximum_0', 'angular_velocity_std_dev_0', 'angular_velocity_iqr_0', 'device_distance_average_0', 'device_distance_median_0', 'device_distance_minimum_0', 'device_distance_maximum_0', 'velocity_average_1', 'velocity_median_1', 'angular_velocity_average_1', 'angular_velocity_median_1', 'angular_velocity_minimum_1', 'controller_rotation_distance_average_1', 'controller_rotation_distance_median_1', 'velocity_average_2', 'velocity_median_2', 'velocity_maximum_2', 'acceleration_median_2', 'jerk_median_2', 'angular_velocity_average_2', 'angular_velocity_median_2', 'angular_velocity_minimum_2', 'angular_velocity_maximum_2', 'angular_velocity_std_dev_2', 'angular_velocity_iqr_2', 'device_distance_average_2', 'device_distance_median_2', 'device_distance_maximum_2', 'device_distance_std_dev_2', 'device_distance_iqr_2', 'controller_rotation_distance_average_2', 'controller_rotation_distance_median_2'],

 #57
 # accuracy    0.770028
 # f1_micro    0.770028
 # f1_macro    0.722546
 # TPR         0.789315
 # FPR         0.230818
 # TNR         0.769182
 # FNR         0.210685
 ['velocity_average', 'velocity_median', 'acceleration_median', 'acceleration_iqr', 'jerk_median', 'jerk_iqr', 'angular_velocity_average', 'angular_velocity_median', 'device_distance_average', 'device_distance_median', 'device_distance_maximum', 'device_distance_std_dev', 'controller_rotation_distance_average', 'controller_rotation_distance_median', 'controller_rotation_distance_maximum', 'controller_rotation_distance_std_dev', 'controller_rotation_distance_iqr', 'velocity_maximum_0', 'velocity_std_dev_0', 'velocity_iqr_0', 'acceleration_average_0', 'acceleration_median_0', 'acceleration_std_dev_0', 'acceleration_iqr_0', 'angular_velocity_average_0', 'angular_velocity_median_0', 'angular_velocity_maximum_0', 'angular_velocity_std_dev_0', 'angular_velocity_iqr_0', 'device_distance_average_0', 'device_distance_median_0', 'device_distance_minimum_0', 'device_distance_maximum_0', 'velocity_average_1', 'velocity_median_1', 'angular_velocity_average_1', 'angular_velocity_median_1', 'angular_velocity_minimum_1', 'controller_rotation_distance_median_1', 'velocity_average_2', 'velocity_median_2', 'velocity_maximum_2', 'acceleration_median_2', 'jerk_median_2', 'angular_velocity_average_2', 'angular_velocity_median_2', 'angular_velocity_minimum_2', 'angular_velocity_maximum_2', 'angular_velocity_std_dev_2', 'angular_velocity_iqr_2', 'device_distance_average_2', 'device_distance_median_2', 'device_distance_maximum_2', 'device_distance_std_dev_2', 'device_distance_iqr_2', 'controller_rotation_distance_average_2', 'controller_rotation_distance_median_2'],

 #54
 # accuracy    0.757878
 # f1_micro    0.757878
 # f1_macro    0.723530
 # TPR         0.756507
 # FPR         0.208301
 # TNR         0.791699
 # FNR         0.243493
 ['velocity_average', 'velocity_median', 'acceleration_median', 'acceleration_iqr', 'jerk_median', 'jerk_iqr', 'angular_velocity_average', 'angular_velocity_median', 'device_distance_average', 'device_distance_median', 'device_distance_maximum', 'device_distance_std_dev', 'controller_rotation_distance_average', 'controller_rotation_distance_median', 'controller_rotation_distance_maximum', 'controller_rotation_distance_std_dev', 'velocity_maximum_0', 'velocity_std_dev_0', 'velocity_iqr_0', 'acceleration_average_0', 'acceleration_median_0', 'acceleration_iqr_0', 'angular_velocity_average_0', 'angular_velocity_median_0', 'angular_velocity_maximum_0', 'angular_velocity_std_dev_0', 'angular_velocity_iqr_0', 'device_distance_average_0', 'device_distance_median_0', 'device_distance_minimum_0', 'device_distance_maximum_0', 'velocity_average_1', 'velocity_median_1', 'angular_velocity_average_1', 'angular_velocity_median_1', 'angular_velocity_minimum_1', 'controller_rotation_distance_median_1', 'velocity_average_2', 'velocity_median_2', 'velocity_maximum_2', 'acceleration_median_2', 'jerk_median_2', 'angular_velocity_average_2', 'angular_velocity_median_2', 'angular_velocity_minimum_2', 'angular_velocity_maximum_2', 'angular_velocity_std_dev_2', 'angular_velocity_iqr_2', 'device_distance_average_2', 'device_distance_median_2', 'device_distance_maximum_2', 'device_distance_std_dev_2', 'device_distance_iqr_2', 'controller_rotation_distance_median_2']

]
