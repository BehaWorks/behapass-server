from datetime import datetime
from typing import List

from flask import Blueprint, request
from flask_restplus import Resource, Api, fields, marshal

from server import app
from server.lookup.faiss import *
from server.lookup.preprocessing import remove_outliers
from server.metrix import create_metrix_vector
from server.models.movement import Movement, HEADSET, CONTROLLER_1, CONTROLLER_2
from server.models.user import User
from utils.json_encoder import JSONEncoder

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
                                               'grip_button': fields.Boolean(),
                                               })

logger_record = logger.model('Logger record', {"movements": fields.List(fields.Nested(movement_record)),
                                               "buttons": fields.List(fields.Nested(button_record))})

user_record = logger.model('User record', {"data": fields.String()})

lookup_result = logger.model('Lookup result', {"user_id": fields.String(required=True)})
not_found = logger.model('Bad request response', {"message": fields.String(required=True)})

model = None

queued_movements = {}

def get_model():
    global model
    if model is None:
        model = FaissIndexFlatL2()
    return model


db = create_db()

@namespace.route("/")
class LoggerRecord(Resource):

    @logger.marshal_with(logger_record)
    def get(self):
        return {"movements": list(db.get_all_movements()),
                "buttons": list(db.get_all_buttons())}

    @logger.expect(logger_record)
    def post(self):
        db.insert_movements(request.json["movements"])
        db.insert_buttons(request.json["buttons"])
        db.insert_metrix(create_metrix_vector(*split_movements(request.json["movements"])))
        return {
            "status": "OK"
        }


@namespace.route("/user")
class UserRecord(Resource):

    @logger.expect(user_record)
    def post(self):
        user = request.json
        user["registration_started"] = datetime.utcnow().timestamp()
        user["registration_finished"] = None
        user = User.from_dict(user)
        data = user.__dict__
        if data["_id"] is None:
            del (data["_id"])
        id = str(db.insert_user(data))
        queued_movements[id] = []
        return {"id": id}


@namespace.route('/user/<user_id>/movements', methods=['POST'])
class RegisterUser(Resource):
    @logger.expect(movement_record)
    def post(self, user_id):
        try:
            queued_movements[user_id].append(request.json)
        except KeyError:
            return namespace.abort(404, 'Unknown user. First create user using /user to get user_id')

        from server.config.config import MINIMUM_RECORDS
        if len(queued_movements[user_id]) < MINIMUM_RECORDS:
            return {"message": "Send more movements for succesfull registration",
                    "remaining": MINIMUM_RECORDS - len(queued_movements[user_id])}, 202

        metrix = map(lambda movements: create_metrix_vector(*split_movements(movements)), queued_movements[user_id])
        df = remove_outliers(metrix)
        if len(df) < MINIMUM_RECORDS:
            return {"message": "Send more movements for succesfull registration",
                    "remaining": MINIMUM_RECORDS - len(df)}, 202

        db.insert_metrix(df)
        del (queued_movements[user_id])
        return {"message": "OK"}


@namespace.route("/movements")
class MovementRecord(Resource):

    @logger.marshal_with(movement_record)
    def get(self):
        return list(db.get_all_movements())


@namespace.route("/buttons")
class ButtonRecord(Resource):

    @logger.marshal_with(button_record)
    def get(self):
        return list(db.get_all_buttons())


@namespace.route("/lookup")
class Lookup(Resource):

    @logger.expect(logger_record)
    @namespace.response(code=200, model=lookup_result, description='Success')
    @namespace.response(code=404, model=not_found, description='Not Found')
    def post(self):
        vector = create_metrix_vector(*split_movements(request.json["movements"]))
        df = pd.DataFrame(vector.to_dict(), index=["user_id"])
        df = df.drop("user_id", axis="columns")
        df = df.drop("session_id", axis="columns")
        result = get_model().search(df.to_numpy("float32"), config["NEIGHBOURS"])
        if not result:
            return {"message": "No users were found."}, 404
        return marshal(result, lookup_result)


def split_movements(collection):
    controller_data: List[Movement] = []
    headset_data = []
    for i in collection:
        m = Movement.from_dict(i)
        if m.controller_id == HEADSET:
            headset_data.append(m)
        elif m.controller_id == CONTROLLER_1:
            controller_data.append(m)
    return controller_data, headset_data
