from server import create_app

app = create_app()
# app.config.from_pyfile('server/config/config.py')

config = app.config

# @app.route("/api/visualisation")
# def visualisation():
#     return render_template("users_form.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
