import json
import typing 
from typing import Union

import pandas as pd
import numpy as np
import requests

from stac_manager.catalog_manager import CatalogManager
from stac_manager.data_models import STACCollectionSource, STACItemSource

from runner.constants import DATA_SOURCES_URI, DATA_FILE_EXTENSIONS

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