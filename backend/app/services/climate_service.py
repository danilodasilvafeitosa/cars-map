import requests
import pandas as pd

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