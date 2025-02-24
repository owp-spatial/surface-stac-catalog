# surface-stac-catalog

This repository contains a script for creating or updating a SpatioTemporal Asset Catalog (STAC) using the `CatalogManager` class.

## Installation

Ensure you have Python installed (>=3.8). Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The main.py script is designed to create or update a STAC catalog by processing elevation source data.

## CLI Arguments

Argument Description Default
--catalog_path Path or URI for the STAC catalog Config value
--catalog_id Root Catalog ID Config value
--catalog_title Root Catalog Title Config value
--catalog_description Root Catalog Description Config value
--elevation_sources_path Path to the elevation sources data Config value
--verbose Print verbose output (default: True) True

## Example

You can execute the script with default configuration values:

```bash
python runners/main.py \
  --catalog_path "s3://my-catalog-path" \
  --catalog_id "my_catalog" \
  --catalog_title "My STAC Catalog" \
  --catalog_description "A description of my catalog" \
  --elevation_sources_path "s3://elevation-data" \
  --verbose
```

## Config

The script relies on a `config.py` file, which reads environment variables from a .env file if present. If the .env file is missing, it falls back to default values.

### .env File (Optional)

You can define a .env file in the project root to override configuration values:

```bash
DEBUG=True
BASE_DIR=/path/to/catalog
ROOT_CATALOG_ID=my_custom_catalog
ROOT_CATALOG_TITLE=My Custom STAC Catalog
ROOT_CATALOG_DESCRIPTION=My custom description
ELEVATION_SOURCES_DATA_URI=https://my-data-source.com/elevationSources
```

### Default Configuration Values

If environment variables are not set, config.py will use sensible defaults:

```bash
DEBUG=True
BASE_DIR= ./catalog/
ROOT_CATALOG_ID="hf-surfaces-catalog"
ROOT_CATALOG_TITLE="hf-surfaces-title"
ROOT_CATALOG_DESCRIPTION="hf-surfaces-description"
ELEVATION_SOURCES_DATA_URI="https://owp-spatial.r-universe.dev/elevationSources/data/catalog_table/json"
```

## License

This project is licensed under the Apache 2.0 License.
