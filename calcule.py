from io import StringIO
from typing import Any, Optional

import numpy as np
import pandas as pd

from config_service.asset_map import AssetMap
from config_service.asset_multi import AssetMulti
from config_service.asset_return import AssetReturnHolder
from config_service.load_config import load_config
from config_service.moments import Moments
from config_service.small_return import ReturnSummary


class ReturnCruncher:
    def __init__(self, data_dict: dict, marks: Optional[list] = None) -> None:
        self.titre: AssetMulti = getattr(
            AssetMap(**load_config("asset_map")), data_dict.get("asset")
        )
        self._data = self.load_and_process_data(data_dict)
        self.marks = marks or None

    def load_and_process_data(self, data_dict):
        df = pd.read_json(StringIO(data_dict.get("frame")))
        df["Date"] = pd.to_datetime(df["Date"])
        tickers = [self.titre.bench, self.titre.bull] + (
            [self.titre.bear] if self.titre.bear else []
        )
        return df[df["ticker"].isin(tickers)]

    @property
    def data(self):
        return self._data.copy()

    def get_close_to_close(self, ticker: str, marks: list) -> dict[str, Any]:
        start, end = [round(x / 2) for x in marks[:2]]

        df_filtered = (
            self.data[self.data["ticker"] == ticker]
            .sort_values("Date")
            .reset_index(drop=True)
        )

        end = min(end, df_filtered.index.max())
        close_start = df_filtered["Close"].loc[start]
        close_end = df_filtered["Close"].loc[end]

        return {
            "return": round((close_end / close_start - 1) * 100, 2),
            "date_start": df_filtered["Date"].loc[start],
            "date_end": df_filtered["Date"].loc[end],
        }

    def get_night_return(self, ticker: str, marks: list) -> dict[str, Any]:
        df_filtered = (
            self.data[self.data["ticker"] == ticker]
            .sort_values("Date")
            .reset_index(drop=True)
        )

        percent_changes = []
        start, end = [round(x / 2) for x in marks[:2]]
        end = end - 1
        end = min(end, df_filtered.index.max())
        for day in range(start, end):
            close_price = df_filtered.iloc[day]["Close"]
            next_open_price = df_filtered.iloc[day + 1]["Open"]
            percent_change = next_open_price / close_price
            percent_changes.append(percent_change)

        net_change = (np.prod(np.array(percent_changes)) - 1) * 100
        return {
            "return": round(net_change, 2),
            "date_start": df_filtered["Date"].loc[start],
            "date_end": df_filtered["Date"].loc[end],
        }

    def get_day_return(self, ticker: str, marks: list) -> dict[str, Any]:
        df_filtered = (
            self.data[self.data["ticker"] == ticker]
            .sort_values("Date")
            .reset_index(drop=True)
        )

        percent_changes = []
        start, end = [round(x / 2) for x in marks[:2]]
        end = min(end, df_filtered.index.max())
        for day in range(start, end):
            open_price = df_filtered.iloc[day]["Open"]
            close_price = df_filtered.iloc[day]["Close"]
            percent_change = close_price / open_price
            percent_changes.append(percent_change)

        net_change = (np.prod(np.array(percent_changes)) - 1) * 100

        return {
            "return": round(net_change, 2),
            "date_start": df_filtered["Date"].loc[start],
            "date_end": df_filtered["Date"].loc[end],
        }

    def get_summary_per_asset(self, ticker: str, marks: list):
        actual = self.get_close_to_close(ticker=ticker, marks=marks)
        night = self.get_night_return(ticker=ticker, marks=marks)
        day = self.get_day_return(ticker=ticker, marks=marks)
        return ReturnSummary(
            actual=actual.get("return"),
            actual_start=actual.get("date_start"),
            actual_end=actual.get("date_end"),
            night=night.get("return"),
            night_start=night.get("date_start"),
            night_end=night.get("date_end"),
            day=day.get("return"),
            day_start=day.get("date_start"),
            day_end=day.get("date_end"),
        )

    def get_moments(self, ticker: str, marks: list) -> Moments:
        df_filtered = (
            self.data[self.data["ticker"] == ticker]
            .sort_values("Date")
            .reset_index(drop=True)
        )
        df_filtered['Change'] = df_filtered['Close'].pct_change()
        
        # Assuming 252 trading days in a year
        trading_days = 252
        
        return Moments(
            mean=df_filtered['Change'].mean() * trading_days * 100,  # Annualized and converted to percentage
            std=df_filtered['Change'].std() * np.sqrt(trading_days) * 100,  # Annualized and converted to percentage
            skew=df_filtered['Change'].skew(),  # Skewness doesn't need annualization
            kurt=df_filtered['Change'].kurtosis(),  # Kurtosis doesn't need annualization
        )

    def get_returns_for_everything(self) -> AssetReturnHolder:
        return AssetReturnHolder(
            bench_display=self.titre.bench_display,
            bench_return=self.get_summary_per_asset(
                ticker=self.titre.bench, marks=self.marks
            ),
            bull_display=self.titre.bull_display,
            bull_return=self.get_summary_per_asset(
                ticker=self.titre.bull, marks=self.marks
            ),
            bench_stats=self.get_moments(ticker=self.titre.bench, marks=self.marks),
            bull_stats=self.get_moments(ticker=self.titre.bull, marks=self.marks),
            bear_display=self.titre.bear_display,
            bear_return=(
                self.get_summary_per_asset(ticker=self.titre.bear, marks=self.marks)
                if self.titre.bear
                else None
            ),
            bear_stats=(
                self.get_moments(ticker=self.titre.bear, marks=self.marks)
                if self.titre.bear
                else None
            ),
        )
