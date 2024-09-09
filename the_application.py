from dataclasses import fields
from calcule import ReturnCruncher
from config_service.load_config import load_config
from config_service.asset_map import AssetMap
from dash import dcc, html, Input, Output, State
from dash import dash
from dash.exceptions import PreventUpdate

from data.data_sorter import DataSorter
from operations import get_slider_marks, update_graphs_secondary, get_stats_matrix

from support import store_data
import dash_bootstrap_components as dbc

data_interface = DataSorter()
map_interface = AssetMap(**load_config("asset_map"))

# Initialize the Dash app
app = dash.Dash(__name__, assets_folder="assets")

# Define the layout
app.layout = html.Div(
    [
        html.H1("Direxion Products - Performance Analysis"),
        dcc.Dropdown(
            id="asset_dropdown",
            options=[
                {
                    "label": getattr(map_interface, field.name).set_name,
                    "value": field.name,
                }
                for field in fields(map_interface)
            ],
            placeholder="Select an asset",
        ),
        html.Div(
            id="slider_home",
            children=[
                dcc.RangeSlider(
                    id="slider",
                    min=0,
                    max=450,
                    step=1,
                    value=[0, 500],
                )
            ],
            className="hidden_content",
        ),
        html.Div(
            id="graphs_container",
            children=[
                html.Div(
                    [
                        dcc.Graph(id="benchmark", style={"display": "none"}),
                        dcc.Graph(id="bull", style={"display": "none"}),
                        dcc.Graph(id="bear", style={"display": "none"}),
                    ]
                ),
            ],
            className="hidden_content",
        ),
        html.H2("Summary Statistics: Pure 3x Leverage Return, Real Return"),
        html.Div(id= "stats_home", children = [dcc.Graph(id="stats_show")], className="hidden_content"),
        dcc.Store(id="data_store", data=None),
        dcc.Store(id="range_slider_value_store"),
    ]
)


# callback to store data everytime dropdown is clicked
@app.callback(
    Output("data_store", "data"),
    Input("asset_dropdown", "value"),
    prevent_initial_call=True,  # Prevents callback from firing on initialization
)
def callback_store_data(selected_asset: str):
    if not selected_asset:
        raise PreventUpdate
    return store_data(
        selected_asset, map_interface=map_interface, data_interface=data_interface
    )


@app.callback(
    [
        Output("slider", "value"),
        Output("slider", "className"),
        Output("graphs_container", "children"),
        Output("graphs_container", "className"),
        Output("slider", "marks"),
        Output("slider_home", "className"),
    ],
    [Input("slider", "value"), Input("data_store", "data")],
    prevent_initial_call=True,
)
def update_graph(slider_range: list[float], some_data: dict):
    if not bool(some_data):
        raise PreventUpdate
    figure = update_graphs_secondary(
        map_interface=map_interface,
        date_slider_value=slider_range,
        data_store=some_data,
    )
    marks = get_slider_marks(map_interface=map_interface, store=some_data)
    return (
        slider_range,
        "content_loaded",
        figure,
        "content_loaded",
        marks,
        "content_loaded",
    )


@app.callback(
    [
        Output("stats_home", "children"),
        Output("stats_home", "className")
    ],
    [Input("slider", "value"), Input("data_store", "data")],
)
def deliver_stats(marks: list[float], some_data: dict):
    if marks is None or some_data is None:
        raise PreventUpdate
    crucher = ReturnCruncher(data_dict=some_data, marks=marks)
    crunch = crucher.get_returns_for_everything()
    return (get_stats_matrix(data=crunch), "content_loaded")


if __name__ == "__main__":
    app.run_server(debug=True)
