import pymongo

from server import config


def create_db():
    return Mongo()


class Mongo():

    def __init__(self) -> None:
        super().__init__()
        self.mongo = pymongo.MongoClient(config["DB_HOST"])
        self.db = self.mongo[config["DB_NAME"]]
        self.test_movement_collection = self.db["test_movement"]
        self.test_button_collection = self.db["test_button"]
        self.test_metrix_collection = self.db["test_metrix"]

    def get_all_movements(self):
        return self.test_movement_collection.find()

    def get_all_metrix(self):
        return self.test_metrix_collection.find()

    def get_all_buttons(self):
        return self.test_button_collection.find()

    def insert_buttons(self, buttons):
        self.test_button_collection.insert_many(buttons)

    def insert_movements(self, movements):
        self.test_movement_collection.insert_many(movements)

    def insert_metrix(self, metrix):
        self.test_movement_collection.insert_many(metrix)

    def get_user_ids(self):
        return self.test_movement_collection.distinct("user_id")

    def get_session_ids(self, user_id=None):
        if user_id is not None:
            return self.test_movement_collection.distinct("session_id", {"user_id": user_id})
        else:
            return self.test_movement_collection.distinct("session_id")

    def get_movements_by_session_id(self, session_id):
        return self.test_movement_collection.find({"session_id": session_id})
