from io import StringIO
from typing import Optional
from calcule import ReturnCruncher
from config_service.asset_map import AssetMap
from config_service.asset_multi import AssetMulti

import plotly.graph_objs as go
from dash import dcc, html
import pandas as pd

from config_service.asset_return import AssetReturnHolder
from config_service.small_return import ReturnSummary
from data.data_sorter import DataSorter
from support import get_annotation_map, get_display_values, organise_df
from plotly.subplots import make_subplots

def get_slider_marks(map_interface: AssetMap, store: dict):

    filtered_df = pd.read_json(StringIO(store.get("frame")))
    asset_instance = getattr(map_interface, store.get("asset"))

    df_bench = organise_df(filtered_df[filtered_df["ticker"] == asset_instance.bench])
    df_bull = organise_df(filtered_df[filtered_df["ticker"] == asset_instance.bull])
    df_bear = (
        organise_df(filtered_df[filtered_df["ticker"] == asset_instance.bear])
        if asset_instance.bear
        else None
    )
    common_dates = set(df_bench["Date"]) & set(df_bull["Date"])
    if df_bear is not None:
        common_dates &= set(df_bear["Date"])

    common_dates = sorted(list(common_dates))

    return {
        i: date
        for i, date in enumerate(common_dates)
        if i % (len(common_dates) // 10) == 0
    }


def update_graphs_secondary(
    map_interface: AssetMap, date_slider_value: list[float], data_store=dict
):
    slider_start, slider_end = date_slider_value[:2]
    filtered_df = pd.read_json(StringIO(data_store.get("frame")))

    relevant_map_item = getattr(map_interface, data_store.get("asset"))

    df_bench = organise_df(
        filtered_df[filtered_df["ticker"] == relevant_map_item.bench]
    ).iloc[slider_start:slider_end, :]
    df_bull = organise_df(
        filtered_df[filtered_df["ticker"] == relevant_map_item.bull]
    ).iloc[slider_start:slider_end, :]
    df_bear = (
        organise_df(filtered_df[filtered_df["ticker"] == relevant_map_item.bear]).iloc[
            slider_start:slider_end, :
        ]
        if relevant_map_item.bear
        else None
    )

    return [
        deliver_graphs(
            df_bench=df_bench,
            df_bull=df_bull,
            df_bear=df_bear,
            asset_map_item=relevant_map_item,
        )
    ]


def deliver_graphs(
    df_bench: pd.DataFrame,
    df_bull: pd.DataFrame,
    asset_map_item: AssetMulti,
    df_bear: Optional[pd.DataFrame] = None,
):

    benchmark = {
        "data": [
            go.Scatter(
                x=df_bench["Date"],
                y=df_bench["Price"],
                mode="lines",
                name=asset_map_item.bench_display,
            )
        ],
        "layout": go.Layout(
            title=f"{asset_map_item.bench_display}",
            xaxis={"title": "Date"},
            yaxis={"title": "Price"},
            margin={"l": 40, "b": 40, "t": 40, "r": 40},
            hovermode="closest",
        ),
    }

    # bull_graph

    bull = {
        "data": [
            go.Scatter(
                x=df_bull["Date"],
                y=df_bull["Price"],
                mode="lines",
                name=asset_map_item.bench_display,
            )
        ],
        "layout": go.Layout(
            title=f"{asset_map_item.bull_display}",
            xaxis={"title": "Date"},
            yaxis={"title": "Price"},
            margin={"l": 40, "b": 40, "t": 40, "r": 40},
            hovermode="closest",
        ),
    }
    callback_list = [benchmark, bull]
    # bear_graph
    if asset_map_item.bear:
        bear = {
            "data": [
                go.Scatter(
                    x=df_bear["Date"],
                    y=df_bear["Price"],
                    mode="lines",
                    name=asset_map_item.bench_display,
                )
            ],
            "layout": go.Layout(
                title=f"{asset_map_item.bear_display}",
                xaxis={"title": "Date"},
                yaxis={"title": "Price"},
                margin={"l": 40, "b": 40, "t": 40, "r": 40},
                hovermode="closest",
            ),
        }

        callback_list.append(bear)

    return html.Div([dcc.Graph(figure=graph) for graph in callback_list])


def get_stats_matrix(data: AssetReturnHolder):
    from support import get_annotation_map

    columns = [''] + [data.bench_display, data.bull_display]
    if data.bear_display:
        columns.append(data.bear_display)

    # Mapping of original field names to new display titles
    row_titles = {
        'Total': 'Holding the entire time',
        'Day': 'Holding only through the day',
        'Night': 'Holding only through the night'
    }

    rows = ['Total', 'Day', 'Night']  # Keep original names for field access
    table_data = []

    for row_label in rows:
        row_data = [row_titles[row_label]]  # Use new title for display
        for attr in ['bench_return', 'bull_return', 'bear_return']:
            if hasattr(data, attr) and getattr(data, attr):
                return_data = getattr(data, attr)
                field = 'actual' if row_label == 'Total' else row_label.lower()
                
                value = getattr(return_data, field)
                annotation = get_annotation_map(return_data)[field]
                cell_content = html.Div([
                    html.Div(f"{value:.2f}%", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                    html.Div(annotation, style={'fontSize': '12px', 'color': 'gray'})
                ])
                row_data.append(cell_content)
            else:
                row_data.append('')
        table_data.append(row_data)

    header = html.Tr([html.Th(col, style={'textAlign': 'center', 'padding': '10px'}) for col in columns])
    rows = [html.Tr([html.Td(cell, style={'textAlign': 'center', 'padding': '10px'}) for cell in row]) for row in table_data]

    table = html.Table([header] + rows, style={
        'width': '100%',
        'borderCollapse': 'collapse',
        'border': '1px solid black'
    })

    return [table]
