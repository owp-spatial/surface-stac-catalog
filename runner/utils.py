import json
import typing 
from typing import Union

import pandas as pd
import numpy as np
import requests

from stac_manager.catalog_manager import CatalogManager
from stac_manager.data_models import STACCollectionSource, STACItemSource

from runner.constants import ELEVATION_SOURCES_DATA_URI, DATA_FILE_EXTENSIONS

def get_prefix_from_s3_dir(bucket_name :str, bucket_dir:str) -> str:
    """Given a bucket name and a directory in that bucket, get a string that can be used for searching via s3.list_objects_v2()"""
    
    # bucket_name = OWP_SPATIAL_S3_BUCKET_NAME
    # bucket_dir = OWP_SPATIAL_SURFACE_NWS_EHYDRO_S3_BUCKET

    dir_names = bucket_dir.replace("s3://", "").replace(bucket_name, "").split("/")

    return "/".join([i for i in dir_names if i])

def get_collection_list_from_catalog_table(df):
    
    collections_list = []

    for index, row  in df.iterrows():
        # print(f"index: {index}\nrow: {row}")
        stac_collection = STACCollectionSource(
            id = row['domain'],
            title = f"{row['domain']} title", 
            description=f"{row['domain']} description"
        )
        collections_list.append(stac_collection)
        # print()

    return collections_list

def get_collection_id_from_parts(*parts):
    collection_id = "_".join([i for i in parts if i])
    return collection_id

def get_urls_ending_with(urls : list[str], ending:str):
    return [i for i in urls if i.endswith(ending)] 

def get_urls_not_ending_with(urls: list[str], endings: list[str]) -> list[str]:
    return [url for url in urls if not any(url.endswith(end) for end in endings)]
    
# TODO: Figure out how CatalogManager will handle being given a 'catalog.json' as a collection/item/asset
# TODO: Right now, I am just prioritzing any assets with a ".vrt", if No VRT exists, then use whatever other data sources are avalaible
# TODO: If NO OTHER DATA SOURCES exists EXCEPT a catalog.json, then use that. 
# TODO: In the future its very likely that the catalog.json will be second in priorirty
def get_highest_priority_asset_urls(urls : list[str]) -> list[str]:

    # priority 1: Look for ".vrt" URLs first
    vrt_urls = get_urls_ending_with(urls, ".vrt")
    if vrt_urls:
        return vrt_urls

    # priority 2: Look for everything else (not ".vrt" or "catalog.json")
    other_urls = get_urls_not_ending_with(urls, [".vrt", "catalog.json"])
    if other_urls:
        return other_urls

    # priority 3: Fall back to "catalog.json" URLs if exists
    catalog_urls = get_urls_ending_with(urls, "catalog.json")
    if catalog_urls:
        return catalog_urls

    # None if no URLs art matched 
    return []  