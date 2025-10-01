"""DuckDB helpers for working with BuildStock parquet data."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import duckdb
import pandas as pd

from buildstocktools.logging import logger


def connect(read_only: bool = True) -> duckdb.DuckDBPyConnection:
    """Create a DuckDB connection suitable for read operations."""
    logger.debug("Creating DuckDB connection read_only=%s", read_only)
    return duckdb.connect(database=":memory:", read_only=read_only)


def register_parquet(
    conn: duckdb.DuckDBPyConnection,
    name: str,
    paths: Iterable[str | Path],
) -> None:
    """Register parquet files as a DuckDB view."""
    parquet_list = [str(Path(p)) for p in paths]
    logger.debug("Registering parquet %s as %s", parquet_list, name)
    conn.register(name, parquet_list)


def query_parquet(path: str | Path, sql: str, *, parameters: Optional[Iterable] = None) -> pd.DataFrame:
    """Execute a SQL query against the parquet dataset."""
    with connect() as conn:
        logger.debug("Running query against %s", path)
        query = f"SELECT * FROM read_parquet('{Path(path)}') WHERE 1=1"
        if "FROM" in sql.upper():
            query = sql.format(path=Path(path))
        else:
            query = f"SELECT {sql} FROM read_parquet('{Path(path)}')"
        return conn.execute(query, parameters or []).fetchdf()


def read_parquet(path: str | Path, *, columns: Optional[Iterable[str]] = None, filters: Optional[str] = None) -> pd.DataFrame:
    """Read parquet data into a DataFrame with optional filtering."""
    with connect() as conn:
        select = "*" if columns is None else ",".join(columns)
        sql = f"SELECT {select} FROM read_parquet('{Path(path)}')"
        if filters:
            sql += f" WHERE {filters}"
        logger.debug("Executing parquet read: %s", sql)
        return conn.execute(sql).fetchdf()

