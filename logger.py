from flask import Blueprint
from flask import Flask

bp = Blueprint('api', __name__, template_folder='templates')


@bp.route("/")
def index_page():
    return "Hello World!"


@bp.route("/data/")
def about_page():
    return "Vitaj!"


app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/api/')


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
