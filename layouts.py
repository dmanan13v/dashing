from dataclasses import fields

from dash import dcc, html

from config_service.asset_map import AssetMap
from config_service.load_config import load_config

map_interface = AssetMap(**load_config("asset_map"))

landing_layout = html.Div(
    [
        html.H1("Welcome to the App"),
        html.P("Click the button to enter"),
        html.Button("Enter App", id="enter-app-button", n_clicks=0),
        html.Div(id="page-content"),
    ]
)

main_app_layout = html.Div(
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
        html.H2("Returns Summary"),
        html.Div(
            id="stats_home",
            children=[dcc.Graph(id="stats_show")],
            className="hidden_content",
        ),
        dcc.Store(id="data_store", data=None),
        dcc.Store(id="range_slider_value_store"),
    ]
)
