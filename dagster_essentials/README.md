# Dagster University: Dagster Essentials

Material from the [Dagster Essentials](https://courses.dagster.io/courses/take/dagster-essentials/multimedia/48002083-what-s-data-engineering) course, taken June 2024.



## Lesson 1: Introduction

- Data engineers develop software to collect, store and manage data so that stakeholders and other applications can use that data
- Orchestrators manage complex pipelines for data engineers
- DAGs (directed acyclic graph) visualise workflows (repeatable defined running orders of processes)
- Task-centric workflows focus on how each step is performed
- Asset-centric workflows focus on what is produced at each step, giving the following benefits (according to Dagster):

    > **Context and visibility.** Everyone in your organization can understand the data lineage and how data assets relate to each other
    >
    > **Productivity.** By building a DAG that globally understands what data exists and why, asset-centric workflows allow for reusing assets without changing an existing sequence of tasks
    >
    > **Observability.** It’s easy to tell exactly why assets are out-of-date, whether it might be late upstream data or errors in code
    >
    > **Troubleshooting.** Every run and computation is tied to the goal of producing data, so debugging tools like logs are specific to the assets being produced



## Lesson 2: Prequisites & setup

*If using git, add both `de_env` and `dagster_university/data/` to the `.gitignore`.*

1. Create a virtual environment called `de_env` (`de` = Dagster Essentials)
1. Activate `de_env`
1. Install Dagster
1. Create the Dagster project from the pre-built example
1. Setup the default environment variables
1. Install the dependencies
1. Start the Dagster UI
1. Check [the instance via a browser]()

```bash
python3 -m venv de_env
source de_env/bin/activate
pip install 'dagster~=1.7'
dagster project from-example --example project_dagster_university_start --name dagster_university
cd dagster_university
cp .env.example .env
pip install -e ".[dev]"
dagster dev
```

This creates two module &mdash; `dagster_university` and `dagster_university_tests`. The `dagster_university` module contains the code needed for the Dagster project, and further modules of `assets`, `jobs`, `partitions`, `resources`, `schedules`, and `sensors`. The `assets` module also contains some files needed for the course material (`constants,py`, `metrics.py` and `trips.py`). 


```
dagster_university
├── __init__.py
├── assets
│   ├── __init__.py
│   ├── constants.py
│   ├── metrics.py
│   └── trips.py
├── jobs
├── partitions
├── resources
├── schedules
└── sensors
```

## Lesson 3: Software-defined assets

- Assets are objects like data tables and views, files, ml models or dbt models (and more)
- Dagster uses software-defined assets as the building block
- Assets are defined using the `@asset` decorator on a function that produces the object
- Assets have an asset key (name; defaults to the name of the function) and upstream dependencies (referenced by asset keys)


1. Define two assets in `assets/trips.py`

    ```python
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
    ```

    Comment string provides a description parsed in the Dagster UI.

1. Start the Dagster UI

    ```bash
    # from the dagster_university module
    dagster dev
    ```

1. Go to assets > view global asset lineage

1. Materialize the assets and confirm files are in `data/`

## Lesson 4: Asset dependencis

- Dependencies are used as project is expanded in a pipeline because assets will naturally need other assets to exist before they can be materialized
- Upstream assets have assets that rely on them, downstream assets rely on other assets

1. Create assets that load data into DuckDB and depend on the `taxi_trips_file` and `taxi_zones_file` assets

    ```python
    # Adding to trips.py...
    import duckdb
    import os

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
        sql_query = f"""
            create or replace table trips as (
            select
                LocationID as zone_id,
                Zone as zone,
                Borough as borough,
                the_geom as geom
            from '{constants.TAXI_ZONES_FILE_PATH}'
            );
        """
        with duckdb.connect(os.getenv("DUCKDB_DATABASE")) as conn:
            conn.execute(sql_query)
    ```

1. Materialize the datasets into the database

