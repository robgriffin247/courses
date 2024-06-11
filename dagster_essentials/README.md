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

1. Create a virtual environment called `de_env` (`de` = Dagster Essentials)
1. Activate `de_env`
1. Install Dagster
1. Create the Dagster project from the pre-built example
1. Setup the default environment variables
1. Install the dependencies
1. Spin up a Dagster webserver
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

```bash
.
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

