import pandas as pd
import numpy as np
from server import config
from server.config.config import MAXIMAL_DISTANCE
from server.db.test_mongo import TestMongo
from server.views.api import get_model
from server.db import create_db
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

db = create_db(TestMongo())
model = get_model()
DISTANCE = 20
y_true = []
y_pred = []
bad_distances = []
distances = []

db_train = create_db()

user_ids_from_train = db_train.get_user_ids_from_train()
print(user_ids_from_train)
for i in db.get_all_metrix_test():
    df = pd.DataFrame(i, index=["user_id"])
    df = df.drop("_id", axis="columns")
    df = df.drop("user_id", axis="columns")
    #df = df.drop("session_id", axis="columns")
    result = model.search(df.to_numpy("float32"), config["NEIGHBOURS"])
    if len(result) > 0:
        if i["user_id"] in user_ids_from_train:
            y_true.append(i["user_id"])
        else:
            y_true.append("newUser")

        if result[0]["distance"] <= MAXIMAL_DISTANCE:
            y_pred.append(result[0]["user_id"])
        else:
            y_pred.append("newUser")


a_kuracy = accuracy_score(y_true=y_true, y_pred=y_pred)
efjedna_mikro = f1_score(y_true=y_true, y_pred=y_pred, average="micro")
efjedna_makro = f1_score(y_true=y_true, y_pred=y_pred, average="macro")
matica = confusion_matrix(y_true=y_true, y_pred=y_pred)

print("a_kuracy: %s" % a_kuracy)
print("efjedna_mikro: %s" % efjedna_mikro)
print("efjedna_makro: %s" % efjedna_makro)
print("metrix: \n%s" % matica)

