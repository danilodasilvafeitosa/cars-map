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

def get_car_by_id(cod_imovel: str):
    if _cars_gdf is None:
        raise RuntimeError("Dados nao carregados. Chame load_data() no startup.")

    matching_cars = _cars_gdf[_cars_gdf["cod_imovel"] == cod_imovel]

    if matching_cars.empty:
        raise ValueError(f"CAR com cod_imovel '{cod_imovel}' nao encontrado.")

    return matching_cars.iloc[0]

def get_talhoes_by_car(cod_imovel: str) -> gpd.GeoDataFrame:
    if _talhoes_gdf is None:
        raise RuntimeError("Dados nao carregados. Chame load_data() no startup.")
    return _talhoes_gdf[_talhoes_gdf["cod_imovel"] == cod_imovel]

def get_talhao_centroid(talhao_row):
    centroid = talhao_row.geometry.centroid
    latitude = centroid.y
    longitude = centroid.x
    return (latitude, longitude)

def get_talhao_geometry_web_mercator(talhao_row):
    geometry_series = gpd.GeoSeries([talhao_row.geometry], crs="EPSG:4326")
    geometry_web_mercator = geometry_series.to_crs("EPSG:3857")

    return geometry_web_mercator.iloc[0]
