from config_service.asset_map import AssetMap
from data_sorter import DataSorter
import plotly.graph_objs as go
from dash import dcc, html


def update_graphs_on_start(
    selected_asset: str, map_interface: AssetMap, data_interface: DataSorter
):
    asset_instance = getattr(map_interface, selected_asset)

    filtered_df = data_interface.filter_by_strings(asset_instance.spit_tickers())

    # bench_graph
    df_bench = filtered_df[filtered_df["ticker"] == asset_instance.bench]
    df_bull = filtered_df[filtered_df["ticker"] == asset_instance.bull]
    df_bear = (
        filtered_df[filtered_df["ticker"] == asset_instance.bear]
        if asset_instance.bear
        else None
    )

    common_dates = set(df_bench["Date"]) & set(df_bull["Date"])
    if df_bear is not None:
        common_dates &= set(df_bear["Date"])

    common_dates = sorted(list(common_dates))

    # Create Date Slider
    date_slider = dcc.RangeSlider(
        id="date-slider",
        min=0,
        max=len(common_dates) - 1,
        value=[0, len(common_dates) - 1],
        marks={
            i: date
            for i, date in enumerate(common_dates)
            if i % (len(common_dates) // 10) == 0
        },  # Display fewer marks for readability
        step=1
    )

    benchmark = {
        "data": [
            go.Scatter(
                x=df_bench["Date"],
                y=df_bench["Close"],
                mode="lines",
                name=asset_instance.bench_display,
            )
        ],
        "layout": go.Layout(
            title=f"{asset_instance.bench_display}",
            xaxis={"title": "Date"},
            yaxis={"title": "Close"},
            margin={"l": 40, "b": 40, "t": 40, "r": 40},
            hovermode="closest",
        ),
    }

    # bull_graph

    bull = {
        "data": [
            go.Scatter(
                x=df_bull["Date"],
                y=df_bull["Close"],
                mode="lines",
                name=asset_instance.bench_display,
            )
        ],
        "layout": go.Layout(
            title=f"{asset_instance.bull_display}",
            xaxis={"title": "Date"},
            yaxis={"title": "Close"},
            margin={"l": 40, "b": 40, "t": 40, "r": 40},
            hovermode="closest",
        ),
    }
    callback_list = [benchmark, bull]
    # bear_graph
    if asset_instance.bear:
        bear = {
            "data": [
                go.Scatter(
                    x=df_bear["Date"],
                    y=df_bear["Close"],
                    mode="lines",
                    name=asset_instance.bench_display,
                )
            ],
            "layout": go.Layout(
                title=f"{asset_instance.bear_display}",
                xaxis={"title": "Date"},
                yaxis={"title": "Close"},
                margin={"l": 40, "b": 40, "t": 40, "r": 40},
                hovermode="closest",
            ),
        }

        callback_list.append(bear)

    return html.Div(
        [date_slider, html.Div([dcc.Graph(figure=graph) for graph in callback_list])]
    )


def store_data(
    selected_asset: str, data_interface: DataSorter, map_interface: AssetMap
):
    if selected_asset is None:
        pass
    asset_instance = getattr(map_interface, selected_asset)
    filtered_df = data_interface.filter_by_strings(asset_instance.spit_tickers())
    return filtered_df.to_json()


