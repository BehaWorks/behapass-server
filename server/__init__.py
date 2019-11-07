from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config/config.py')
config = app.config

from server.views import api
from server.views import visualisations


def register_blueprints(app):
    app.register_blueprint(api.blueprint, url_prefix='/api')
    app.register_blueprint(visualisations.blueprint, url_prefix='/visualisations')


register_blueprints(app)
