import pandas as pd

from server.db import Mongo


class TestMongo(Mongo):

    def __init__(self) -> None:
        super().__init__()
        self.metrix_collection = self.db["train"]
        self.test_metrix_collection = self.db["test"]

    def get_all_metrix_test(self):
        return self.test_metrix_collection.find()

    def get_user_ids(self):
        return self.metrix_collection.distinct("user_id")

    def get_clean_train_test(self):
        df = pd.DataFrame(list(self.get_all_metrix()))
        df_test = pd.DataFrame(list(self.get_all_metrix_test()))
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
        return df, df_test
