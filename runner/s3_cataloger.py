
# Theres a OWP Spatial S3 bucket with a 'surface' directory
# I'm going to walk specific directories 
# in Each directory, ill find more directories 
# ac collection will be "dir1_dir2"
# (i.e "nws-ehydro_conus", "nws-ehydro_puerto-rico/")
# All spatial files within these directories will become items / assets for that collection

import os
import boto3

from runner.constants import OWP_SPATIAL_S3_BUCKET_BASE, \
    OWP_SPATIAL_S3_BUCKET_NAME, \
    OWP_SPATIAL_SURFACE_NWS_EHYDRO_S3_BUCKET, \
    OWP_SPATIAL_SURFACE_NWS_NOS_SURVEYS_S3_BUCKET, \
    OWP_SPATIAL_SURFACE_NWS_TOPOBATHY_S3_BUCKET

from runner.utils import get_prefix_from_s3_dir

s3 = boto3.client("s3")
get_prefix_from_s3_dir(OWP_SPATIAL_S3_BUCKET_NAME, OWP_SPATIAL_SURFACE_NWS_EHYDRO_S3_BUCKET)

class S3Cataloger:

    def __init__(self, bucket_name:str, prefix_list : list = []) -> None:
        self.s3 = boto3.client("s3")
        self._bucket_name = bucket_name
        self._prefix_list = prefix_list
        self._objects_list = []
        self._metadata_list = []
        self._populate_data_lists()

    def _populate_data_lists(self): 
        self._get_objects_with_prefixes()
        self._exract_metadata_from_objects_list()
        return 
    
    def get_object_list(self) -> list:
        return self._objects_list
    
    def get_metadata_list(self) -> list:
        return self._metadata_list
    
    def _get_objects_with_prefixes(self) -> None:
        
        for prefix in self._prefix_list:
            response = self.s3.list_objects_v2(
                Bucket=self._bucket_name,
                Prefix=prefix
            )
            if response and "Contents" in response: 

                for object in response['Contents']:
                    if not object['Key'].endswith("/"): 
                        object['prefix'] = prefix
                        self._objects_list.append(object)
        
        return 
    
    def _exract_metadata_from_objects_list(self) -> None:
        for object in self.get_object_list():
            metadata = self._get_stac_metadata_from_s3_object(object)
            self._metadata_list.append(metadata)
        return 

    def get_object_list(self) -> list:
        return self._objects_list
    
    def _get_stac_metadata_from_s3_object(self, s3_object : dict) -> dict:

        key = s3_object.get("Key")

        if not key:
            return None

        if key.endswith("/"):
            return None
        
        s3_uri = f"s3://{self._bucket_name}/{key}"
        file_name = os.path.basename(key)
        dir_name  = os.path.dirname(key)

        return {
            "collection_id" : dir_name,
            "item_id" : key,
            "asset_id" : file_name, 
            "asset_href" : s3_uri
            }


prefix_list = [
    get_prefix_from_s3_dir(OWP_SPATIAL_S3_BUCKET_NAME, OWP_SPATIAL_SURFACE_NWS_EHYDRO_S3_BUCKET),
    get_prefix_from_s3_dir(OWP_SPATIAL_S3_BUCKET_NAME, OWP_SPATIAL_SURFACE_NWS_NOS_SURVEYS_S3_BUCKET),
    get_prefix_from_s3_dir(OWP_SPATIAL_S3_BUCKET_NAME, OWP_SPATIAL_SURFACE_NWS_TOPOBATHY_S3_BUCKET)
    ]

s3_catalog = S3Cataloger(bucket_name=OWP_SPATIAL_S3_BUCKET_NAME, prefix_list=prefix_list)
s3_catalog.get_metadata_list()