"""ComStock schema helpers."""
from __future__ import annotations

from typing import Dict

REGION_ALIASES: Dict[str, str] = {
    "state": "state",
    "state_abbreviation": "state",
    "utility": "utility",
    "utility_service_area": "utility",
    "cbecs_climate_zone": "cbecs_climate_zone",
    "ashrae_climate_zone": "ashrae_climate_zone",
}


def normalize_columns(columns):
    return [REGION_ALIASES.get(col.lower(), col) for col in columns]


def region_columns() -> Dict[str, str]:
    return {
        "state": "State abbreviation",
        "utility": "Utility service territory",
        "cbecs_climate_zone": "CBECS climate zone",
        "ashrae_climate_zone": "ASHRAE climate zone",
    }

