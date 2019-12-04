import pymongo
from flask import Blueprint, request
from flask_restplus import Resource, Api, fields

from server import app
from server.models.movement import HEADSET, CONTROLLER_1, CONTROLLER_2
from utils.json import JSONEncoder

config = app.config

blueprint = Blueprint('api', __name__)
blueprint.json_encoder = JSONEncoder
logger = Api(app=blueprint, title="Logger", description="Logger API description", version="1.1",
             contact_url="https://team12-19.studenti.fiit.stuba.sk",
             doc="/documentation")

namespace = logger.namespace('logger', description='Logger APIs')

movement_record = logger.model('Movement Record', {'session_id': fields.String(required=True),
                                                   'user_id': fields.String(),
                                                   'timestamp': fields.Float(required=True),
                                                   'controller_id': fields.String(required=True,
                                                                                  enum=[HEADSET,
                                                                                        CONTROLLER_1,
                                                                                        CONTROLLER_2]),
                                                   'x': fields.Float(required=True),
                                                   'y': fields.Float(required=True),
                                                   'z': fields.Float(required=True),
                                                   'yaw': fields.Float(),
                                                   'pitch': fields.Float(),
                                                   'roll': fields.Float(),
                                                   'r_x': fields.Float(required=True),
                                                   'r_y': fields.Float(required=True),
                                                   'r_z': fields.Float(required=True),
                                                   })
button_record = logger.model('Button Record', {'session_id': fields.String(required=True),
                                               'user_id': fields.String(),
                                               'timestamp': fields.Float(required=True),
                                               'controller_id': fields.String(required=True),
                                               'trigger': fields.Float(),
                                               'trackpad_x': fields.Float(),
                                               'trackpad_y': fields.Float(),
                                               'button_pressed': fields.Integer(),
                                               'button_touched': fields.Integer(),
                                               'menu_button': fields.Boolean(),
                                               'trackpad_pressed': fields.Boolean(),
                                               'trackpad_touched': fields.Boolean(),
                                               'grip_button': fields.Boolean,
                                               })

logger_record = logger.model('Logger record', {"movements": fields.List(fields.Nested(movement_record)),
                                               "buttons": fields.List(fields.Nested(button_record))})
mongo = pymongo.MongoClient(config["DB_HOST"], )
db = mongo[config["DB_NAME"]]
test_movement_collection = db["test_movement"]
test_button_collection = db["test_button"]


@namespace.route("/")
class LoggerRecord(Resource):

    @logger.marshal_with(logger_record)
    def get(self):
        return {"movements": list(test_movement_collection.find()),
                "buttons": list(test_button_collection.find())}

    @logger.expect(logger_record)
    def post(self):
        test_movement_collection.insert_many(request.json["movements"])
        test_button_collection.insert_many(request.json["buttons"])
        return {
            "status": "OK"
        }


@namespace.route("/movements")
class MovementRecord(Resource):

    @logger.marshal_with(movement_record)
    def get(self):
        return list(test_movement_collection.find())


@namespace.route("/buttons")
class ButtonRecord(Resource):

    @logger.marshal_with(button_record)
    def get(self):
        return list(test_button_collection.find())
