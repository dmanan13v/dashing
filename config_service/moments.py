from dataclasses import dataclass

@dataclass
class Moments:
    mean: float
    std: float
    skew: float
    kurt: float