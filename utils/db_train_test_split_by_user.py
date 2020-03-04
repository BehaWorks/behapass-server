from random import shuffle
import pandas as pd
import pymongo

config = {
    "DB_HOST": "mongodb://host.docker.internal:27017/",
    "DB_NAME": "behaworks_logger_v6",
    "DB_NAME_OTHER": "behaworks_logger_v6_napodobnovanie_split_by_name"
}

mongo = pymongo.MongoClient(config["DB_HOST"])
db_original = mongo[config["DB_NAME"]]
db_other = mongo[config["DB_NAME_OTHER"]]

metrix_collection = db_original["metrix"]
df = pd.DataFrame(list(metrix_collection.find()))
df = df.drop("session_id", axis="columns")
user_ids = df["user_id"].unique()

shuffle(user_ids)
df_first_half_by_user_id = df.loc[df['user_id'].isin(user_ids[:int(len(user_ids)/2)])]
df_second_half_by_user_id = df.loc[df['user_id'].isin(user_ids[int(len(user_ids)/2):])]

# main_user_ids = [item for item in user_ids if item.startswith('m_')]  #for split by prefix m_
# other_user_ids = [item for item in user_ids if not item.startswith('m_')]

# df_first_half_by_user_id = df.loc[df['user_id'].isin(main_user_ids)]
# df_second_half_by_user_id = df.loc[df['user_id'].isin(other_user_ids)]

db_other["train"].insert_many(df_first_half_by_user_id.to_dict('records'))
db_other["test"].insert_many(df_second_half_by_user_id.to_dict('records'))
