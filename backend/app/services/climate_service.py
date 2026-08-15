import requests
import pandas as pd
from datetime import date, timedelta

CLIMATE_API_URL="https://archive-api.open-meteo.com/v1/archive"

def fetch_climate_data(latitude: float, longitude: float, start_date: str, end_date: str):
    params = {
        "latitude": latitude,
        "longitude":longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min,temperature_2m_mean",
        "timezone": "America/Sao_Paulo"
    }

    response = requests.get(CLIMATE_API_URL, params=params)
    response.raise_for_status()
    return response.json()

def aggregate_monthly(daily_data: dict):
    df = pd.DataFrame(daily_data)
    df["time"] = pd.to_datetime(df["time"])
    df["month"] = df["time"].dt.month

    monthly_avg = df.groupby("month").mean(numeric_only=True)
    return monthly_avg

def get_talhao_climate_report_data(latitude: float, longitude: float):
    safe_date = date.today() - timedelta(days=7)
    climatology_start = safe_date.replace(year=safe_date.year - 30)

    current_year_start = date(safe_date.year, 1, 1)

    climatology = fetch_climate_data(
        latitude=latitude,
        longitude=longitude,
        start_date=climatology_start.isoformat(),
        end_date=safe_date.isoformat(),
    )

    current_year = fetch_climate_data(
        latitude=latitude,
        longitude=longitude,
        start_date=current_year_start.isoformat(),
        end_date=safe_date.isoformat(),
    )

    return {
        "climatology": aggregate_monthly(climatology["daily"]),
        "current_year": aggregate_monthly(current_year["daily"]),
    }
