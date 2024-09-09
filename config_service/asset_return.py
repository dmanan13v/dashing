from dataclasses import dataclass, fields
from typing import Optional

import pandas as pd

from config_service.small_return import ReturnSummary


@dataclass
class AssetReturnHolder:
    bench_display: str
    bench_return: ReturnSummary
    bull_display: str
    bull_return: ReturnSummary
    bear_display: Optional[str] = None
    bear_return: Optional[ReturnSummary] = None
