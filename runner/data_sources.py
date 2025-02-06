# VRT file URIs 
VRT_SOURCES = [
    # 3DEP - VRT
    "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/USGS_Seamless_DEM_1.vrt",
    # "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/USGS_Seamless_DEM_13.vrt",

    # Atlantic - VRT 
    "https://chs.coast.noaa.gov/htdata/raster2/elevation/NCEI_ninth_Topobathy_2014_8483/NCEI_ninth_Topobathy_2014_EPSG-4269.vrt",
    "https://chs.coast.noaa.gov/htdata/raster2/elevation/NCEI_ninth_Topobathy_2014_8483/NCEI_ninth_Topobathy_2014_EPSG-4269_1.vrt",

    # Hawaii - VRT
    "https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/dem/NCEI_ninth_Topobathy_Hawaii_9428/NCEI_ninth_Topobathy_Hawaii_EPSG-4326.vrt",
    ]

# STAC catalog URIs
STAC_CATALOG_SOURCES = [
    # # Atlantic - Texas - STAC Catalog
    # "https://chs.coast.noaa.gov/htdata/raster2/elevation/NCEI_ninth_Topobathy_2014_8483/stac/catalog.json",

    # # Hawaii - STAC Catalog
    # "https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/dem/NCEI_ninth_Topobathy_Hawaii_9428/stac/catalog.json",
    ]

HTML_INDEX_SOURCES = [
    # Hawaii - index.html
    # "https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/dem/NCEI_ninth_Topobathy_Hawaii_9428/index.html"
    ]

# URLs to Datasources
DATA_SOURCES = [*VRT_SOURCES, *STAC_CATALOG_SOURCES, *HTML_INDEX_SOURCES]
