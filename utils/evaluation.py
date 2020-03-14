import pandas as pd
from server import config
from server.config.config import MAXIMAL_DISTANCE
from server.db.test_mongo import TestMongo
from server.views.api import get_model
from server.db import create_db
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

db = create_db(TestMongo())
model = get_model()
y_true = []
y_pred = []

user_ids_from_train = db.metrix_collection.distinct("user_id")
print(user_ids_from_train)

for i in db.get_all_metrix_test():
    df = pd.DataFrame(i, index=["user_id"])
    df = df.drop("_id", axis="columns")
    df = df.drop("user_id", axis="columns")
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


accuracy = accuracy_score(y_true=y_true, y_pred=y_pred)
f1_mikro = f1_score(y_true=y_true, y_pred=y_pred, average="micro")
f1_makro = f1_score(y_true=y_true, y_pred=y_pred, average="macro")
matrix = confusion_matrix(y_true=y_true, y_pred=y_pred)

for (i, true) in enumerate(y_true):
    if true != "newUser":
        y_true[i] = "existingUser"
    if y_pred[i] != "newUser":
        y_pred[i] = "existingUser"

binary_matrix = confusion_matrix(y_true=y_true, y_pred=y_pred)
TP = binary_matrix[0][0]
FN = binary_matrix[0][1]
FP = binary_matrix[1][0]
TN = binary_matrix[1][1]

TPR = TP/(TP+FN)
FPR = FP/(FP+TN)
TNR = TN/(FP+TN)
FNR = 1 - TPR

print("accuracy: %s" % accuracy)
print("f1_mikro: %s" % f1_mikro)
print("f1_makro: %s" % f1_makro)
print("True positive rate: %s" % TPR)
print("True negative rate: %s" % TNR)
print("False positive rate: %s" % FPR)
print("False negative rate: %s" % FNR)
print("matrix: \n%s" % matrix)
print("binary matrix: \n%s" % binary_matrix)
