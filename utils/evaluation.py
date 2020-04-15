from server.db import create_db
from server.db.test_mongo import TestMongo
from server.views.api import get_model
import pandas as pd

db = create_db(TestMongo())
model = get_model()
df = pd.DataFrame(list(db.get_all_metrix()))
df_test = pd.DataFrame(list(db.get_all_metrix_test()))
try:
    df = df.drop("_id", axis="columns")
except KeyError:
    pass
try:
    df = df.drop("session_id", axis="columns")
except KeyError:
    pass
try:
    df_test = df_test.drop("_id", axis="columns")
except KeyError:
    pass
try:
    df_test = df_test.drop("session_id", axis="columns")
except KeyError:
    pass
features = ['user_id', 'velocity_average', 'velocity_median', 'velocity_minimum', 'velocity_maximum', 'velocity_std_dev', 'velocity_iqr', 'velocity_average_0', 'velocity_median_0', 'velocity_minimum_0', 'velocity_maximum_0', 'velocity_std_dev_0', 'velocity_iqr_0', 'velocity_average_1', 'velocity_median_1', 'velocity_minimum_1', 'velocity_maximum_1', 'velocity_std_dev_1', 'velocity_iqr_1', 'velocity_average_2', 'velocity_median_2', 'velocity_minimum_2', 'velocity_maximum_2', 'velocity_std_dev_2', 'velocity_iqr_2', 'angular_velocity_average', 'angular_velocity_median', 'angular_velocity_minimum', 'angular_velocity_maximum', 'angular_velocity_std_dev', 'angular_velocity_iqr', 'angular_velocity_average_0', 'angular_velocity_median_0', 'angular_velocity_minimum_0', 'angular_velocity_maximum_0', 'angular_velocity_std_dev_0', 'angular_velocity_iqr_0', 'angular_velocity_average_1', 'angular_velocity_median_1', 'angular_velocity_minimum_1', 'angular_velocity_maximum_1', 'angular_velocity_std_dev_1', 'angular_velocity_iqr_1', 'angular_velocity_average_2', 'angular_velocity_median_2', 'angular_velocity_minimum_2', 'angular_velocity_maximum_2', 'angular_velocity_std_dev_2', 'angular_velocity_iqr_2', 'device_distance_average', 'device_distance_median', 'device_distance_minimum', 'device_distance_maximum', 'device_distance_std_dev', 'device_distance_iqr', 'device_distance_average_0', 'device_distance_median_0', 'device_distance_minimum_0', 'device_distance_maximum_0', 'device_distance_std_dev_0', 'device_distance_iqr_0', 'device_distance_average_1', 'device_distance_median_1', 'device_distance_minimum_1', 'device_distance_maximum_1', 'device_distance_std_dev_1', 'device_distance_iqr_1', 'device_distance_average_2', 'device_distance_median_2', 'device_distance_minimum_2', 'device_distance_maximum_2', 'device_distance_std_dev_2', 'device_distance_iqr_2']
model.fit(df.loc[:, features])
model.evaluate(df_test.loc[:, features], True)

