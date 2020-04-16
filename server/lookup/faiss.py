import faiss
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from functools import reduce

from server.db import create_db, config


class FaissIndexFlatL2:

    def __init__(self) -> None:
        super().__init__()
        self.db = create_db()
        df = pd.DataFrame(list(self.db.get_all_metrix()))
        self.user_ids = list(df["user_id"])
        self.index = None
        self.scaler = StandardScaler()
        self.fit(df)

    def fit(self, df):
        self.user_ids = list(df["user_id"])
        df = df.drop("user_id", axis="columns")
        try:
            df = df.drop("_id", axis="columns")
        except KeyError:
            pass
        try:
            df = df.drop("session_id", axis="columns")
        except KeyError:
            pass
        self.index = faiss.IndexFlatL2(len(df.columns))
        self.add(self.scaler.fit_transform(df.to_numpy("float32")))

    def add(self, vectors):
        self.index.add(np.ascontiguousarray(vectors))

    def search(self, data, k):
        distances, indices = self.index.search(np.ascontiguousarray(self.scaler.transform(data)), k)
        results = pd.DataFrame(columns=["user_id", "distance"])
        for i, d in zip(indices[0], distances[0]):
            if i > -1 and d <= config["MAXIMAL_DISTANCE"]:
                results = results.append({"user_id": self.user_ids[i], "distance": float(d)}, ignore_index=True)
        results.sort_values(by=['distance'])
        if not len(results):
            return None
        if results["user_id"][0] == results["user_id"].mode()[0] or results["user_id"].nunique() == len(results):
            return results["user_id"][0]
        results["distance"] = results["distance"].astype(float)
        grouped = results.groupby('user_id').agg(inverse_sum=('distance', lambda series: np.sum(1/series)))
        return grouped.idxmax()[0]

    def evaluate(self, data, print_info=False):
        y_true = []
        y_pred = []
        df = pd.DataFrame()
        for _, i in data.iterrows():

            df = pd.DataFrame(i.to_dict(), index=["user_id"])
            try:
                df = df.drop("_id", axis="columns")
            except KeyError:
                pass
            try:
                df = df.drop("user_id", axis="columns")
            except KeyError:
                pass
            result = self.search(df.to_numpy("float32"), config["NEIGHBOURS"])
            if i["user_id"] in self.user_ids:
                y_true.append(i["user_id"])
            else:
                y_true.append("newUser")
            if result:
                y_pred.append(result)
            else:
                y_pred.append("newUser")

        model_metrics = {
            "accuracy": accuracy_score(y_true=y_true, y_pred=y_pred),
            "f1_micro": f1_score(y_true=y_true, y_pred=y_pred, average="micro"),
            "f1_macro": f1_score(y_true=y_true, y_pred=y_pred, average="macro"),
        }
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

        model_metrics["TPR"] = TP / (TP + FN)
        model_metrics["FPR"] = FP / (FP + TN)
        model_metrics["TNR"] = TN / (FP + TN)
        model_metrics["FNR"] = 1 - model_metrics["TPR"]

        if print_info:
            print("Nr. of features: %s" % len(df.columns))
            print("Accuracy: %s" % model_metrics["accuracy"])
            print("F1_micro: %s" % model_metrics["f1_micro"])
            print("F1_macro: %s" % model_metrics["f1_macro"])
            print("True positive rate: %s" % model_metrics["TPR"])
            print("True negative rate: %s" % model_metrics["TNR"])
            print("False positive rate: %s" % model_metrics["FPR"])
            print("False negative rate: %s" % model_metrics["FNR"])
            print("Confusion matrix: \n%s" % matrix)
            print("Binary matrix: \n%s\n======================" % binary_matrix)

        return model_metrics, matrix


class TestModel(FaissIndexFlatL2):

    # noinspection PyMissingConstructor
    def __init__(self) -> None:
        self.db = None
        self.user_ids = []
        self.index = None
        self.scaler = StandardScaler()
