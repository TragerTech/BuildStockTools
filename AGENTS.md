# BuildStockTools Agents Guide

This repository contains a Python package and CLI for interacting with BuildStock datasets. When extending the project, follow these guidelines:

- Prefer DuckDB SQL and pandas vectorized operations over Python loops.
- Configure logging with `buildstocktools.logging.configure_logging` and the `loguru` logger.
- Keep canonical release metadata centralized in `buildstocktools/config.py`.
- Document schema quirks or aliases in the modules under `buildstocktools/sources/`.
- Update the README with new user-facing features or workflows.

Testing expectations:

- Add synthetic parquet fixtures in tests to validate new behavior.
- Use pytest and avoid network calls in unit tests.

For CLI contributions:

- Commands live in `buildstocktools/cli.py` using Typer.
- Provide examples in the README.

