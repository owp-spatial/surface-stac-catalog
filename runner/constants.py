def s3_path(base_url, *parts):
    """Join S3 path components without worrying about slashes."""
    return "/".join([base_url, "/".join(parts) + "/"])

# -------------------------------------------------------------
# ---- S3 paths ----
# -------------------------------------------------------------

# Base S3 bucket path
S3_PREFIX = "s3://"
OWP_SPATIAL_S3_BUCKET_NAME = "spatial-water-noaa"
OWP_SPATIAL_S3_BUCKET_BASE = f"{S3_PREFIX}{OWP_SPATIAL_S3_BUCKET_NAME}"

OWP_SPATIAL_SURFACE_S3_BUCKET = s3_path(OWP_SPATIAL_S3_BUCKET_BASE, "surface")

# -------------------------------------------------------------
# ---- Data util variables ----
# -------------------------------------------------------------

ELEVATION_SOURCES_DATA_URI = "https://owp-spatial.r-universe.dev/elevationSources/data/catalog_table/json"

# -------------------------------------------------------------
# ---- Data util variables ----
# -------------------------------------------------------------

DATA_FILE_EXTENSIONS = [".tif", ".tiff", ".vrt", ".zip", ".gpkg", 
                  ".nc", ".zip", ".gdb", ".shp", ".json", ".geojson"]
