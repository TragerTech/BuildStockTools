"""BuildStockTools package."""
from __future__ import annotations

from importlib.metadata import version

from buildstocktools.logging import configure_logging, logger

__all__ = ["configure_logging", "logger"]


def __getattr__(name: str):
    if name == "__version__":
        return version("buildstocktools")
    raise AttributeError(name)

