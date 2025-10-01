from __future__ import annotations

from pathlib import Path

import pandas as pd

from buildstocktools.access import build_filters, discover_releases, head, weighted_stratified_sample


def write_parquet(tmp_path: Path, name: str, df: pd.DataFrame) -> Path:
    path = tmp_path / name
    df.to_parquet(path, index=False)
    return path


def test_discover_releases_contains_canonical():
    df = discover_releases()
    assert not df.empty
    assert "resstock-2024.2" in df["key"].values


def test_build_filters_handles_sequences():
    filters = build_filters({"state": ["CO", "CA"], "year": 2020})
    assert "state IN ('CO','CA')" in filters
    assert "year = 2020" in filters


def test_head_filters(tmp_path):
    data = pd.DataFrame(
        {
            "building_id": [1, 2, 3],
            "state": ["CO", "CA", "CO"],
            "weight": [1.0, 2.0, 3.0],
        }
    )
    path = write_parquet(tmp_path, "resstock.parquet", data)
    df = head(path, n=2, filters={"state": "CO"})
    assert len(df) == 2
    assert set(df["state"]) == {"CO"}


def test_weighted_stratified_sample(tmp_path):
    data = pd.DataFrame(
        {
            "building_id": [1, 2, 3, 4, 5, 6],
            "state": ["CO", "CO", "CA", "CA", "CA", "WA"],
            "iecc_climate_zone": ["5B", "5B", "3C", "3C", "4C", "5B"],
            "weight": [1.0, 1.0, 2.0, 2.0, 2.0, 4.0],
        }
    )
    path = write_parquet(tmp_path, "resstock.parquet", data)
    df = weighted_stratified_sample(
        path,
        weight_column="weight",
        strata=["state"],
        sample_size=3,
        random_state=42,
    )
    assert len(df) == 3
    assert set(df["state"]) == {"CO", "CA", "WA"}

