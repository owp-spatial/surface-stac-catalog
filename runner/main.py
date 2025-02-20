import argparse
import os
from os.path import basename
from pathlib import Path
import json

from stac_manager.catalog_manager import CatalogManager
from stac_manager.data_models import STACCollectionSource, STACItemSource

import numpy as np 

from runner.utils import get_collection_map_from_remote_catalog
from runner.data_models import CatalogTableRecord
from runner.constants import OWP_SPATIAL_S3_BUCKET_BASE, \
    OWP_SPATIAL_S3_BUCKET_NAME
from runner.s3_bucket import S3Bucket
from runner.remote_catalog_table import RemoteCatalogTable
from runner.s3_data_cataloger import S3DataCataloger
 
from config.config import Config as config

# ----------------------------------------------------------------------------- 
# ---- Catalog data in OWP Spatial S3 bucket data -----
# ----------------------------------------------------------------------------- 

# s3_bucket = S3Bucket(OWP_SPATIAL_S3_BUCKET_NAME)
# s3_bucket.add_prefix("surface", "nws-ehydro")
# s3_bucket.add_prefix("surface", "nws-nos-surveys")
# s3_bucket.add_prefix("surface", "nws-topobathy")

# prefix_list = s3_bucket.get_relative_prefixes()
# prefix_list

# s3_catalog = S3DataCataloger(bucket_name=OWP_SPATIAL_S3_BUCKET_NAME, prefix_list=prefix_list)
# s3_catalog.get_metadata_list()

# ----------------------------------------------------------------------------- 
# ---- Main function -----
# ----------------------------------------------------------------------------- 

def main(catalog_path : str,
         catalog_id : str,
         catalog_title : str,
         catalog_description : str,
         elevation_sources_path : str,
         verbose : bool = True
         ):

    # Get the collection map from the remote catalog
    collection_map = get_collection_map_from_remote_catalog(elevation_sources_path)

    # Create a catalog manager
    catalog_manager = CatalogManager(
        catalog_path=catalog_path,
        id=catalog_id,
        title = catalog_title,
        description = catalog_description
    )

    if verbose:
        catalog_manager.describe()

    # Add collections and items to the catalog
    for key, value in collection_map.items():
        if verbose:
            print(f"Adding Collection: {key}")

        collection  = value.get("collection")
        items       = value.get("items", [])

        # Add collection as a child
        catalog_manager.add_child_collection(
            collection_id=collection.id, 
            title=collection.title, 
            description=collection.description
        )

        # Add items to the collection
        for item in items:
            if verbose:
                print(f" > Adding Item ID '{item.id}' to collection ID '{item.collection_id}'")

            try:
                catalog_manager.add_item_to_collection(
                    collection_id=item.collection_id, 
                    data_path=item.data_path, 
                    properties=item.properties
                ) 
            except Exception as e:
                print(f"e:\n > '{e}'")
    
    # Save the catalog
    catalog_manager.save_catalog()

    if verbose:
        catalog_manager.describe()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create or update a STAC catalog at the specified path.")
    parser.add_argument("--catalog_path", type=str, default=config.CATALOG_URI, help="Path or URI for the STAC catalog")
    parser.add_argument("--catalog_id", type=str, default=config.ROOT_CATALOG_ID, help="Root Catalog ID")
    parser.add_argument("--catalog_title", type=str, default=config.ROOT_CATALOG_TITLE, help="Root Catalog Title")
    parser.add_argument("--catalog_description", type=str, default=config.ROOT_CATALOG_DESCRIPTION, help="Root Catalog Description")
    parser.add_argument("--elevation_sources_path", type=str, default=config.ELEVATION_SOURCES_DATA_URI, help="Path to the elevation sources data")
    parser.add_argument("--verbose", action="store_true", default=True, help="Print verbose output")

    args = parser.parse_args()

    main(
        catalog_path=args.catalog_path,
        catalog_id=args.catalog_id,
        catalog_title=args.catalog_title,
        catalog_description=args.catalog_description,
        elevation_sources_path=args.elevation_sources_path,
        verbose=args.verbose
    )