"""High-level accessors for BuildStock releases."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd

from buildstocktools import config
from buildstocktools.io.duck import read_parquet
from buildstocktools.logging import logger


def discover_releases(dataset: Optional[str] = None, canonical_only: bool = True) -> pd.DataFrame:
    """Return a DataFrame of known releases."""
    releases = list(config.iter_releases(dataset=dataset, canonical_only=canonical_only))
    logger.debug("Discovered %d releases", len(releases))
    return pd.DataFrame(
        [
            {
                "key": key,
                "dataset": release.dataset,
                "version": release.version,
                "canonical": release.canonical,
                "s3_path": release.s3_path,
                "description": release.description,
            }
            for key, release in releases
        ]
    )


def _format_filter_value(value) -> str:
    if isinstance(value, (list, tuple, set)):
        members = ",".join(f"'{v}'" if isinstance(v, str) else str(v) for v in value)
        return f"IN ({members})"
    if isinstance(value, str):
        return f"= '{value}'"
    return f"= {value}"


def build_filters(filters: Optional[Dict[str, Iterable[str]]]) -> Optional[str]:
    if not filters:
        return None
    clauses = [f"{column} {_format_filter_value(value)}" for column, value in filters.items()]
    return " AND ".join(clauses)


def head(parquet_path: str | Path, n: int = 5, *, columns: Optional[Iterable[str]] = None, filters: Optional[Dict[str, Iterable[str]]] = None) -> pd.DataFrame:
    """Return the first n rows matching filters."""
    filter_expr = build_filters(filters)
    df = read_parquet(parquet_path, columns=columns, filters=filter_expr)
    return df.head(n)


def weighted_stratified_sample(
    parquet_path: str | Path,
    *,
    weight_column: str,
    strata: Optional[List[str]] = None,
    sample_size: int,
    filters: Optional[Dict[str, Iterable[str]]] = None,
    random_state: Optional[int] = None,
) -> pd.DataFrame:
    """Return a weighted stratified sample from parquet."""
    filter_expr = build_filters(filters)
    df = read_parquet(parquet_path, filters=filter_expr)
    if df.empty:
        raise ValueError("No records match the provided filters.")

    if strata:
        grouped = df.groupby(strata, dropna=False)
        weight_sums = grouped[weight_column].sum()
        proportions = weight_sums / weight_sums.sum()
        allocations_float = proportions * sample_size
        allocations = allocations_float.astype(int)
        remainder = sample_size - allocations.sum()
        if remainder > 0:
            fractional = allocations_float - allocations
            top_groups = fractional.sort_values(ascending=False).head(remainder).index
            allocations.loc[top_groups] += 1

        def sample_group(group: pd.DataFrame) -> pd.DataFrame:
            key = tuple(group.name) if isinstance(group.name, tuple) else group.name
            n_samples = allocations.loc[key]
            if n_samples == 0:
                return group.iloc[0:0]
            n_samples = min(int(n_samples), len(group))
            return group.sample(
                n=n_samples,
                weights=group[weight_column],
                replace=False,
                random_state=random_state,
            )

        sample_df = grouped.apply(sample_group)
        return sample_df.reset_index(drop=True)

    return df.sample(
        n=sample_size,
        weights=df[weight_column],
        replace=False,
        random_state=random_state,
    )


__all__ = [
    "discover_releases",
    "build_filters",
    "head",
    "weighted_stratified_sample",
]

