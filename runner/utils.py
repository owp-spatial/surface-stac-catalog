import json
import typing 
from typing import Union
from os.path import basename

import numpy as np
import requests

from stac_manager.catalog_manager import CatalogManager
from stac_manager.data_models import STACCollectionSource, STACItemSource

from runner.remote_catalog_table import RemoteCatalogTable
from runner.constants import ELEVATION_SOURCES_DATA_URI, DATA_FILE_EXTENSIONS

from config.config import Config as config

def get_prefix_from_s3_dir(bucket_name :str, bucket_dir:str) -> str:
    """Given a bucket name and a directory in that bucket, get a string that can be used for searching via s3.list_objects_v2()"""
    
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

def remove_duplicates(lst):
    """Remove duplicates from a list while preserving order."""
    deduplicated = []

    for item in lst:
        if item not in deduplicated:
            deduplicated.append(item)

    return deduplicated

def get_collection_id_from_parts(*parts):

    # collection_id = "_".join(remove_duplicates([i for i in parts if i]))
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

# ----------------------------------------------------------------------------- 
# ---- Elevation Sources Spatial S3 bucket data -----
# ----------------------------------------------------------------------------- 
def get_collection_map_from_remote_catalog(url:str = config.ELEVATION_SOURCES_DATA_URI) -> dict:

    # url = config.ELEVATION_SOURCES_DATA_URI
    remote_catalog=RemoteCatalogTable(url=url)
    elevation_sources = remote_catalog.get_catalog()    

    # Stores key:values like so: 
        # collection_id : {collection : STACCollectionSource, items : list[STACItemSource]}
    collection_map = {}

    for record in elevation_sources:
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

    return collection_map