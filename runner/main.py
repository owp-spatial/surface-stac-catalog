import argparse
import os
from os.path import basename
from pathlib import Path
import json

from stac_manager.catalog_manager import CatalogManager
from stac_manager.data_models import STACCollectionSource, STACItemSource

import pandas as pd
import numpy as np 

from runner.data_sources import VRT_SOURCES, \
    STAC_CATALOG_SOURCES, \
    HTML_INDEX_SOURCES, \
    DATA_SOURCES

from runner.remote_catalog import RemoteCatalog
 
from runner.utils import clean_catalog_table, _snake_case_values

import config.settings as settings

# 1. Get the remote catalog
# 1a. Create Collections for each unique domain in REMOTE CATALOG
# 2a. Add asset_urls as items (and as assets) to respective collection

# 2. Get eHydro paths in S3
# 2a. 


def main(catalog_path: str):
    # Update settings dynamically
    settings.CATALOG_URI = catalog_path
    
    # List out desired collections to create/update
    collections = [
            STACCollectionSource(
                id = "conus",
                title = "CONUS title",
                description = "CONUS description"
            ),
            STACCollectionSource(
                id = "atlantic",
                title = "Atlantic title",
                description = "Atlantic description"
            ),
            STACCollectionSource(
                id = "hawaii",
                title = "Hawaii title",
                description = "Hawaii description"
            ),
            ]

    items = [
        STACItemSource(
            collection_id="conus",
            id=basename([i for i in DATA_SOURCES if "USGS_Seamless_DEM_1.vrt" in i][0]),
            data_path=[i for i in DATA_SOURCES if "USGS_Seamless_DEM_1.vrt" in i][0],
            properties={"priority": 1},
        ),
        *(
            STACItemSource(
                collection_id="atlantic",
                id=basename(i),
                data_path=i,
                properties={"priority": 2},
            )
            for i in DATA_SOURCES if "ncei" in i.lower() and "ninth_topobathy_2014_8483" in i.lower()
        ),
        *(
            STACItemSource(
                collection_id="hawaii",
                id=basename(i),
                data_path=i,
                properties={"priority": 2},
            )
            for i in DATA_SOURCES if "ncei" in i.lower() and "hawaii" in i.lower()
        ),
    ]

    # print_dict(vars(settings))

    catalog_manager = CatalogManager(
        catalog_path=catalog_path,
        id=settings.ROOT_CATALOG_ID,
        title=settings.ROOT_CATALOG_TITLE,
        description=settings.ROOT_CATALOG_DESCRIPTION,
    )

    catalog_manager.describe()

    for collection in collections:
        print(f"Adding Collection: {collection.id}")
        catalog_manager.add_child_collection(
            collection_id=collection.id, title=collection.title, description=collection.description
        )

    for item in items:
        print(f"Adding Item: {item.id}")
        catalog_manager.add_item_to_collection(
            collection_id=item.collection_id, data_path=item.data_path, properties=item.properties
        )

    catalog_manager.save_catalog()
    catalog_manager.describe()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create or update a STAC catalog at the specified path.")

    parser.add_argument("catalog_path", type=str, help="Path or URI for the STAC catalog")
    parser.add_argument("catalog_id", type=str, help="Root Catalog ID")
    parser.add_argument("catalog_title", type=str, help="Root Catalog Title")
    parser.add_argument("catalog_description", type=str, help="Root Catalog Description")

    args = parser.parse_args()
    main(args.catalog_path)