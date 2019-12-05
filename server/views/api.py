from typing import List

import pandas as pd
from flask import Blueprint, request
from flask_restplus import Resource, Api, fields

from server import app, model
from server.db import create_db
from server.metrix import create_Metrix_Vector
from server.models.movement import Movement, HEADSET, PRIMARY_CONTROLER
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
                                                   'controller_id': fields.String(required=True),
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

lookup_result = logger.model('Lookup result', {"user_id": fields.String(required=True),
                                               "distance": fields.Float(required=True)})

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

        controller_data: List[Movement] = []
        headset_data = []
        for i in request.json["movements"]:
            m = Movement.from_dict(i)
            if m.controller_id == HEADSET:
                headset_data.append(m)
            elif m.controller_id == PRIMARY_CONTROLER:
                controller_data.append(m)

        db.insert_metrix(create_Metrix_Vector(controller_data, headset_data).to_dict())
        return {
            "status": "OK"
        }


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
    @logger.marshal_with(lookup_result)
    def post(self):
        controller_data: List[Movement] = []
        headset_data = []
        for i in request.json["movements"]:
            m = Movement.from_dict(i)
            if m.controller_id == HEADSET:
                headset_data.append(m)
            elif m.controller_id == PRIMARY_CONTROLER:
                controller_data.append(m)
        vector = create_Metrix_Vector(controller_data, headset_data)
        df = pd.DataFrame.from_records(vector.to_dict(), index=["user_id"])
        df = df.drop("user_id", axis="columns")
        df = df.drop("session_id", axis="columns")
        return model.search(df.to_numpy("float32"), 5)
