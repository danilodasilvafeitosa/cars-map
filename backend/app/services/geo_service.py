import logging
import geopandas as gpd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

_cars_gdf: gpd.GeoDataFrame | None = None
_talhoes_gdf: gpd.GeoDataFrame | None = None

def load_data() -> None:
    global _cars_gdf, _talhoes_gdf

    _cars_gdf = gpd.read_file(DATA_DIR / "jatai_cars.json")
    _talhoes_gdf = gpd.read_file(DATA_DIR / "jatai_talhoes.json")

    logging.info(f"CARs carregados: {len(_cars_gdf)}")
    logging.info(f"Talhoes carregados: {len(_talhoes_gdf)}")

def get_all_cars() -> gpd.GeoDataFrame:
    if _cars_gdf is None:
        raise RuntimeError("Dados nao carregados. Chame load_data() no startup.")
    return _cars_gdf

def get_talhoes_by_car(cod_imovel: str) -> gpd.GeoDataFrame:
    if _talhoes_gdf is None:
        raise RuntimeError("Dados nao carregados. Chame load_data() no startup.")
    return _talhoes_gdf[_talhoes_gdf["cod_imovel"] == cod_imovel]

def get_talhao_centroid(talhao_row):
    centroid = talhao_row.geometry.centroid
    latitude = centroid.y
    longitude = centroid.x
    return (latitude, longitude)