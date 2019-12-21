from server import create_db
from server.metrix import create_metrix_vector
from server.views.api import split_movements

db = create_db()

new_db = db.mongo["behaworks_logger_v8"]
# movement_collection = new_db["movement"]
# button_collection = new_db["button"]
metrix_collection = new_db["metrix"]
# for movement in db.get_all_movements():
#     movement_collection.insert_one(movement)
# for button in db.get_all_buttons():
#     button_collection.insert_one(button)
for session_id in db.get_session_ids():
    try:
        metrix_collection.insert_one(
            create_metrix_vector(*split_movements(db.get_movements_by_session_id(session_id))).to_dict())
    except ValueError:
        print("ZLE: " + session_id)
