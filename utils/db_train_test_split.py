import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split

config = {
    "DB_HOST": "mongodb://127.0.0.1:27017/",
    "DB_NAME": "behaworks_behapass_v9",
    "DB_NAME_OTHER": "behaworks_behapass_v9"
}

mongo = pymongo.MongoClient(config["DB_HOST"])
db_original = mongo[config["DB_NAME"]]
db_other = mongo[config["DB_NAME_OTHER"]]

metrix_collection = db_original["metrix"]
df = pd.DataFrame(list(metrix_collection.find()))

user_ids = df.pop("user_id")

df.pop("_id")
df.pop("session_id")
X_train, X_test, Y_train, Y_test = train_test_split(df, user_ids, stratify=user_ids)
train = X_train.join(Y_train)
test = X_test.join(Y_test)
db_other["train"].insert_many(train.to_dict('records'))
db_other["test"].insert_many(test.to_dict('records'))
pass
