# BuildStockTools

BuildStockTools provides reproducible access to NREL's ResStock and ComStock datasets published on the [OEDI data lake](https://data.openei.org/submissions/4870). The package combines DuckDB-powered Parquet readers, canonical release discovery, and weight-aware stratified sampling utilities. A Typer-powered CLI offers quick inspection of datasets.

## Installation

```bash
pip install .
```

For development, install the optional test dependencies:

```bash
pip install .[test]
```

## Usage

### CLI

List canonical releases:

```bash
buildstocktools canonical
```

Inspect a parquet file:

```bash
buildstocktools head data/sample.parquet --column state --column weight
```

Draw a weighted stratified sample:

```bash
buildstocktools sample data/sample.parquet \
  --sample-size 100 \
  --weight-column weight \
  --strata state --strata iecc_climate_zone \
  --filter state=[CO,CA]
```

### Python API

```python
from buildstocktools.access import weighted_stratified_sample

df = weighted_stratified_sample(
    "data/sample.parquet",
    weight_column="weight",
    strata=["state"],
    sample_size=100,
    filters={"state": ["CO", "CA"]},
    random_state=42,
)
```

## Testing

```bash
pytest
```

## License

GPL-3.0

