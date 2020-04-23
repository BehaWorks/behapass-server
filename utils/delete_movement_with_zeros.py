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

allMovements = db.get_all_movements()

allMovements = list(allMovements)
lengthOfAll = len(allMovements)

# divided of movements according to whether they are wrong
filteredMovementWithoutZeros = list(filter(lambda x: x["x"] != 0 and x["y"] != 0 and x["z"] != 0, allMovements))
filteredMovementWithZeros = list(filter(lambda x: x["x"] == 0 and x["y"] == 0 and x["z"] == 0, allMovements))

# if the non-zero motion has a pair (controller - headset) in zero movements, non-zero movement is not added either
result = []
for nonZeroElement in filteredMovementWithoutZeros:
    doNotContains = True
    for zeroElement in filteredMovementWithZeros:
        if nonZeroElement['session_id'] == zeroElement['session_id'] and nonZeroElement['timestamp'] == zeroElement['timestamp']:
            doNotContains = False
    if doNotContains:
        result.append(nonZeroElement)

# If the filtered session has only one movement, it will also be deleted
groupedMovements = (pd.DataFrame(result)
                    .groupby(['session_id', 'controller_id']))

toDeleteSeassionID = []
for element in groupedMovements:
    if element[1].shape[0] == 1:
        toDeleteSeassionID.append(element[0][0])

toDeleteSeassionID = list(set(toDeleteSeassionID))

finalresult = []
for movements in result:
    doNotContains = True
    for seasionid in toDeleteSeassionID:
        if movements['session_id'] == seasionid:
            doNotContains = False

    if doNotContains:
        finalresult.append(movements)

db_other["movements"].insert_many(pd.DataFrame(finalresult).to_dict('records'))

print("deleted ", len(finalresult), " samples from", lengthOfAll)
