import os
from dotenv import load_dotenv
from pathlib import Path

class Config:
    """Configuration settings loaded from environment variables."""
    
    # Locate the .env file
    DEFAULT_BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_PATH = DEFAULT_BASE_DIR / ".env"

    # Load environment variables from the .env file
    load_dotenv(dotenv_path=ENV_PATH)

    DEBUG = os.getenv("DEBUG") == "True"

    # Base directory where STAC catalogs will live
    # BASE_DIR = os.getenv("BASE_DIR", str(DEFAULT_BASE_DIR))
    BASE_DIR = os.getenv("BASE_DIR", "./catalog/")
    ROOT_STAC_DIR_NAME = os.getenv("ROOT_STAC_DIR_NAME", "stac-root")
    ROOT_STAC_DIR = os.path.join(BASE_DIR, ROOT_STAC_DIR_NAME)

    # Name of the main catalog.json file (defaults to "catalog.json")
    CATALOG_FILE_NAME = os.getenv("CATALOG_FILE_NAME", "catalog.json")
    CATALOG_URI = os.path.join(ROOT_STAC_DIR, CATALOG_FILE_NAME)

    # Name data for the root STAC catalog
    ROOT_CATALOG_ID = os.getenv("ROOT_CATALOG_ID", "hf-surfaces-catalog")
    ROOT_CATALOG_TITLE = os.getenv("ROOT_CATALOG_TITLE", "hf-surfaces-title")
    ROOT_CATALOG_DESCRIPTION = os.getenv("ROOT_CATALOG_DESCRIPTION", "hf-surfaces-description")
    
    ELEVATION_SOURCES_DATA_URI = os.getenv("ELEVATION_SOURCES_DATA_URI", "https://owp-spatial.r-universe.dev/elevationSources/data/catalog_table/json")

# # Locate the .env file
# DEFAULT_BASE_DIR = Path(__file__).resolve().parent.parent
# ENV_PATH = DEFAULT_BASE_DIR / ".env"

# # Load environment variables from the .env file
# load_dotenv(dotenv_path=ENV_PATH)

# DEBUG = os.getenv("DEBUG") == "True"

# # Base directory where stac catalogs will live
# BASE_DIR = os.getenv("BASE_DIR", str(DEFAULT_BASE_DIR))
# # BASE_DIR = os.getenv("BASE_DIR")
# ROOT_STAC_DIR_NAME= os.getenv("ROOT_STAC_DIR_NAME", "stac-root")
# ROOT_STAC_DIR=os.path.join(BASE_DIR, ROOT_STAC_DIR_NAME)

# # Directory for a specific Catalog
# CATALOG_DIR_NAME = os.getenv("CATALOG_DIR_NAME", "")
# CATALOG_DIR = os.path.join(ROOT_STAC_DIR, CATALOG_DIR_NAME)

# # name of the main catalog.json file (defaults to "catalog.json") 
# CATALOG_FILE_NAME = os.getenv("CATALOG_FILE_NAME", "catalog.json")
# CATALOG_URI = os.path.join(CATALOG_DIR, CATALOG_FILE_NAME)

# # Name data for the root STAC catalog
# ROOT_CATALOG_ID           = os.getenv("ROOT_CATALOG_ID", "hf-surfaces-catalog")
# ROOT_CATALOG_TITLE        = os.getenv("ROOT_CATALOG_TITLE", "hf-surfaces-title")
# ROOT_CATALOG_DESCRIPTION  = os.getenv("ROOT_CATALOG_DESCRIPTION", "hf-surfaces-description")

# ELEVATION_SOURCES_DATA_URI = os.getenv("ELEVATION_SOURCES_DATA_URI")

# # # TODO: Remove these testing files from the settings
# # VRT_URI = os.getenv("VRT_URI")
# # TIF_URI = os.getenv("TIF_URI")
# # TIF_URI_1 = os.getenv("TIF_URI_1")
# # TIF_URI_2 = os.getenv("TIF_URI_2")