"""Typer-powered CLI for BuildStockTools."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import typer

from buildstocktools.access import discover_releases, head as head_df, weighted_stratified_sample
from buildstocktools.logging import configure_logging, logger

app = typer.Typer(help="Tools for working with BuildStock datasets")


def _parse_filters(filters: List[str]) -> dict:
    parsed = {}
    for item in filters:
        if "=" not in item:
            raise typer.BadParameter("Filters must be in column=value format")
        column, value = item.split("=", 1)
        if value.startswith("[") and value.endswith("]"):
            entries = [v.strip() for v in value.strip("[]").split(",") if v.strip()]
            parsed[column] = entries
        else:
            parsed[column] = value
    return parsed


@app.callback()
def main(verbose: bool = typer.Option(False, "--verbose", help="Enable debug logging")) -> None:
    configure_logging("DEBUG" if verbose else "INFO")


@app.command()
def canonical(dataset: Optional[str] = typer.Option(None, help="Filter by dataset")) -> None:
    """List canonical releases."""
    df = discover_releases(dataset=dataset)
    if df.empty:
        typer.echo("No releases found")
    else:
        typer.echo(df.to_string(index=False))


@app.command()
def head(
    parquet: Path = typer.Argument(..., exists=True, dir_okay=False),
    n: int = typer.Option(5, help="Number of rows to display"),
    column: List[str] = typer.Option(None, "--column", help="Columns to select"),
    filter: List[str] = typer.Option(None, "--filter", help="Filters in column=value or column=[a,b] format"),
) -> None:
    filters = _parse_filters(filter) if filter else None
    df = head_df(parquet, n=n, columns=column or None, filters=filters)
    typer.echo(df.to_string(index=False))


@app.command()
def sample(
    parquet: Path = typer.Argument(..., exists=True, dir_okay=False),
    sample_size: int = typer.Option(..., help="Number of samples to draw"),
    weight_column: str = typer.Option(..., help="Weight column name"),
    strata: List[str] = typer.Option(None, "--strata", help="Columns for stratification"),
    filter: List[str] = typer.Option(None, "--filter", help="Filters in column=value or column=[a,b] format"),
    random_state: Optional[int] = typer.Option(None, help="Random seed"),
) -> None:
    filters = _parse_filters(filter) if filter else None
    logger.info(
        "Sampling %d rows stratified by %s with filters %s",
        sample_size,
        strata or "none",
        filters or "none",
    )
    df = weighted_stratified_sample(
        parquet,
        weight_column=weight_column,
        strata=strata or None,
        sample_size=sample_size,
        filters=filters,
        random_state=random_state,
    )
    typer.echo(df.to_string(index=False))


if __name__ == "__main__":  # pragma: no cover
    app()

