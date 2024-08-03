from dataclasses import dataclass


@dataclass
class AssetMulti:
    set_name: str
    bench: str
    bench_display: str
    bull: str
    bull_display: str
    bear: str = None
    bear_display: str = None

    def spit_tickers(self) -> list:
        return [self.bench, self.bull, self.bear]
