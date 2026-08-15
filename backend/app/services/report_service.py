from jinja2 import Template
from weasyprint import HTML
from pathlib import Path

from app.services import geo_service
from app.services.climate_service import get_talhao_climate_report_data
from app.services import charts_service
from app.services import satellite_service
from app.services.ai_insights_service import generate_climate_insights

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "report.html"

def _build_talhao_data(talhao_row):
    latitude, longitude = geo_service.get_talhao_centroid(talhao_row)
    climate_data = get_talhao_climate_report_data(latitude, longitude)

    croqui = satellite_service.plot_talhao_satellite(talhao_row)
    insights = generate_climate_insights(climate_data["climatology"], climate_data["current_year"])

    rainfall_climatology = charts_service.plot_rainfall_climatology(climate_data["climatology"])
    temperature_climatology = charts_service.plot_temperature_climatology(climate_data["climatology"])
    rainfall_comparison = charts_service.plot_rainfall_comparison(climate_data["climatology"], climate_data["current_year"])
    temperature_comparison = charts_service.plot_temperature_comparison(climate_data["climatology"], climate_data["current_year"])

    return {
        "talhao_id": talhao_row.talhao_id,
        "area_ha": talhao_row.area_ha,
        "croqui": croqui,
        "rainfall_climatology": rainfall_climatology,
        "temperature_climatology": temperature_climatology,
        "rainfall_comparison": rainfall_comparison,
        "temperature_comparison": temperature_comparison,
        "insights": insights,
    }
