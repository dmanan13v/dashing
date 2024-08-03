from dataclasses import dataclass, fields
from config_service.asset_multi import AssetMulti

@dataclass
class AssetMap:
    treasuries_20: dict
    treasuries_7: dict
    ftse_china: dict
    eu_mid_cap: dict
    emerging_markets: dict
    mexico: dict
    korea: dict
    sp_mid_cap: dict
    spy: dict
    rut: dict

    def __post_init__(self):
        # Iterate over all fields of the dataclass
        for field in fields(self):
            # Get the current value of the field
            field_value = getattr(self, field.name)
            # Update the field value by creating an AssetMulti instance
            setattr(self, field.name, AssetMulti(**field_value))

