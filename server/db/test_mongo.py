from server.db import Mongo


class TestMongo(Mongo):

    def __init__(self) -> None:
        super().__init__()
        self.metrix_collection = self.db["train"]
        self.test_metrix_collection = self.db["test"]

    def get_all_metrix_test(self):
        return self.test_metrix_collection.find()
