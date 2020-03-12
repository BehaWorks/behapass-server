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
        self.user_ids = df["user_id"]
        self.index = faiss.IndexFlatL2(len(df.columns))
        self.scaler = StandardScaler()
        self.fit(df)

    def fit(self, df):
        self.user_ids = df["user_id"]
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

    def known_users(self):
        return self.user_ids.unique()

    def evaluate(self, data):
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
                if i["user_id"] in self.known_users():
                    y_true.append(i["user_id"])
                else:
                    y_true.append("newUser")

                if result[0]["distance"] <= config["MAXIMAL_DISTANCE"]:
                    y_pred.append(result[0]["user_id"])
                else:
                    y_pred.append("newUser")

        accuracy = accuracy_score(y_true=y_true, y_pred=y_pred)
        f1_micro = f1_score(y_true=y_true, y_pred=y_pred, average="micro")
        f1_macro = f1_score(y_true=y_true, y_pred=y_pred, average="macro")
        conf_matrix = confusion_matrix(y_true=y_true, y_pred=y_pred)

        return accuracy, f1_micro, f1_macro, conf_matrix

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
