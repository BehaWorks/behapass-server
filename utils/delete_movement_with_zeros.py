from server import create_db
import pandas as pd
import pymongo

config = {
    "DB_HOST": "mongodb://host.docker.internal:27017/",
    "DB_NAME_OTHER": "behaworks_logger_v10",
}

mongo = pymongo.MongoClient(config["DB_HOST"])
db_other = mongo[config["DB_NAME_OTHER"]]

db = create_db()

all_movements = db.get_all_movements()

all_movements = list(all_movements)
length_of_all = len(all_movements)

# divided of movements according to whether they are wrong
filtered_movement_without_zeros = list(filter(lambda x: x["x"] != 0 and x["y"] != 0 and x["z"] != 0, all_movements))
filtered_movement_with_zeros = list(filter(lambda x: x["x"] == 0 and x["y"] == 0 and x["z"] == 0, all_movements))

# if the non-zero motion has a pair (controller - headset) in zero movements, non-zero movement is not added either
result = []
for non_zero_element in filtered_movement_without_zeros:
    do_not_contains = True
    for zero_element in filtered_movement_with_zeros:
        if non_zero_element['session_id'] == zero_element['session_id'] and non_zero_element['timestamp'] == zero_element['timestamp']:
            do_not_contains = False
    if do_not_contains:
        result.append(non_zero_element)

# If the filtered session has only one movement, it will also be deleted
grouped_movements = (pd.DataFrame(result).groupby(['session_id', 'controller_id']))

to_delete_session_id = []
for element in grouped_movements:
    if element[1].shape[0] == 1:
        to_delete_session_id.append(element[0][0])

to_delete_session_id = list(set(to_delete_session_id))

final_result = []
for movements in result:
    do_not_contains = True
    for session_id in to_delete_session_id:
        if movements['session_id'] == session_id:
            do_not_contains = False

    if do_not_contains:
        final_result.append(movements)

db_other["movements"].insert_many(pd.DataFrame(final_result).to_dict('records'))

print("deleted ", len(final_result), " samples from", length_of_all)
