import requests
from . import constants
from dagster import asset

@asset
def taxi_trips_file() -> None:
    """Raw parquet files for taxi trips"""
    month_to_fetch = "2023-03"
    response = requests.get(f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet")

    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), "wb") as f:
        f.write(response.content)

@asset
def taxi_zones_file() -> None:
    """Raw parquet files for taxi zones"""
    response = requests.get("https://data.cityofnewyork.us/api/views/755u-8jsi/rows.csv?accessType=DOWNLOAD")

    with open(constants.TAXI_ZONES_FILE_PATH, "wb") as f:
        f.write(response.content)
