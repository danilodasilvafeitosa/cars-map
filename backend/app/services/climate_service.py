import requests
import pandas as pd
from datetime import date, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential

BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
PARAMETERS = "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR"
COMMUNITY = "AG"

RENAME_MAP = {
    "T2M_MAX": "temperature_2m_max",
    "T2M_MIN": "temperature_2m_min",
    "T2M": "temperature_2m_mean",
    "PRECTOTCORR": "precipitation_sum",
}


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=4, max=30))
def fetch_climate_data(latitude: float, longitude: float, start_date: str, end_date: str):
    params = {
        "parameters": PARAMETERS,
        "community": COMMUNITY,
        "longitude": longitude,
        "latitude": latitude,
        "format": "JSON",
        "start": start_date,
        "end": end_date,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()


def aggregate_monthly(df: pd.DataFrame):
    df = df.copy()
    df["month"] = df.index.month
    return df.groupby("month").mean(numeric_only=True)


def get_talhao_climate_report_data(latitude: float, longitude: float):
    safe_date = date.today() - timedelta(days=7)
    climatology_start = safe_date.replace(year=safe_date.year - 30)
    current_year_num = date.today().year

    raw_response = fetch_climate_data(
        latitude, longitude,
        climatology_start.strftime("%Y%m%d"),
        safe_date.strftime("%Y%m%d"),
    )

    parameters = raw_response["properties"]["parameter"]
    df = pd.DataFrame(parameters)
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    df = df.rename(columns=RENAME_MAP)

    historical_df = df[df.index.year < current_year_num]
    current_year_df = df[df.index.year == current_year_num]

    return {
        "climatology": aggregate_monthly(historical_df),
        "current_year": aggregate_monthly(current_year_df),
    }