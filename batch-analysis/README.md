# Batch Analysis Package

The Batch Analysis Package provides a pipeline for offline processing and analysis of sensor data. It leverages Spark for distributed computation and PostgreSQL for storing the results.  The pipeline reads raw sensor data from HDFS, performs aggregations and calculations, and writes the results to a PostgreSQL database.

## Table of Contents

- [Data Download](#data-download)
- [Batch Analysis Pipeline](#batch-analysis-pipeline)
  - [1. Analysis Phase](#1-analysis-phase)
  - [2. Writing Phase](#2-writing-phase)
- [Requirements](#requirements)
  - [Infrastructure Prerequisites](#infrastructure-prerequisites)
  - [Data Prerequisites](#data-prerequisites)
  - [Environment Variables](#environment-variables)
- [Getting Started](#getting-started)
  - [Data Downloader](#data-downloader)
  - [Batch Analysis Script](#batch-analysis-script)


## Data Download

The data download phase retrieves data from HDFS storage and prepares it for analysis. The data is downloaded as parquet files and converted into a local CSV file within the Spark container. A specific profile can be selected to filter the data for further processing. This phase is also crucial for downloading data that may be used for training machine learning models.

## Batch Analysis Pipeline

The batch analysis pipeline processes and stores sensor data in two main phases: analysis and writing.

### 1. Analysis Phase

In this phase, the data is processed and analyzed using Spark. The system performs two core operations:
- **Aggregation by Class and Institution**: The data is grouped by class and institution, allowing for the calculation of aggregate statistics specific to each group.
- **Time-based Aggregation**: The data is further grouped based on time periods, such as week of the year or month and year, to analyze trends over different time intervals.

These operations allow the pipeline to generate insights into both the temporal and categorical aspects of the data.

### 2. Writing Phase

The writing phase focuses on making the results of the analysis accessible for querying. The aggregated statistics are stored in a PostgreSQL database, which enables the retrieval of insights through SQL queries. This facilitates the construction of dashboards or the integration of the data into chatbots powered by large language models (LLMs), enabling real-time interaction and data-driven decision-making.

## Requirements

The batch analysis application depends on several infrastructure components for proper operation. These components are organized as Docker Compose services within the infrastructure directory.

### Infrastructure Prerequisites

The following clusters must be up and running:

- #### Storage Infrastructure
    - **Hadoop** ([`infrastructure/hadoop`](../infrastructure/spark/docker-compose.yml)): Distributed storage system for storing raw sensor data and metadata.
    - **PostgreSQL** ([`infrastructure/postgresql`](../infrastructure/spark/docker-compose.yml)): Relational database optimized for storing and querying processed sensor metrics and analytics results.

- #### Processing Infrastructure
    - **Spark** ([`infrastructure/spark`](../infrastructure/spark)): Distributed computing engine responsible for batch data processing and executing analytics.

For convenience, all these services can be started using the following command:

```sh
./infrastructure/start-all.sh
```

You can either refer to the individual configuration files for each component to understand their setup or consult the global configuration in the [(`infrastructure/README.md`)](../infrastructure/README.md) file for a comprehensive overview of the infrastructure setup and configuration.

### Data Prerequisites

Before starting the batch analysis process, the system requires the raw sensor data in Parquet format to be available in HDFS. To achieve this, the following script should be executed within the `streaming` package:

```sh
./start-spark-streaming.sh [--background | --foreground]
```

This will ensure that the necessary raw data is processed and stored in HDFS. For further details on the setup and configuration of this process, please refer to the [(`streaming/README.md`)](../streaming/README.md) file.

### Environment Variables

Certain environment variables are required for all Spark jobs within the project. These variables are defined in the `env/spark.env` file and must be sourced for proper configuration. 

It is highly recommended to review the [(`env/README.md`)](../env/README.md) file to ensure that the environment variables are correctly configured for all Spark-related tasks in the project.


### Getting Started

This section provides an overview of how the main scripts within the package work.

1. #### Data Downloader

    ```bash
    ./spark-downloader.sh [--background | --foreground]
    ```
    This script runs the data download job (`spark-downloader.py`). It reads the raw Parquet data stored in HDFS, processes it, and saves it in CSV format. The goal of this process is to download and structure the data so that it can potentially be used for training a machine learning model.

    - `--background`: Runs the download process in the background. The script will start the download and return control to the terminal. This is the default behavior if no option is specified.
    - `--foreground`: Runs the download process in the foreground, keeping the terminal attached to the process and displaying logs directly. The script will run until the download completes or encounters an error.

2. #### Batch Analysis

    ```bash
    ./start-spark.sh [--background | --foreground]
    ```

    This script runs the Spark job (`start-spark.py`). It reads the raw Parquet data stored in HDFS, performs the analysis, and writes the results to PostgreSQL.

    - `--background`: Starts the batch job in the background. The script will submit the job and then return control to the terminal. This is the default behavior if no option is specified.
    - `--foreground`: Starts the batch job in the foreground. The script will submit the job and keep the terminal attached to the Spark driver process, displaying logs directly. The script will run until the batch job completes or encounters an error.

> #### Notes:
> 1. Both scripts include status messages to indicate the progress and result of their operations. Any errors during execution will be clearly displayed with appropriate error messages.
> 2. These scripts copy necessary files and configurations to the Spark master container and submit the respective jobs.