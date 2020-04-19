import argparse
import time
from itertools import combinations, repeat
from multiprocessing import Pool
from random import shuffle

import scipy.special
import tqdm
from sklearn.model_selection import train_test_split

from server.db import create_db
from server.db.test_mongo import TestMongo
from server.lookup.faiss import TestModel
from utils.helpers import append_score

UNKNOWN_USERS_RATIO = 0.3


def cv_run(arguments):
    # print(unknown_users, df_all.shape, len(selected_features), sep='\n')
    unknown_users, df_all, selected_features = arguments
    df_unknown = df_all.loc[df_all['user_id'].isin(unknown_users)]
    df_known = df_all.loc[~df_all['user_id'].isin(unknown_users)]
    train, test = train_test_split(df_known, stratify=df_known['user_id'])
    test = test.append(df_unknown)
    model = TestModel()
    model.fit(train[selected_features])
    return model.evaluate(test[selected_features], args.verbose)[0]


def cross_validation(df_all, selected_features=None):
    user_ids = df_all['user_id'].unique()
    if not selected_features:
        selected_features = list(df_all.columns)
    shuffle(user_ids)
    scores = None

    pool = Pool(args.processes)
    for score in tqdm.tqdm(
            pool.imap_unordered(cv_run, zip(combinations(user_ids, int(len(user_ids) * UNKNOWN_USERS_RATIO)),
                                            repeat(df_all),
                                            repeat(selected_features))),
            total=scipy.special.comb(len(user_ids), int(len(user_ids) * UNKNOWN_USERS_RATIO)), ascii=True):
        scores = append_score(scores, score)

    return scores


parser = argparse.ArgumentParser(description="Run model cross-validation.")
parser.add_argument('-p', '--processes', type=int, help='Number of processes (default: %(default)s)', default=1)
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-q', '--quick', action='store_true',
                    help="Don't run cross-validation, just evaluate the model once")
parser.add_argument('--no_save', action='store_true', help="Don't save cross-validation results")
args = parser.parse_args()

db = create_db(TestMongo())
df, df_test = db.get_clean_train_test()

features = ['user_id', 'velocity_average', 'velocity_median', 'velocity_minimum', 'velocity_maximum',
            'velocity_std_dev', 'velocity_iqr', 'velocity_average_0', 'velocity_median_0', 'velocity_minimum_0',
            'velocity_maximum_0', 'velocity_std_dev_0', 'velocity_iqr_0', 'velocity_average_1', 'velocity_median_1',
            'velocity_minimum_1', 'velocity_maximum_1', 'velocity_std_dev_1', 'velocity_iqr_1', 'velocity_average_2',
            'velocity_median_2', 'velocity_minimum_2', 'velocity_maximum_2', 'velocity_std_dev_2', 'velocity_iqr_2',
            'angular_velocity_average', 'angular_velocity_median', 'angular_velocity_minimum',
            'angular_velocity_maximum', 'angular_velocity_std_dev', 'angular_velocity_iqr',
            'angular_velocity_average_0', 'angular_velocity_median_0', 'angular_velocity_minimum_0',
            'angular_velocity_maximum_0', 'angular_velocity_std_dev_0', 'angular_velocity_iqr_0',
            'angular_velocity_average_1', 'angular_velocity_median_1', 'angular_velocity_minimum_1',
            'angular_velocity_maximum_1', 'angular_velocity_std_dev_1', 'angular_velocity_iqr_1',
            'angular_velocity_average_2', 'angular_velocity_median_2', 'angular_velocity_minimum_2',
            'angular_velocity_maximum_2', 'angular_velocity_std_dev_2', 'angular_velocity_iqr_2',
            'device_distance_average', 'device_distance_median', 'device_distance_minimum', 'device_distance_maximum',
            'device_distance_std_dev', 'device_distance_iqr', 'device_distance_average_0', 'device_distance_median_0',
            'device_distance_minimum_0', 'device_distance_maximum_0', 'device_distance_std_dev_0',
            'device_distance_iqr_0', 'device_distance_average_1', 'device_distance_median_1',
            'device_distance_minimum_1', 'device_distance_maximum_1', 'device_distance_std_dev_1',
            'device_distance_iqr_1', 'device_distance_average_2', 'device_distance_median_2',
            'device_distance_minimum_2', 'device_distance_maximum_2', 'device_distance_std_dev_2',
            'device_distance_iqr_2']
# features = config.FEATURE_SELECTION + ['user_id']

if args.quick:
    m = TestModel()
    m.fit(df[features])
    m.evaluate(df_test[features], True)
else:
    score_df = cross_validation(df.append(df_test), selected_features=features)
    if not args.no_save:
        score_df.to_csv(rf'cv_evaluation_{time.strftime("%Y%m%d-%H%M%S")}.csv', index=False)
    print(score_df.mean().rename('Mean'))
