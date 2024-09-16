from dataclasses import dataclass
from typing import Optional
from config_service.moments import Moments
from config_service.small_return import ReturnSummary

@dataclass
class AssetReturnHolder:
    bench_display: str
    bench_return: ReturnSummary
    bull_display: str
    bull_return: ReturnSummary
    bench_stats: Moments
    bull_stats: Moments
    bear_display: Optional[str] = None
    bear_return: Optional[ReturnSummary] = None
    bear_stats: Optional[Moments] = None
