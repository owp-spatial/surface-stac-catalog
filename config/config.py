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