import faiss
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler

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
        results = []
        for i, d in zip(indices[0], distances[0]):
            if i > -1:
                results.append({"user_id": self.user_ids[i], "distance": float(d)})
        return results

    def evaluate(self, data, print_info=False):
        y_true = []
        y_pred = []
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
            if len(result) > 0:
                if i["user_id"] in self.user_ids:
                    y_true.append(i["user_id"])
                else:
                    y_true.append("newUser")

                if result[0]["distance"] <= config["MAXIMAL_DISTANCE"]:
                    y_pred.append(result[0]["user_id"])
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

    def process_results(self, results):
        counts = {}
        for result in results:
            if result["user_id"] not in counts:
                counts[result["user_id"]] = 0
            counts[result["user_id"]] += 1
        if len(counts) == 1:
            return results[0]["user_id"]
        counts = list(counts.items())
        counts.sort(key=lambda tup: tup[1], reverse=True)
        if counts[0][1] > counts[1][1]:
            return counts[0][0]
        previous = counts[0][1]
        finalists = {}
        for current in counts:
            if current[1] < previous:
                break
            finalists[current[0]] = 0
        for result in results:
            if result["user_id"] in finalists:
                finalists[result["user_id"]] += result["distance"]
        distances = list(finalists.items())
        distances.sort(key=lambda tup: tup[1])
        return distances[0][0]


class TestModel(FaissIndexFlatL2):

    def __init__(self) -> None:
        self.db = None
        self.user_ids = []
        self.index = None
        self.scaler = StandardScaler()
