import pymongo

from server import config

instance = None


def create_db(param=None):
    global instance
    if param is not None:
        instance = param
    if instance is None:
        instance = Mongo()
    return instance


class Mongo():

    def __init__(self) -> None:
        super().__init__()
        self.mongo = pymongo.MongoClient(config["DB_HOST"])
        self.db = self.mongo[config["DB_NAME"]]
        self.movement_collection = self.db["movement"]
        self.button_collection = self.db["button"]
        self.metrix_collection = self.db["metrix"]

    def get_all_movements(self):
        return self.movement_collection.find().sort("timestamp", pymongo.ASCENDING)

    def get_all_metrix(self):
        return self.metrix_collection.find()

    def get_all_metrix_by_user_id(self, user_id):
        return self.metrix_collection.find({"user_id": user_id})

    def get_all_buttons(self):
        return self.button_collection.find().sort("timestamp", pymongo.ASCENDING)

    def insert_buttons(self, buttons):
        self.button_collection.insert_many(buttons)

    def insert_movements(self, movements):
        self.movement_collection.insert_many(movements)

    def insert_metrix(self, metrix):
        self.movement_collection.insert_many(metrix)

    def get_user_ids(self):
        return self.movement_collection.distinct("user_id")

    def remove_metrix_by_session_ids(self, session_ids):
        self.metrix_collection.delete_many({"session_id": {"$in": session_ids}})

    def get_session_ids(self, user_id=None):
        if user_id is not None:
            return self.movement_collection.distinct("session_id", {"user_id": user_id})
        else:
            return self.movement_collection.distinct("session_id")

    def get_movements_by_session_id(self, session_id):
        return self.movement_collection.find({"session_id": session_id}).sort("timestamp", pymongo.ASCENDING)

    def get_movements_by_session_id_and_controler_id(self, session_id, controller_id):
        return self.movement_collection.find({"session_id": session_id, "controller_id": controller_id}).sort("timestamp", pymongo.ASCENDING)