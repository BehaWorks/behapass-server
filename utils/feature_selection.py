import pandas as pd
from plotly.graph_objs._figure import Figure
from sklearn.feature_selection import SelectKBest, chi2

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
model_metrics = ["accuracy", "f1-micro", "f1-macro"]
score_df = pd.DataFrame(columns=["nr. of features", "features"] + model_metrics)
feature_dict = dict()
while k > 0:
    selector = SelectKBest(chi2, k=k)
    selector.fit(df, y=user_ids)
    selected_features = selector.get_support(indices=True)
    df_filtered = df.iloc[:, selected_features]
    test_df_filtered = test_df.iloc[:, selected_features]

    model.fit(df_filtered.join(user_ids))
    scores = model.evaluate(test_df_filtered.join(test_user_ids))
    score_df.loc[len(score_df)] = [k] + [list(df_filtered.columns)] + list(scores[:-1])
    print("Number of features: %d" % k)
    print("Accuracy: %f\nF1-micro: %f\nF1-macro: %f\nConfusion matrix: \n%s\n============================" % scores)
    k = k - 1

fig = Figure()
for col in score_df.columns[2:]:
    fig.add_scatter(x=score_df["nr. of features"], y=score_df[col], name=col)

fig.show(renderer="browser")

score_df.sort_values(by=model_metrics, ascending=False, inplace=True)
print("Number of features: %d\nFeatures list: %s" % (
score_df['nr. of features'].values[0], score_df['features'].values[0]))

pass
