import pandas as pd
import plotly.graph_objs as go
import plotly.offline as po
from flask import Blueprint, render_template, request
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

from server.db import create_db
from server.metrix.acceleration import Acceleration
from server.metrix.jerk import Jerk
from server.metrix.metric import Metric
from server.metrix.result import Result
from server.metrix.velocity import Velocity
from server.models.movement import Movement, CONTROLLER_1, HEADSET

Z_GRAPH_RANGE = [-2, 2]
X_GRAPH_RANGE = [-2, 2]
METRIX = [Acceleration(), Velocity(), Jerk()]

blueprint = Blueprint('visualisations', __name__)

db = create_db()


def get_user_ids():
    return db.get_user_ids()


def get_session_ids(user_id=None):
    return db.get_session_ids(user_id)


def get_all_metrix():
    return db.get_all_metrix()


def reduce_dimensionality(data, reducer, normalize=True):
    data = data.dropna()
    data.pop('_id')
    data.pop('session_id')
    user_ids = data.pop('user_id')
    if normalize:
        data = StandardScaler().fit_transform(data)
    reduced = pd.DataFrame(reducer.fit_transform(data))
    user_ids = pd.Series(list(user_ids), name='user_id')
    reduced = reduced.join(user_ids)

    return reduced


def create_plot3d(df, df2):
    max_height = max(df['y'])
    splot_anim = [create_scatter3d(df), create_scatter3d(df2), create_scatter3d(df2), create_scatter3d(df)]
    frames = [go.Frame(
        data=[go.Scatter3d(x=df['x'][:k], y=df['y'][:k], z=df['z'][:k],
                           mode="lines", line=dict(width=8, color="red"), opacity=1, name="Headset", showlegend=True
                           ),
              go.Scatter3d(x=df2['x'][:k], y=df2['y'][:k], z=df2['z'][:k],
                           mode="lines", line=dict(width=8, color="green"), opacity=1, name="Controller", showlegend=True
                           )]) for k in range(len(df['timestamp'])+1)]
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
                        mode="lines", line=dict(width=2, color="blue"), opacity=1, showlegend=False)


def create_scatterplot(data, title, classes_col="user_id", x_index=0, y_index=1, x_label='X', y_label='Y'):
    traces = []

    for name in data[classes_col].unique():
        trace = dict(
            type='scatter',
            x=(data[data[classes_col] == name])[x_index],
            y=(data[data[classes_col] == name])[y_index],
            mode='markers',
            name=name,
            marker=dict(
                size=12,
                line=dict(
                    color='rgba(217, 217, 217, 0.14)',
                    width=0.5),
                opacity=0.8)
        )
        traces.append(trace)

    layout = dict(
        xaxis=dict(title=x_label, showline=False),
        yaxis=dict(title=y_label, showline=False),
        title=dict(text=title)
    )
    fig = dict(data=traces, layout=layout)

    return po.plot(fig, output_type='div')


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
        df_primary_controller = pd.DataFrame(list(
            db.get_movements_by_session_id_and_controler_id(session_id=session_id, controller_id=CONTROLLER_1))
        )
        df_headset = pd.DataFrame(list(
            db.get_movements_by_session_id_and_controler_id(session_id=session_id, controller_id=HEADSET))
        )
        data = []
        for i in df_primary_controller.to_dict('records'):
            data.append(Movement.from_dict(i))
        return render_template('graph.html',
                               graph3d_div=create_plot3d(df_primary_controller, df_headset),
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
    graphs = []
    for instance in METRIX:
        values = compute_metric(instance)
        for key in values:
            graphs.append(create_metric_boxplot(values[key], type(instance).__name__ + " " + key))

    return render_template('metrix.html', graphs=graphs)


@blueprint.route('/dim_reduction')
def dim_reduction():
    graphs = []
    metrix_df = pd.DataFrame(list(get_all_metrix()))

    graphs.append(create_scatterplot(reduce_dimensionality(metrix_df, reducer=PCA(n_components=2)),
                                     "PCA dimensionality reduction on metrix vectors", x_label='PC1', y_label='PC2'))
    graphs.append(create_scatterplot(reduce_dimensionality(metrix_df, reducer=TSNE()),
                                     "t-SNE dimensionality reduction on metrix vectors", x_label='Component 1',
                                     y_label='Component 2'))

    return render_template('metrix.html', graphs=graphs, title="BehaPass - Metrix dimensionality reduction")


def compute_metric(instance: Metric):
    results = {"averages": {}, "medians": {}}
    for user_id in get_user_ids():
        results["averages"][user_id] = []
        results["medians"][user_id] = []
        for session_id in get_session_ids(user_id):
            movements = []
            for record in db.get_movements_by_session_id(session_id=session_id):
                try:
                    movements.append(Movement.from_dict(record))
                except KeyError:
                    pass
            if movements:
                result = instance.calculate(movements)
                results["averages"][user_id].append(result.average)
                results["medians"][user_id].append(result.median)
    return results
