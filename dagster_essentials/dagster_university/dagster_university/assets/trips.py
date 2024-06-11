import requests
from . import constants
from dagster import asset

import duckdb
import os

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


@asset(
    deps=["taxi_trips_file"]
)
def taxi_trips() -> None:
    """
    The raw taxi trips dataset, loaded into a DuckDB database
    """
    sql_query = """
        create or replace table trips as (
        select
            VendorID as vendor_id,
            PULocationID as pickup_zone_id,
            DOLocationID as dropoff_zone_id,
            RatecodeID as rate_code_id,
            payment_type as payment_type,
            tpep_dropoff_datetime as dropoff_datetime,
            tpep_pickup_datetime as pickup_datetime,
            trip_distance as trip_distance,
            passenger_count as passenger_count,
            total_amount as total_amount
        from 'data/raw/taxi_trips_2023-03.parquet'
        );
    """
    with duckdb.connect(os.getenv("DUCKDB_DATABASE")) as conn:
        conn.execute(sql_query)

        
@asset(
    deps=["taxi_zones_file"]
)
def taxi_zones() -> None:
    """
    The raw taxi zones dataset, loaded into a DuckDB database
    """
    sql_query = """
        create or replace table trips as (
        select
            LocationID as zone_id,
            Zone as zone,
            Borough as borough,
            the_geom as geom
        from 'data/raw/taxi_zones.csv'
        );
    """
    with duckdb.connect(os.getenv("DUCKDB_DATABASE")) as conn:
        conn.execute(sql_query)