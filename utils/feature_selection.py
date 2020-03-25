import argparse
import os
import webbrowser
from multiprocessing.pool import Pool

import pandas as pd
import plotly.graph_objects as go
import time
from itertools import chain, combinations
from sklearn.feature_selection import SelectKBest, f_classif

from server import create_db
from server.db.test_mongo import TestMongo
from server.lookup.faiss import TestModel


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))


parser = argparse.ArgumentParser(description="Run feature selection and store model evaluation in a .csv file.")
parser.add_argument('method', type=str, choices=['k_best', 'brute_force'], metavar='METHOD', help='''feature
                                                                        selection method, choices: {%(choices)s}''')
parser.add_argument('-p', '--processes', type=int, help='Number of processes (default: %(default)s)', default=1)
args = parser.parse_args()

db = create_db(TestMongo())

df = pd.DataFrame(list(db.get_all_metrix()))
test_df = pd.DataFrame(list(db.get_all_metrix_test()))
try:
    df = df.drop("_id", axis="columns")
except KeyError:
    pass
try:
    df = df.drop("session_id", axis="columns")
except KeyError:
    pass
try:
    test_df = test_df.drop("_id", axis="columns")
except KeyError:
    pass
try:
    test_df = test_df.drop("session_id", axis="columns")
except KeyError:
    pass
df = df.dropna()
user_ids = df.pop("user_id")
test_user_ids = test_df.pop("user_id")
k = len(df.columns)
score_df = None
selector = None


def analyze(feature_indices):
    print(f"Process ID: {os.getpid()}\nF: {feature_indices}")
    feature_indices = list(feature_indices)
    df_filtered = df.iloc[:, feature_indices]
    test_df_filtered = test_df.iloc[:, feature_indices]
    model = TestModel()
    model.fit(df_filtered.join(user_ids))
    eval_result, conf_matrix = model.evaluate(test_df_filtered.join(test_user_ids), print_info=True)
    eval_result["k"] = len(feature_indices)
    eval_result["features"] = list(df_filtered.columns)

    return eval_result


if args.method == 'k_best':
    while k > 0:
        selector = SelectKBest(f_classif, k=k)
        selector.fit(df, y=user_ids)
        selected_features = selector.get_support(indices=True)
        score_entry = analyze(selected_features)
        if score_df is None:
            score_df = pd.DataFrame(columns=list(score_entry))
        score_df = score_df.append(score_entry, ignore_index=True)
        k = k - 1

    fig = go.Figure()
    for col in score_df.columns[2:]:
        fig.add_scatter(x=score_df["k"], y=score_df[col], name=col)

    try:
        fig.show(renderer="browser")
    except webbrowser.Error:
        print("No runnable browser. Not showing visualisation.")

elif args.method == 'brute_force':
    pool = Pool(processes=args.processes if args.processes > 0 else 1)
    for score_entry in pool.imap_unordered(analyze, powerset(range(len(df.columns)))):
        if score_df is None:
            score_df = pd.DataFrame(columns=list(score_entry))
        score_df = score_df.append(score_entry, ignore_index=True)

score_df.to_csv(rf'feature_selection_{args.method}_{time.strftime("%Y%m%d-%H%M%S")}.csv', index=False)

pass
