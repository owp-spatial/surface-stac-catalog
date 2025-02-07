# Theres a OWP Spatial S3 bucket with a 'surface' directory
# I'm going to walk specific directories 
# in Each directory, ill find more directories 
# ac collection will be "dir1_dir2"
# (i.e "nws-ehydro_conus", "nws-ehydro_puerto-rico/")
# All spatial files within these directories will become items / assets for that collection

import os
from dataclasses import dataclass

import boto3

from runner.constants import OWP_SPATIAL_S3_BUCKET_BASE, \
    OWP_SPATIAL_S3_BUCKET_NAME, \
    OWP_SPATIAL_SURFACE_NWS_EHYDRO_S3_BUCKET, \
    OWP_SPATIAL_SURFACE_NWS_NOS_SURVEYS_S3_BUCKET, \
    OWP_SPATIAL_SURFACE_NWS_TOPOBATHY_S3_BUCKET

from runner.s3_bucket import S3Bucket

# from runner.utils import get_prefix_from_s3_dir

@dataclass
class StacMetadata:
    collection_paths: list[str]
    item_id: str
    asset_id: str
    asset_href: str
    source: str
    domain: str

class S3DataCataloger:
    def __init__(self, bucket_name: str, prefix_list: list[str] = None, s3_client=None) -> None:
        self.s3 = s3_client or boto3.client("s3")  
        self._bucket_name = bucket_name
        self._prefix_list = prefix_list or []
        self._objects_list = []
        self._metadata_list: list[StacMetadata] = []
        self._populate_data_lists()

    def _populate_data_lists(self) -> None:
        """Populate the lists with objects and metadata."""
        self._get_objects_with_prefixes()
        self._extract_metadata_from_objects_list()

    def get_object_list(self) -> list[dict]:
        """Return the list of objects fetched from S3."""
        return self._objects_list

    def get_metadata_list(self) -> list[StacMetadata]:
        """Return the list of STAC metadata objects."""
        return self._metadata_list

    def _get_objects_with_prefixes(self) -> None:
        """Fetch objects from S3 based on the prefixes."""
        for prefix in self._prefix_list:
            response = self.s3.list_objects_v2(Bucket=self._bucket_name, Prefix=prefix)
            if response.get("Contents"):
                for obj in response["Contents"]:
                    if not obj["Key"].endswith("/"):
                        obj["prefix"] = prefix
                        self._objects_list.append(obj)

    def _extract_metadata_from_objects_list(self) -> None:
        """Extract metadata from the list of objects."""
        for obj in self.get_object_list():
            metadata = self._get_stac_metadata_from_s3_object(obj)
            if metadata:
                self._metadata_list.append(metadata)
    def _get_stac_metadata_from_s3_object(self, s3_object: dict) -> StacMetadata:
            """Extract STAC metadata from a given S3 object."""
            key = s3_object.get("Key")
            if not key or key.endswith("/"):
                return None
            
            s3_uri = f"s3://{self._bucket_name}/{key}"
            file_name = os.path.basename(key)
            dir_parts = key.split("/")
            
            if len(dir_parts) < 4:
                return None  # Ensure proper path structure
            
            source = dir_parts[2]  # Extract <SOURCE>
            domain = dir_parts[3]  # Extract <DOMAIN>

            return StacMetadata(
                collection_paths=dir_parts[:-1],
                item_id=key,
                asset_id=file_name,
                asset_href=s3_uri,
                source=source,
                domain=domain
            )

    # def _get_stac_metadata_from_s3_object(self, s3_object: dict) -> StacMetadata:
    #     """Extract STAC metadata from a given S3 object."""
    #     key = s3_object.get("Key")
    #     if not key or key.endswith("/"):
    #         return None
        
    #     s3_uri = f"s3://{self._bucket_name}/{key}"
    #     file_name = os.path.basename(key)
    #     dir_name = os.path.dirname(key)

    #     return StacMetadata(
    #         collection_paths=dir_name.split('/'),
    #         item_id=key,
    #         asset_id=file_name,
    #         asset_href=s3_uri
    #     )

# s3_bucket = S3Bucket(OWP_SPATIAL_S3_BUCKET_NAME)
# s3_bucket.add_prefix("surface", "nws-ehydro")
# s3_bucket.add_prefix("surface", "nws-nos-surveys")
# s3_bucket.add_prefix("surface", "nws-topobathy")

# s3_bucket.get_relative_prefixes()

# # prefix_list = [
# #     get_prefix_from_s3_dir(OWP_SPATIAL_S3_BUCKET_NAME, OWP_SPATIAL_SURFACE_NWS_EHYDRO_S3_BUCKET),
# #     get_prefix_from_s3_dir(OWP_SPATIAL_S3_BUCKET_NAME, OWP_SPATIAL_SURFACE_NWS_NOS_SURVEYS_S3_BUCKET),
# #     get_prefix_from_s3_dir(OWP_SPATIAL_S3_BUCKET_NAME, OWP_SPATIAL_SURFACE_NWS_TOPOBATHY_S3_BUCKET)
# #     ]

# s3_catalog = S3DataCataloger(bucket_name=OWP_SPATIAL_S3_BUCKET_NAME, prefix_list=prefix_list)
# s3_catalog.get_metadata_list()