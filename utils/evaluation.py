from server.config import config
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

features = config.FEATURE_SELECTION;
features = features + ['user_id'];
model.fit(df.loc[:, features])
model.evaluate(df_test.loc[:, features], True)

