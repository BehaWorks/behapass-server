from pprint import pprint

import pandas as pd
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
selector = SelectKBest(chi2, k=20)
# print("Number of columns: %d" % len(df.columns))
selector.fit(df, y=user_ids)
selected_features = selector.get_support(indices=True)
df_filtered = df.iloc[:, selected_features]
test_df_filtered = test_df.iloc[:, selected_features]
model.fit(df_filtered.join(user_ids))
pprint(model.evaluate(test_df_filtered.join(test_user_ids)))
# print("Number of columns: %d" % len(df.columns))

pass
