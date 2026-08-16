import requests
import pandas as pd
from datetime import date, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential

CLIMATE_API_URL="https://archive-api.open-meteo.com/v1/archive"

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=4, max=30))
def fetch_climate_data(coordinates: list[tuple[float, float]], start_date: str, end_date: str):
    latitudes, longitudes = zip(*coordinates)
    latitude_str = ",".join(str(lat) for lat in latitudes)
    longitude_str = ",".join(str(lon) for lon in longitudes)

    params = {
        "latitude": latitude_str,
        "longitude": longitude_str,
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

def get_climate_report_data_batch(coordinates: list[tuple[float, float]]):
    safe_date = date.today() - timedelta(days=7)
    climatology_start = safe_date.replace(year=safe_date.year - 30)
    current_year_num = date.today().year

    response = fetch_climate_data(coordinates, climatology_start.isoformat(), safe_date.isoformat())

    results = []
    for location_data in response:
        df = pd.DataFrame(location_data["daily"])
        df["time"] = pd.to_datetime(df["time"])
        
        historical_df = df[df["time"].dt.year < current_year_num]
        current_year_df = df[df["time"].dt.year == current_year_num]

        results.append({
        "climatology": aggregate_monthly(historical_df),
        "current_year": aggregate_monthly(current_year_df),
    })

    return results
