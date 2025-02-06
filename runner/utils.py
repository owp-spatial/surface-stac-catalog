import json
import typing 
from typing import Union

import pandas as pd
import numpy as np
import requests

from stac_manager.catalog_manager import CatalogManager
from stac_manager.data_models import STACCollectionSource, STACItemSource

from runner.constants import DATA_SOURCES_URI, DATA_FILE_EXTENSIONS


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