import argparse
import os
from os.path import basename
from pathlib import Path
import json

from stac_manager.catalog_manager import CatalogManager
from stac_manager.data_models import STACCollectionSource, STACItemSource

import pandas as pd
import numpy as np 

from runner.utils import get_collection_id_from_parts, get_highest_priority_asset_urls
from runner.data_models import CatalogTableRecord
from runner.data_sources import VRT_SOURCES, \
    STAC_CATALOG_SOURCES, \
    HTML_INDEX_SOURCES, \
    DATA_SOURCES

from runner.constants import OWP_SPATIAL_S3_BUCKET_BASE, \
    OWP_SPATIAL_S3_BUCKET_NAME, \
    OWP_SPATIAL_SURFACE_NWS_EHYDRO_S3_BUCKET, \
    OWP_SPATIAL_SURFACE_NWS_NOS_SURVEYS_S3_BUCKET, \
    OWP_SPATIAL_SURFACE_NWS_TOPOBATHY_S3_BUCKET

from runner.s3_bucket import S3Bucket
from runner.remote_catalog_table import RemoteCatalogTable
from runner.s3_data_cataloger import S3DataCataloger
 
import config.settings as settings

# 1. Get the remote catalog
# 1a. Create Collections for each unique domain in REMOTE CATALOG
# 2a. Add asset_urls as items (and as assets) to respective collection

# 2. Get eHydro paths in S3
# 2a. 
# ----------------------------------------------------------------------------- 
# ---- Elevation Sources Spatial S3 bucket data -----
# ----------------------------------------------------------------------------- 
settings.CATALOG_URI
settings.ELEVATION_SOURCES_DATA_URI

remote_catalog=RemoteCatalogTable(url=settings.ELEVATION_SOURCES_DATA_URI)
elevation_sources = remote_catalog.get_catalog()    
elevation_sources[0]


# collection_id : {collection : STACCollectionSource, items : list[STACItemSource]}
collection_map = {}

for record in elevation_sources:
    print(f"record: {record}")

    # if len(record.asset_urls) > 1:
        # break
    
    # Build collection ID
    collection_id = get_collection_id_from_parts(record.domain, record.region)

    # Add collection to map if it hasnt been added yet
    if collection_id not in collection_map:
        collection = STACCollectionSource(
            id = collection_id,
            title = f"{collection_id} title",
            description= f"{collection_id} description"
        )

        collection_map[collection_id] = {"collection" : collection, "items" : []}
    
    # get URLs to map to items
    urls = get_highest_priority_asset_urls(record.asset_urls if record.asset_urls else [record.source_url])

    # get list of items for this record and put it in the items list for the collection 
    items = [STACItemSource(
                collection_id=collection_id,
                id=basename(asset_url),
                data_path=asset_url,
                properties={key :  val for key, val in record.__dict__.items() if key in ["source", "resolution", 
                                                                    "horizontal_crs", "vertical_datum",
                                                                    "priority"
                                                                    ]
                                                                    }
                                                                    )
                for asset_url in urls
                ]

    collection_map[collection_id].get("items").extend(items)

    print()

collection_map.keys()
[len(val.get("items")) for key, val in collection_map.items()]

# catalog_manager = CatalogManager(
#     catalog_path=settings.CATALOG_URI,
#     id=settings.ROOT_CATALOG_ID,
#     title=settings.ROOT_CATALOG_TITLE,
#     description=settings.ROOT_CATALOG_DESCRIPTION,
# )

# catalog_manager.describe()

# for collection in collections:
#     print(f"Adding Collection: {collection.id}")
#     catalog_manager.add_child_collection(
#         collection_id=collection.id, title=collection.title, description=collection.description
#     )
# ----------------------------------------------------------------------------- 
# ---- Catalog data in OWP Spatial S3 bucket data -----
# ----------------------------------------------------------------------------- 
S3DataCataloger()


s3_bucket = S3Bucket(OWP_SPATIAL_S3_BUCKET_NAME)
s3_bucket.add_prefix("surface", "nws-ehydro")
s3_bucket.add_prefix("surface", "nws-nos-surveys")
s3_bucket.add_prefix("surface", "nws-topobathy")

prefix_list = s3_bucket.get_relative_prefixes()
prefix_list

s3_catalog = S3DataCataloger(bucket_name=OWP_SPATIAL_S3_BUCKET_NAME, prefix_list=prefix_list)
s3_catalog.get_metadata_list()

# ----------------------------------------------------------------------------- 
# ---- S3 OWP Spatial S3 bucket data -----
# ----------------------------------------------------------------------------- 

s3_bucket = S3Bucket(OWP_SPATIAL_S3_BUCKET_NAME)
s3_bucket.add_prefix("surface", "nws-ehydro")
s3_bucket.add_prefix("surface", "nws-nos-surveys")
s3_bucket.add_prefix("surface", "nws-topobathy")

prefix_list = s3_bucket.get_relative_prefixes()
s3_catalog = S3DataCataloger(bucket_name=OWP_SPATIAL_S3_BUCKET_NAME, prefix_list=prefix_list)
s3_catalog.get_metadata_list()

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