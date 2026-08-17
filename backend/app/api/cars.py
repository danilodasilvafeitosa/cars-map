import json
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from typing import Optional

from app.services import geo_service
from app.services import report_service

router = APIRouter(prefix="/cars", tags=["cars"])

class ReportRequest(BaseModel):
    talhao_ids: Optional[list[str]] = None

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

    talhoes_simplified = talhoes.copy()
    talhoes_simplified["geometry"] = talhoes_simplified["geometry"].simplify(0.00005)

    geojson = talhoes_simplified.to_json()
    return json.loads(geojson)

@router.post("/{cod_imovel}/report")
def generate_report(cod_imovel: str, body: ReportRequest = None):
    try:
        car_row = geo_service.get_car_by_id(cod_imovel)
        talhoes = geo_service.get_talhoes_by_car(cod_imovel)

        if body and body.talhao_ids:
            talhoes = talhoes[talhoes["talhao_id"].isin(body.talhao_ids)]

        talhoes_rows = [row for _, row in talhoes.iterrows()]

        report = report_service.generate_talhoes_report(car_row, talhoes_rows)

        return Response(
            content=report,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=relatorio_climatico.pdf"
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
