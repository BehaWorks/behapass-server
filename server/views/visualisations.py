import pandas as pd
import plotly.graph_objs as go
import plotly.offline as po
import pymongo
from flask import Blueprint, render_template, request

from server import config

Z_GRAPH_RANGE = [-2, 2]
X_GRAPH_RANGE = [-2, 2]

blueprint = Blueprint('visualisations', __name__)


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


def create_plot(query):
    df = pd.DataFrame(list(movement_collection.find(query)))
    max_height = max(df['y'])
    splot_anim = [create_scatter3d(df), create_scatter3d(df)]
    frames = [go.Frame(
        data=go.Scatter3d(x=df['x'][:k], y=df['y'][:k], z=df['z'][:k],
                          mode="lines", line=dict(width=8, color="red"), opacity=1
                          )
    ) for k in range(len(df['timestamp']))]

    layout_anim = go.Layout(
        width=1024,
        height=1024,
        scene=dict(
            camera=dict(up=dict(x=0, y=1, z=0)),
            xaxis=dict(title='X', range=X_GRAPH_RANGE),
            yaxis=dict(title='Height', range=[0, max_height + 0.25]),
            zaxis=dict(title='Z', range=Z_GRAPH_RANGE)),
        updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None])])]
    )

    fig_anim = go.Figure(data=splot_anim, layout=layout_anim, frames=frames)
    frame_duration = df['timestamp'].tolist()[-1] / len(df['timestamp'])
    output = po.plot(fig_anim, output_type='div', animation_opts=dict(frame=dict(duration=frame_duration)))
    return output


def create_scatter3d(df):
    return go.Scatter3d(x=df['x'], y=df['y'], z=df['z'],
                        mode="lines", line=dict(width=2, color="blue"), opacity=1)


@blueprint.route('/')
def root():
    return render_template('users_form.html', user_ids=get_user_ids())


@blueprint.route('/v')
def user_sessions():
    user_id = None
    session_id = None

    try:
        user_id = request.args['user_id']
    except KeyError:
        pass
    try:
        session_id = request.args['session_id']
    except KeyError:
        pass

    if session_id is not None:
        return render_template('graph.html',
                               graph_div=create_plot({"session_id": session_id}),
                               session_id=session_id,
                               user_id=user_id,
                               session_ids=get_session_ids(user_id),
                               user_ids=get_user_ids(),
                               title="%s - %s" % (user_id, session_id)
                               )

    if user_id is not None:
        return render_template('sessions_form.html',
                               user_id=user_id,
                               session_ids=get_session_ids(user_id),
                               user_ids=get_user_ids(),
                               title=user_id + ' sessions'
                               )
