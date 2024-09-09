
from dataclasses import dataclass

import pandas as pd

@dataclass
class ReturnSummary:
    actual: float
    actual_start: pd.Timestamp
    actual_end: pd.Timestamp
    night: float
    night_start: pd.Timestamp
    night_end: pd.Timestamp
    day: float
    day_start: pd.Timestamp
    day_end: pd.Timestamp
