"""ResStock schema helpers."""
from __future__ import annotations

from typing import Dict

REGION_ALIASES: Dict[str, str] = {
    "state": "state",
    "state_abbreviation": "state",
    "state_cd": "state",
    "census_division": "census_division",
    "eba": "balancing_area",
    "balancing_area": "balancing_area",
    "hdd_bin": "heating_bin",
    "cooling_bin": "cooling_bin",
    "iecc_climate_zone": "iecc_climate_zone",
}


def normalize_columns(columns):
    """Map known aliases to canonical ResStock names."""
    return [REGION_ALIASES.get(col.lower(), col) for col in columns]


def region_columns() -> Dict[str, str]:
    """Return canonical region column descriptions."""
    return {
        "state": "State abbreviation",
        "census_division": "Census division",
        "balancing_area": "Electric balancing authority",
        "heating_bin": "Heating degree bin",
        "cooling_bin": "Cooling degree bin",
        "iecc_climate_zone": "IECC climate zone",
    }

