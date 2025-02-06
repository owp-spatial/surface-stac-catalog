import json
import typing 
from typing import Union

import requests

from runner.constants import DATA_SOURCES_URI

class RemoteCatalog:
    def __init__(self, url: str = DATA_SOURCES_URI):
        self.url = url
        self.catalog_data = None
        self._init_catalog()

    def _fetch_catalog(self) -> Union[str, list[dict], dict, None]:
        """Retrieve the catalog data from the provided URL."""
        try:
            resp = requests.get(self.url)
            resp.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
            self.catalog_data = resp.json()  # Store the catalog data for further processing
            return self.catalog_data
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except ValueError as e:
            print(f"JSON decoding error: {e}")
        return None  # Return None if an error occurs

    def _convert_str_lists_to_lists(self, 
                                   catalog_data : list[dict],
                                   str_list_keys: list[dict] = None
                                   ) -> list[dict]:
        
        """Convert specific string-based list fields to actual lists."""
        if not catalog_data:
            print("No catalog data to process.")
            return catalog_data

        if str_list_keys is None:
            str_list_keys = ["asset_urls"]

        # convert string lists (i.e. "[]") to actual lists for specific keys
        for record in catalog_data:
            for key in str_list_keys:
                if key in record:
                    try:
                        record[key] = json.loads(record.get(key, '[""]'))  # convert string to list
                    except Exception as e:
                        print(f"Error converting key {key}: {e}")

        return catalog_data
    
    def _init_catalog(self) -> None:
        if not self.catalog_data:
            catalog_data = self._fetch_catalog()
            catalog_data = self._convert_str_lists_to_lists(catalog_data=catalog_data, 
                                                            str_list_keys = ["asset_urls"]
                                                            )
        self.catalog_data = catalog_data
            
        return None

    def get_catalog(self) -> Union[list[dict], None]:
        """Process the catalog and return the processed data."""
        return self.catalog_data
