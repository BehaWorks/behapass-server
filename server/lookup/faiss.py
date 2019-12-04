import faiss
import pandas as pd

from server.db import create_db


class FaissIndexFlatL2():

    def __init__(self) -> None:
        super().__init__()
        self.db = create_db()
        df = pd.DataFrame(list(self.db.get_all_metrix()))
        df = df.drop("_id", axis="columns")
        self.user_ids = df["user_id"]
        df = df.drop("user_id", axis="columns")
        df = df.drop("session_id", axis="columns")
        self.index = faiss.IndexFlatL2(len(df.columns))
        self.add(df.to_numpy("float32"))

    def add(self, vectors):
        self.index.add(vectors)

    def search(self, data, k):
        distances, indices = self.index.search(data, k)
        results = []
        for i, d in zip(indices[0], distances[0]):
            if i > -1:
                results.append({"user_id": self.user_ids[i], "distance": float(d)})
        return results
