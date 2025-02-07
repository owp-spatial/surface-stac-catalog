from dataclasses import dataclass, field

from typing import List, Optional

@dataclass
class CatalogTableRecord:
    domain: str = ""
    region: str = ""
    source: str = ""
    resolution: str = ""
    has_topo: bool = False
    has_bathymetry: bool = False
    horizontal_crs: str = ""
    vertical_datum: str = ""
    vertical_datum_conversion: str = ""
    priority: int = 0
    source_url: str = ""
    asset_urls: List[str] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> "CatalogTableRecord":
        """Convert a dictionary into a DatasetMetadata object, ensuring correct types with defaults."""
        return CatalogTableRecord(
            domain=data.get("domain", ""),
            region=data.get("region", ""),
            source=data.get("source", ""),
            resolution=data.get("resolution", ""),
            has_topo=data.get("has_topo", "False") == "True",
            has_bathymetry=data.get("has_bathymetry", "False") == "True",
            horizontal_crs=data.get("horizontal_crs", ""),
            vertical_datum=data.get("vertical_datum", ""),
            vertical_datum_conversion=data.get("vertical_datum_conversion", ""),
            priority=int(data.get("priority", 0)),
            source_url=data.get("source_url", ""),
            asset_urls=data.get("asset_urls", []),
        )

data = {
    "domain": "pr-usvi",
    "region": "pr",
    "source": "ncei_cudem",
    "resolution": "3m",
    "has_topo": "True",
    "has_bathymetry": "True",
    "horizontal_crs": "NAD83",
    "vertical_datum": "PRVD02",
    "vertical_datum_conversion": "MSL = PRVD02 - 0.01583",
    "priority": 1,
    "source_url": "https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/dem/NCEI_ninth_Topobathy_PuertoRico_9525/index.html",
    "asset_urls": [
        "https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/dem/NCEI_ninth_Topobathy_PuertoRico_9525/NCEI_ninth_Topobathy_PuertoRico_EPSG-4269.vrt",
        "https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/dem/NCEI_ninth_Topobathy_PuertoRico_9525/stac/catalog.json"
    ]
}

# dataset = CatalogTableRecord.from_dict(data)
# print(dataset)
