import pandas as pd
import plotly.graph_objs as go
import plotly.offline as po
import pymongo
from flask import Blueprint, render_template, request

from server import config
from server.metrix import Result, Metric
from server.metrix.acceleration import Acceleration
from server.metrix.velocity import Velocity
from server.models.movement import Movement

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


def create_plot3d(df):
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


def create_metric_plot(metric: Result, title):
    fig = go.Figure(
        data=[go.Scatter(x=list(range(len(metric.data))), y=metric.data)],
        layout=go.Layout(
            title=go.layout.Title(text=title)
        )
    )
    output = po.plot(fig, output_type='div')
    return output


def create_metric_boxplot(data, title):
    fig = go.Figure(layout=go.Layout(
        title=go.layout.Title(text=title),
        showlegend=False
    ))
    for i in data:
        fig.add_trace(go.Box(y=data[i], x=[i] * len(data[i]), boxpoints='all'))
    output = po.plot(fig, output_type='div')
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
        df = pd.DataFrame(list(movement_collection.find({"session_id": session_id})))
        data = []
        for i in df.to_dict('records'):
            data.append(Movement.from_dict(i))
        return render_template('graph.html',
                               graph3d_div=create_plot3d(df),
                               velocity_div=create_metric_plot(Velocity().calculate(data), "Velocity"),
                               acceleration_div=create_metric_plot(Acceleration().calculate(data), "Acceleration"),
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


@blueprint.route('/metrix')
def metrix():
    v_averages, v_medians = compute_metric(Velocity())
    a_averages, a_medians = compute_metric(Acceleration())
    return render_template('metrix.html', graphs=[create_metric_boxplot(v_averages, "Velocity averages"),
                                                  create_metric_boxplot(v_medians, "Velocity medians"),
                                                  create_metric_boxplot(a_averages, "Acceleration averages"),
                                                  create_metric_boxplot(a_medians, "Acceleration medians")])


def compute_metric(instance: Metric):
    averages = {}
    medians = {}
    for user_id in get_user_ids():
        averages[user_id] = []
        medians[user_id] = []
        for session_id in get_session_ids(user_id):
            movements = []
            for record in movement_collection.find({"session_id": session_id}):
                try:
                    movements.append(Movement.from_dict(record))
                except KeyError:
                    pass
            if movements:
                result = instance.calculate(movements)
                averages[user_id].append(result.average)
                medians[user_id].append(result.median)
    return averages, medians
