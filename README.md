---
description: dlt source for morphais.com
keywords: [Morphais API, morphais.com]
---

# dlt-source-morphais

[![PyPI version](https://img.shields.io/pypi/v/dlt-source-morphais)](https://pypi.org/project/dlt-source-morphais/)

[DLT](htps://www.github.com/dlt-hub/dlt) source for [Morphais](https://www.morphais.com/).

Currently loads the following data:

| Table | Contains |
| -- | -- |
| `persons` | Items of the `Person` model with all properties |
| `persons_*` | Multi-value properties derived of the `Person` model |
| `highlights` | Unique [highlights](https://morphais.readme.io/reference/filter-functions#highlights) |
| `audiences` | Unique audiences (B2B, B2C, etc.)  |
| `legal_forms` | Unique legal forms (GmbH, Ltd., etc.) |
| `funding_stages` | Unique funding stages (Pre-Seed, Seed, etc.)  |
| `industries` | Unique [industries](https://morphais.readme.io/reference/filter-functions#industries) |
| `solutions` | Unique [solutions](https://morphais.readme.io/reference/filter-functions#solutions) |
| `startups` | Items of the `Startup` model with all properties |
| `startups_*` | Multi-value properties derived of the `Startup` model |

## Usage

Create a `.dlt/secrets.toml` with your API key and email:

```toml
morphais_email="<YOUR-EMAIL>"
morphais_api_key="<YOUR_API_KEY>"
```

and then run the default source with optional list references:

```py
from dlt_source_morphais import source as morphais_source

pipeline = dlt.pipeline(
   pipeline_name="morphais_pipeline",
   destination="duckdb",
   dev_mode=True,
)
morphais_data = morphais_source()
pipeline.run(morphais_data)
```

## Development

This project is using [devenv](https://devenv.sh/).

### Run the sample

```sh
MORPHAIS_EMAIL=[...] \
   MORPHAIS_API_KEY=[...] \
   python morphais_pipeline.py
```

### Regenerate the model

Run

```sh
generate-model
```
