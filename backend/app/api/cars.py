import json
from fastapi import APIRouter, HTTPException
from app.services import geo_service

router = APIRouter(prefix="/cars", tags=["cars"])

@router.get("")
def list_cars():
    cars = geo_service.get_all_cars()
    geojson = cars.to_json()
    return json.loads(geojson)

@router.get("/{cod_imovel}/talhoes")
def list_talhoes_by_car(cod_imovel: str):
    talhoes = geo_service.get_talhoes_by_car(cod_imovel)

    if talhoes.empty:
        raise HTTPException(status_code=404, detail=f'Talhões não encontrados para o CAR: {cod_imovel}')

    geojson = talhoes.to_json()
    return json.loads(geojson)