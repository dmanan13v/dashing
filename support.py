from dataclasses import dataclass, fields
import pandas as pd
from config_service.asset_map import AssetMap
from config_service.asset_return import AssetReturnHolder
from data.data_sorter import DataSorter
from config_service.small_return import ReturnSummary

def store_data(
    selected_asset: str, data_interface: DataSorter, map_interface: AssetMap
):
    if selected_asset is None:
        pass
    asset_instance = getattr(map_interface, selected_asset)
    filtered_df = data_interface.filter_by_strings(asset_instance.spit_tickers())
    filtered_df.selected_asset = selected_asset
    return {"frame": filtered_df.to_json(), "asset": selected_asset}


def organise_df(df: pd.DataFrame) -> pd.DataFrame:
    with pd.option_context("mode.chained_assignment", None):
        df.loc[:, "Date"] = pd.to_datetime(df["Date"])
        df.loc[:, "open_time"] = df["Date"].apply(
            lambda x: x.replace(hour=9, minute=30)
        )
        df.loc[:, "close_time"] = df["Date"].apply(
            lambda x: x.replace(hour=16, minute=0)
        )

    df_combined = pd.concat(
        [
            df[["open_time", "Open"]].rename(
                columns={"open_time": "Date", "Open": "Price"}
            ),
            df[["close_time", "Close"]].rename(
                columns={"close_time": "Date", "Close": "Price"}
            ),
        ]
    )

    df_combined = df_combined.sort_values("Date").reset_index(drop=True)

    return df_combined


def get_display_values(dataclass_instance: dataclass) -> list[str]:
    display_values = []
    for field in fields(dataclass_instance):
        if "display" in field.name:
            value = getattr(dataclass_instance, field.name)
            if value is not None:
                display_values.append(value)
    return display_values


def timestamp_to_nice_string(start: pd.Timestamp, end: pd.Timestamp):
    return f"Calculated from {start:%Y-%m-%d} to {end:%Y-%m-%d}"


def get_annotation_map(return_summary: ReturnSummary):
    return {
        'actual': f"{return_summary.actual_start:%Y-%m-%d} to {return_summary.actual_end:%Y-%m-%d}",
        'day': f"{return_summary.day_start:%Y-%m-%d} to {return_summary.day_end:%Y-%m-%d}",
        'night': f"{return_summary.night_start:%Y-%m-%d} to {return_summary.night_end:%Y-%m-%d}"
    }