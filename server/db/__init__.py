import json
from datetime import datetime
from typing import Any

import pymongo
import redis
from bson import ObjectId

from server import config
from server.models.user import User

instance = None


def create_db(param=None):
    global instance
    if param is not None:
        instance = param
    if instance is None:
        instance = Mongo()
    return instance


class Mongo:

    def __init__(self) -> None:
        super().__init__()
        self.mongo = pymongo.MongoClient(config["DB_HOST"])
        self.db = self.mongo[config["DB_NAME"]]
        self.user_collection = self.db["user"]
        self.movement_collection = self.db["movement"]
        self.button_collection = self.db["button"]
        self.metrix_collection = self.db["metrix"]
        self.queued_movements = RedisRegistrationQueueDict(prefix="behapass_queue_movements_")

    def get_all_movements(self):
        return self.movement_collection.find().sort("timestamp", pymongo.ASCENDING)

    def get_all_movements_by_user_id(self, user_id):
        return self.movement_collection.find({"user_id": user_id}).sort("timestamp", pymongo.ASCENDING)

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
        self.metrix_collection.insert_many(metrix)

    def get_user_ids(self):
        return self.movement_collection.distinct("user_id")

    def get_session_ids(self, user_id=None):
        if user_id is not None:
            return self.movement_collection.distinct("session_id", {"user_id": user_id})
        else:
            return self.movement_collection.distinct("session_id")

    def get_movements_by_session_id(self, session_id):
        return self.movement_collection.find({"session_id": session_id}).sort("timestamp", pymongo.ASCENDING)

    def get_buttons_by_session_id(self, session_id):
        return self.button_collection.find({"session_id": session_id}).sort("timestamp", pymongo.ASCENDING)

    def get_movements_by_session_id_and_controler_id(self, session_id, controller_id):
        return self.movement_collection.find({"session_id": session_id, "controller_id": controller_id}).sort(
            "timestamp", pymongo.ASCENDING)

    def insert_user(self, user: User):
        return self.user_collection.insert_one(user).inserted_id

    def get_user(self, user_id):
        user = self.user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise KeyError("User not found")
        return user

    def finish_user_registration(self, user_id):
        self.user_collection.update_one({"_id": ObjectId(user_id)},
                                        {"$set": {"registration_finished": datetime.utcnow().timestamp()}})


class RedisRegistrationQueueDict:

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
        self.redis = redis.Redis(host=config["REDIS_HOST"], port=config["REDIS_PORT"], decode_responses=True)

    def __delitem__(self, key: str) -> None:
        self.redis.delete(self.prefix + key)
        self.redis.delete(self.prefix + "registering_" + key)

    def append(self, key, value):
        if not self.redis.exists(self.prefix + "registering_" + key):
            raise KeyError("User not found")
        if self.redis.type(self.prefix + key) != "list":
            self.redis.delete(self.prefix + key)
        self.redis.lpush(self.prefix + key, json.dumps(value))
        self.redis.expire(self.prefix + key, config["REGISTRATION_EXPIRE"])

    def add_registering_user(self, user_id):
        self.redis.set(self.prefix + "registering_" + user_id, "registration in progress")

    def __getitem__(self, key: str) -> Any:
        if self.redis.type(self.prefix + key) == "list":
            result = [json.loads(string) for string in self.redis.lrange(self.prefix + key, 0, 200025000)]
            return result

        return self.redis.get(self.prefix + key)

    def __setitem__(self, key, value):
        self.redis.set(self.prefix + key, value)
