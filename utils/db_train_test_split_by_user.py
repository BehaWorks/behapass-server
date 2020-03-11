from random import shuffle
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
import re

config = {
    "DB_HOST": "mongodb://host.docker.internal:27017/",
    "DB_NAME": "behaworks_logger_v8",
    "DB_NAME_OTHER": "behaworks_logger_v8",
    "RATIO_OF_EXISTING_USERS": 70,
    "NORMAL_SPLIT": "y"
}

mongo = pymongo.MongoClient(config["DB_HOST"])
db_original = mongo[config["DB_NAME"]]
db_other = mongo[config["DB_NAME_OTHER"]]

metrix_collection = db_original["metrix"]
df = pd.DataFrame(list(metrix_collection.find()))
df = df.drop("session_id", axis="columns")
user_ids = df["user_id"].unique()

if config["NORMAL_SPLIT"] == 'y':
    shuffle(user_ids)
    df_first_part_by_user_id = df.loc[df['user_id'].isin(user_ids[:int(len(user_ids) / 100 * (config["RATIO_OF_EXISTING_USERS"]))])]
    df_second_part_by_user_id = df.loc[df['user_id'].isin(user_ids[int(len(user_ids) / 100 * (config["RATIO_OF_EXISTING_USERS"])):])]

    user_ids = df_first_part_by_user_id.pop("user_id")

    df_first_part_by_user_id.pop("_id")
    X_train, X_test, Y_train, Y_test = train_test_split(df_first_part_by_user_id, user_ids, stratify=user_ids)
    train = X_train.join(Y_train)
    test = X_test.join(Y_test)

    db_other["train"].insert_many(train.to_dict('records'))
    db_other["test"].insert_many(test.to_dict('records'))
    db_other["test"].insert_many(df_second_part_by_user_id.to_dict('records'))

else:
    imitated_user_ids = [item for item in user_ids if re.match(r'^m.*_', item)]  # for split by prefix m_
    imitating_user_ids = [item for item in user_ids if not re.match(r'^m.*_', item)]

    df_imitated_user_id = df.loc[df['user_id'].isin(imitated_user_ids)]
    df_imitating_user_id = df.loc[df['user_id'].isin(imitating_user_ids)]
    db_other["train"].insert_many(df_imitated_user_id.to_dict('records'))
    db_other["test"].insert_many(df_imitating_user_id.to_dict('records'))
