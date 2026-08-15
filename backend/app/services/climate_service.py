import requests
import pandas as pd
from datetime import date, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential

CLIMATE_API_URL="https://archive-api.open-meteo.com/v1/archive"

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
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

def aggregate_monthly(df: pd.DataFrame):
    df = df.copy()
    df["month"] = df["time"].dt.month

    monthly_avg = df.groupby("month").mean(numeric_only=True)
    return monthly_avg

def get_talhao_climate_report_data(latitude: float, longitude: float):
    safe_date = date.today() - timedelta(days=7)
    climatology_start = safe_date.replace(year=safe_date.year - 30)
    current_year_num = date.today().year

    response = fetch_climate_data(
        latitude=latitude,
        longitude=longitude,
        start_date=climatology_start.isoformat(),
        end_date=safe_date.isoformat(),
    )

    df = pd.DataFrame(response["daily"])
    df["time"] = pd.to_datetime(df["time"])

    current_year_num = date.today().year
    historical_df = df[df["time"].dt.year < current_year_num]
    current_year_df = df[df["time"].dt.year == current_year_num]

    return {
        "climatology": aggregate_monthly(historical_df),
        "current_year": aggregate_monthly(current_year_df),
    }
