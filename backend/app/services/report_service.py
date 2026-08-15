import markdown
import time

from jinja2 import Template
from weasyprint import HTML
from pathlib import Path

from app.services import geo_service
from app.services.climate_service import get_talhao_climate_report_data
from app.services import charts_service
from app.services import satellite_service
from app.services.ai_insights_service import generate_climate_insights

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "report.html"
DELAY_BETWEEN_TALHOES = 1.5

def _build_talhao_data(talhao_row):
    latitude, longitude = geo_service.get_talhao_centroid(talhao_row)
    climate_data = get_talhao_climate_report_data(latitude, longitude)

    croqui = satellite_service.plot_talhao_satellite(talhao_row)
    insights = generate_climate_insights(climate_data["climatology"], climate_data["current_year"])
    insights_html = markdown.markdown(insights)

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
        "insights": insights_html,
    }

def generate_talhoes_report(car_row, talhoes_rows):
    talhoes_data = []
    for talhao in talhoes_rows:
        talhao_data = _build_talhao_data(talhao)
        talhoes_data.append(talhao_data)
        time.sleep(DELAY_BETWEEN_TALHOES)

    car_data = {
        "cod_imovel": car_row.cod_imovel,
        "municipio": car_row.municipio,
        "uf": car_row.uf,
        "area_ha": car_row.area_ha,
    }

    with open(TEMPLATE_PATH) as f:
        template = Template(f.read())

    html_content = template.render(car=car_data, talhoes=talhoes_data)
    pdf_bytes = HTML(string=html_content).write_pdf()

    return pdf_bytes
