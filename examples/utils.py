import pandas as pd
import numpy as np

def clean_catalog_table(df):

    clean_names = {
        "Region" : "region",
        "Source" : "source",
        "Resolution" : "resolution",
        "Topo?" : "has_topo",
        "Bathy?" : "has_bathymetry",
        "Horizontal Coordinate System" : "horizontal_crs",
        "Vertical Datum" : "vertical_datum",
        "Vertical Datum Conversion" : "vertical_datum_conversion",
        "Source URL" : "source_url",
        "Priority" : "priority"
    }

    # clean column names
    df = df.rename(columns=clean_names, inplace=False)

    # ---- Clean region column ----
    df['region'] = df['region'].fillna("")
    df['region'] = _snake_case_values(df['region'])

    # ---- Clean source column ----
    df['source'] = df['source'].fillna("")
    df['source'] = _snake_case_values(df['source'])
    
    # ---- Clean has_topo ----
    df['has_topo'] = np.where(
        df['has_topo'].str.lower() == "yes", 
        True,
        False
    )

    # ---- Clean has_bathymetry ----
    df['has_bathymetry'] = np.where(
        df['has_bathymetry'].str.lower() == "yes", 
        True,
        False
    )
    # ---- Clean horizontal_crs ----
    # ---- Clean vertical_datum ----
    # ---- Clean vertical_datum_conversion ----
    # ---- Clean source_url ----
    # ---- Clean priority ----
    df['priority'] = df['priority'].fillna(0)
    df['priority'] = df['priority'].astype("int")

    # Remove rows with no source_url:
    df = df[~df['source_url'].isna()]

    return df

def _snake_case_values(df_column):
    return df_column.str.lower().str.replace(r'\s+', '_', regex=True) 