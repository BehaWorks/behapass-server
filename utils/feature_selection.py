import webbrowser

import pandas as pd
import plotly.graph_objects as go
from sklearn.feature_selection import SelectKBest, f_classif

from server import create_db
from server.db.test_mongo import TestMongo
from server.views.api import get_model

db = create_db(TestMongo())
model = get_model()

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
model_metrics = []
while k > 0:
    selector = SelectKBest(f_classif, k=k)
    selector.fit(df, y=user_ids)
    selected_features = selector.get_support(indices=True)
    df_filtered = df.iloc[:, selected_features]
    test_df_filtered = test_df.iloc[:, selected_features]

    model.fit(df_filtered.join(user_ids))
    eval_result, conf_matrix = model.evaluate(test_df_filtered.join(test_user_ids), print_info=True)
    if score_df is None:
        score_df = pd.DataFrame(columns=["k", "features"] + list(eval_result))
        model_metrics = list(eval_result)
    eval_result["k"] = k
    eval_result["features"] = list(df_filtered.columns)
    score_df = score_df.append(eval_result, ignore_index=True)
    k = k - 1

fig = go.Figure()
for col in score_df.columns[2:]:
    fig.add_scatter(x=score_df["k"], y=score_df[col], name=col)

try:
    fig.show(renderer="browser")
except webbrowser.Error:
    print("No runnable browser. Not showing visualisation.")

score_df.sort_values(by=model_metrics, ascending=False, inplace=True)
for col in score_df.columns:
    print(f"{col}: {score_df[col].values[0]}")

pass
