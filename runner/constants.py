
def s3_path(base_url, *parts):
    """Join S3 path components without worrying about slashes."""
    return "/".join([base_url, "/".join(parts) + "/"])

# -------------------------------------------------------------
# ---- BASE S3 path ----
# -------------------------------------------------------------

S3_PREFIX = "s3://"
OWP_SPATIAL_S3_BUCKET_NAME = "spatial-water-noaa"
OWP_SPATIAL_S3_BUCKET_BASE = f"{S3_PREFIX}{OWP_SPATIAL_S3_BUCKET_NAME}"

# -------------------------------------------------------------
# ---- S3 paths ----
# -------------------------------------------------------------

OWP_SPATIAL_SURFACE_S3_BUCKET = s3_path(OWP_SPATIAL_S3_BUCKET_BASE, "surface")

OWP_SPATIAL_SURFACE_NWS_EHYDRO_S3_BUCKET = s3_path(OWP_SPATIAL_S3_BUCKET_BASE, "surface", "nws-ehydro")
OWP_SPATIAL_SURFACE_NWS_NOS_SURVEYS_S3_BUCKET = s3_path(OWP_SPATIAL_S3_BUCKET_BASE, "surface", "nws-nos-surveys")
OWP_SPATIAL_SURFACE_NWS_TOPOBATHY_S3_BUCKET = s3_path(OWP_SPATIAL_S3_BUCKET_BASE, "surface", "nws-topobathy")
# -------------------------------------------------------------
# ---- Data util variables ----
# -------------------------------------------------------------

DATA_SOURCES_URI = "https://owp-spatial.r-universe.dev/elevationSources/data/catalog_table/json"

# -------------------------------------------------------------
# ---- Data util variables ----
# -------------------------------------------------------------

DATA_FILE_EXTENSIONS = [".tif", ".tiff", ".vrt", ".zip", ".gpkg", 
                  ".nc", ".zip", ".gdb", ".shp", ".json", ".geojson"]




