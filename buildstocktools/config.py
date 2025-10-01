"""BuildStock release registry and configuration utilities."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional

from loguru import logger


@dataclass(frozen=True)
class Release:
    """Description of an OEDI BuildStock release."""

    dataset: str
    version: str
    canonical: bool
    s3_path: str
    description: str

    def local_path(self, base_dir: Optional[Path] = None) -> Path:
        """Return the expected local storage path for the release."""
        if base_dir is None:
            base_dir = Path.home() / ".cache" / "buildstocktools"
        path = base_dir / self.dataset / self.version
        logger.debug("Derived local path for {} {}: {}", self.dataset, self.version, path)
        return path


_RELEASES: Dict[str, Release] = {
    "resstock-2024.2": Release(
        dataset="resstock",
        version="2024.2",
        canonical=True,
        s3_path="s3://oedi-data-lake/buildstock/resstock/2024.2",
        description="ResStock v2024.2 official release",
    ),
    "resstock-2025.1": Release(
        dataset="resstock",
        version="2025.1",
        canonical=True,
        s3_path="s3://oedi-data-lake/buildstock/resstock/2025.1",
        description="ResStock v2025.1 official release",
    ),
    "comstock-2024.2": Release(
        dataset="comstock",
        version="2024.2",
        canonical=True,
        s3_path="s3://oedi-data-lake/buildstock/comstock/2024.2",
        description="ComStock v2024.2 official release",
    ),
}


def get_release(key: str) -> Release:
    """Fetch a release by key, raising KeyError if unknown."""
    logger.debug("Fetching release {}", key)
    return _RELEASES[key]


def list_releases(dataset: Optional[str] = None, canonical_only: bool = False) -> Iterable[Release]:
    """Iterate over releases filtered by dataset/canonical flag."""
    releases = _RELEASES.values()
    if dataset:
        releases = [r for r in releases if r.dataset == dataset.lower()]
    if canonical_only:
        releases = [r for r in releases if r.canonical]
    logger.debug(
        "Listing releases for dataset={} canonical_only={} -> {} entries",
        dataset,
        canonical_only,
        len(list(releases)) if isinstance(releases, list) else "unknown",
    )
    return releases


def iter_releases(dataset: Optional[str] = None, canonical_only: bool = False):
    """Yield (key, release) pairs respecting filters."""
    for key, release in _RELEASES.items():
        if dataset and release.dataset != dataset.lower():
            continue
        if canonical_only and not release.canonical:
            continue
        yield key, release


def describe_release(key: str) -> str:
    release = get_release(key)
    return f"{release.dataset.title()} {release.version}: {release.description} ({release.s3_path})"

