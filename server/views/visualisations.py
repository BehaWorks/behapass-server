import pymongo
from flask import Blueprint, render_template, request

blueprint = Blueprint('visualisations', __name__)

config = {'DB_HOST': "mongodb://localhost:27017/",
          'DB_NAME': "behaworks_logger_v5",
          'DB_PORT': "",
          'URL_PREFIX': "/api"}

mongo = pymongo.MongoClient(config["DB_HOST"], )
db = mongo[config["DB_NAME"]]
movement_collection = db["test_movement"]


def get_user_ids():
    return movement_collection.distinct("user_id")


def get_session_ids(user_id=None):
    if user_id is not None:
        return movement_collection.distinct("session_id", {"user_id": user_id})
    else:
        return movement_collection.distinct("session_id")


@blueprint.route('/')
def root():
    try:
        user_id = request.args['user_id']
        return render_template('user_sessions.html',
                               user_id=user_id,
                               session_ids=get_session_ids(user_id)
                               )
    except KeyError:
        return render_template('index.html', user_ids=get_user_ids())

# @blueprint.route('/<user_id>')
# def user_sessions(user_id):
#     pass
