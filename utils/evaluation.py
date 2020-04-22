import argparse
import time
from itertools import combinations, repeat
from multiprocessing import Pool
from random import shuffle

import scipy.special
import tqdm
from sklearn.model_selection import train_test_split

from server.config import config
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
parser.add_argument('-i', '--iterations', type=int, help='How many times to run the validation (default: %(default)s)',
                    default=1)
args = parser.parse_args()

db = create_db(TestMongo())
df, df_test = db.get_clean_train_test()

features = config.FEATURE_SELECTION + ['user_id']

if args.quick:
    m = TestModel()
    m.fit(df[features])
    m.evaluate(df_test[features], True)
else:
    score_df = None
    for i in tqdm.tqdm(range(args.iterations), ascii=True):
        if score_df is not None:
            score_df = score_df.append(cross_validation(df.append(df_test), selected_features=features))
        else:
            score_df = cross_validation(df.append(df_test), selected_features=features)
    if not args.no_save:
        score_df.to_csv(rf'cv_evaluation_{time.strftime("%Y%m%d-%H%M%S")}.csv', index=False)
    print(score_df.mean().rename('Mean'))
