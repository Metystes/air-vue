import plotly.graph_objects as go
from flask import Flask, render_template
#import plotly.figure_factory as ff
import plotly.express as px
import plotly
import json

import numpy as np
import pandas as pd

app = Flask(__name__)

def get_data():
    pass


def plot_map(data):
    """[summary]
    
    Arguments:
        data {[df]} -- [dataframe containing at leat 3 columns: Latitude, Longitude, value]
    
    Returns:
        [type] -- [description]
    """    
    quakes = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')

    fig = go.Figure(go.Densitymapbox(lat=quakes.Latitude, lon=quakes.Longitude, z=quakes.Magnitude,
                                    radius=10))
    fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.layout.template = None

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON



@app.route("/")
def home():
    graphJSON = plot_map()
    return render_template('index.html', v=graphJSON)


if __name__ == "__main__":
    app.run(debug=True)
