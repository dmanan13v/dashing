from dataclasses import fields
import pandas as pd
from config_service.load_config import load_config
from config_service.asset_map import AssetMap
import dash
from dash import dcc, html, Input, Output
from data_sorter import DataSorter
from operations import store_data, update_graphs_on_start

data_interface = DataSorter()
map_interface = AssetMap(**load_config("asset_map"))

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(
    [
        html.H1("Direxion Products"),
        dcc.Dropdown(
            id="asset-dropdown",
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
            id="graphs-container",
            children=[
                dcc.Slider(id='date-slider'),
                html.Div(
                    [
                        dcc.Graph(id="benchmark"),
                        dcc.Graph(id="bull"),
                        dcc.Graph(id="bear", style={"display": "none"}),
                    ],
                    style={
                        "width": "70%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
                html.Div(
                    [html.H3("Statistics"), html.Table(id="stats-table")],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
            ],
        ),
        dcc.Store(id="data-store"),
    ]
)

# intial callback that returns graphs and slider
@app.callback(
    Output("graphs-container", "children"), [Input("asset-dropdown", "value")]
)
def update_graphs_initial(selected_asset: str):
    if selected_asset is None:
        return
    return update_graphs_on_start(
        selected_asset, map_interface=map_interface, data_interface=data_interface
    )


# callback to store data everytime we update graphs
@app.callback(
    Output("data-store", "data"),
    Input("asset-dropdown", "value"),
    prevent_initial_call=True,  # Prevents callback from firing on initialization
)
def callback_store_data(selected_asset: str):
    print("restoring data")
    return store_data(
        selected_asset, map_interface=map_interface, data_interface=data_interface
    )



if __name__ == "__main__":
    app.run_server(debug=True)
