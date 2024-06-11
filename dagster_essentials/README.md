# Dagster University: Dagster Essentials

Material from the [Dagster Essentials](https://courses.dagster.io/courses/take/dagster-essentials/multimedia/48002083-what-s-data-engineering) course, taken June 2024.



## Lesson 1: Introduction

- Data engineers develop software to collect, store and manage data so that stakeholders and other applications can use that data
- Orchestrators manage complex pipelines for data engineers
- DAGs (directed acyclic graph) visualise workflows (repeatable defined running orders of processes)
- Task-centric workflows focus on how each step is performed
- Asset-centric workflows focus on what is produced at each step, giving the following benefits (according to Dagster):

    > - Context and visibility. Everyone in your organization can understand the data lineage and how data assets relate to each other
    > - Productivity. By building a DAG that globally understands what data exists and why, asset-centric workflows allow for reusing assets without changing an existing sequence of tasks
    > - Observability. It’s easy to tell exactly why assets are out-of-date, whether it might be late upstream data or errors in code
    > - Troubleshooting. Every run and computation is tied to the goal of producing data, so debugging tools like logs are specific to the assets being produced



## Lesson 2: Prequisites & setup