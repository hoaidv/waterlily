This file describes the system under distributed perspective.
This is the one of the most abstract level of the system.

# Components

## Benchmark scripts

Benchmark scripts are in `{PROJECT_ROOT}/experiment/`.
This will make calls to application layer using product ids, and export benchmark result.

Question: How to find product ids to make calls?

## Application

This is very simple:
- 1 API serving product details by product id.
- 1 API serving multiple product details by multiple product ids.

This component is to be scaled independently.

## Database

This is already setup with provided config `{PROJECT_ROOT}/experiment/mysql-config.json`
This is the component to be scaled independently in multiple ways for testing.

# Data flow

Benchmark scripts --requests--> Application --queries--> Database
Benchmark scripts <--responses-- Application <--results-- Database