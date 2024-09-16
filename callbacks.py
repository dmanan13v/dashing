from dash import Input, Output, State, callback_context
from dash.exceptions import PreventUpdate

from calcule import ReturnCruncher
from config_service.asset_map import AssetMap
from config_service.load_config import load_config
from data.data_sorter import DataSorter
from operations import (get_combined_stats_matrix, get_slider_marks,
                        update_graphs_secondary)
from support import store_data

data_interface = DataSorter()
map_interface = AssetMap(**load_config("asset_map"))

def register_callbacks(app):
    @app.callback(Output('url', 'pathname'),
                  Input('enter-app-button', 'n_clicks'),
                  State('url', 'pathname'))
    def change_url(enter_clicks, current_path):
        ctx = callback_context
        if not ctx.triggered:
            return app.no_update
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'enter-app-button':
            return '/main'
        elif button_id == 'back-button':
            return '/'
        else:
            return current_path

    @app.callback(
        Output("data_store", "data"),
        Input("asset_dropdown", "value"),
        prevent_initial_call=True,
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
        return (get_combined_stats_matrix(data=crunch), "content_loaded")