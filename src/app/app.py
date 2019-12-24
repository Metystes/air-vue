# Import Global modules
import plotly.graph_objects as go
from flask import Flask, render_template
import plotly
import json

# Import local modules
from src.data.createDB import (Database, db_backend, db_name)
from src.models.Interpolation import Interpolation

app = Flask(__name__)


def get_data():
    dbms = Database(db_backend, db_name)
    query = """WITH ranked AS(
        SELECT m.*, ROW_NUMBER() OVER(PARTITION BY id ORDER BY time DESC) as rm
        FROM `airly_raw_data` as m
    ), locs as (SELECT id, lat, lng, city, street FROM 'airly_locs')
    SELECT r.*, l.lat, l.lng
    FROM ranked r LEFT JOIN locs as l on l.id = r.id where rm = 1
    """
    return dbms.pd_readSQL(sql=query)


def plot_map(data):
    """Plotting new map
    
    Arguments:
        data {df} -- [dataframe containing at leat 3 columns:
                      lat, lng, val]
    
    Returns:
        json -- JSON file with info about plotly figure
    """
    fig = go.Figure(go.Densitymapbox(lat=data.lat, lon=data.lng,
                                     z=data.val,
                                     radius=15, opacity=0.7))
    fig.update_layout(mapbox_style="stamen-terrain",
                      mapbox_center_lon=19.947015,
                      mapbox_center_lat=50.055163,
                      mapbox_zoom=9)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.layout.template = None

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route("/")
def home():
    data = get_data()
    data.rename(columns={'pm10': 'val'}, inplace=True)
    graphJSON = plot_map(data)

    inter = Interpolation()
    data = inter.predict_grid(
        49.8, 50.24, 19.6, 20.25, 0.001)
    data.rename(columns={'x': 'lat', 'y': 'lng'}, inplace=True)
    graphJSON_Interpolation = plot_map(data)

    return render_template('index.html', v=graphJSON,
                           map_inter=graphJSON_Interpolation)


if __name__ == "__main__":
    app.run(debug=True)
