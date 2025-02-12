# Streaming Package

The Streaming Package provides a robust pipeline for real-time sensor data processing, analysis, and storage. It ensures continuous environmental monitoring through a distributed architecture leveraging Kafka, Spark, Hadoop, and InfluxDB. The pipeline processes raw sensor data, computes aggregate statistics, identifies correlations between sensor metrics, and stores the results for further analysis. The system operates asynchronously, offering reliability, fault tolerance, and efficient data management.

## Table of Contents

- [Streaming Pipeline](#streaming-pipeline)
  - [Analysis Phase](#1-analysis-phase)
  - [Writing Phase](#2-writing-phase)
- [Requirements](#requirements)
  - [Infrastructure Prerequisites](#infrastructure-prerequisites)
  - [Data Prerequisites](#data-prerequisites)
- [Execute Pipeline](#execute-pipeline)


## Streaming pipeline

The streaming pipeline is designed to process, analyze, and store real-time sensor data. It consists of two main phases:

### 1. Analysis Phase

The first phase handles the processing of incoming data through three fundamental operations. Initially, it processes raw data from Kafka, combining it with related metadata to create a structured dataset. Subsequently, the system calculates aggregate statistics for each classroom using a sliding time window, providing a synthetic view of monitored conditions. Finally, it computes correlations between different sensor metrics within the specified time window, enabling the identification of significant patterns or relationships among monitored variables.

### 2. Writing Phase

The second phase manages the storage of processed data across different storage systems. Data is stored in both HDFS and InfluxDB, ensuring redundancy and flexibility in data access.

Regarding HDFS, raw data is saved in Parquet format, utilizing an incremental writing mode that ensures data integrity through a checkpoint mechanism for fault tolerance.

InfluxDB stores three distinct types of information: raw sensor data, aggregate statistics, and correlation data. The writing of statistics and correlations is synchronized according to a predefined time window, ensuring a complete and consistent update of results with each processing cycle.

The pipeline operates in a fully asynchronous manner, continuing data processing until explicit process termination, thus ensuring continuous and reliable environmental monitoring.

## Requirements

The streaming application requires several infrastructure components to be running properly. These components are organized as Docker Compose services within the infrastructure directory.

### Infrastructure Prerequisites


The following clusters must be operational:

- #### Storage Infrastructure
    - **Hadoop** ([`infrastructure/hadoop`](../infrastructure/spark/docker-compose.yml)): Distributed storage system for maintaining raw sensor data and metadata
    - **InfluxDB** ([`infrastructure/influxdb`](../infrastructure/spark/docker-compose.yml)): Time-series database optimized for storing and querying processed sensor metrics and analytics results
- #### Processing Infrastructure
    - **Spark** ([`infrastructure/spark`](../infrastructure/spark)): Distributed computing engine responsible for real-time data processing and analytics execution
- #### Ingestion Infrastructure
    - **Kafka** ([`infrastructure/ingestion/kafka`](../infrastructure/ingestion/kafka/docker-compose.yml)): Message broker system that manages and coordinates incoming sensor data streams
    - **Server Proxy** ([`infrastructure/ingestion/server-proxy`](../infrastructure/ingestion/server-proxy/README.md)): Gateway service that handles the routing and management of incoming sensor data to Kafka

For convenience, all these services can be launched using:
```sh
./infrastructure/start-all.sh
```

For detailed configuration information, refer to each component's respective documentation in the infrastructure directory.

For convenience, you can launch the entire infrastructure using the provided script:

```sh
./infrastructure/start-all.sh
```

> For detailed information about the infrastructure setup and configuration, please refer to ([`infrastructure/README.md`](../infrastructure/README.md))

### Data Prerequisites

The system requires metadata about educational institutions (sensor installation locations) to be stored in Hadoop before starting the streaming process. This metadata can be uploaded using the provided script:

```sh
./data/upload-data.sh
```

This script will populate Hadoop with the necessary institution information that the streaming pipeline requires for data processing and analysis.

## Execute pipeline

The streaming application can be controlled through two shell scripts that handle the start and stop operations.

1. To initiate the streaming process:
    
    ```sh
    ./start-spark-streaming.sh [--background | --foreground]
    ```
    This script copies necessary files and configurations to the Spark master container and submits the streaming job.


    - `--background`: Starts the streaming job in the background. The script will submit the job and then return control to the terminal. This is the default behavior if no option is specified.
    - `--foreground:` Starts the streaming job in the foreground. The script will submit the job and keep the terminal attached to the Spark driver process, displaying logs directly. The script will run until the streaming job is manually stopped or encounters an error.


2. To terminate the streaming process:

    ```sh
    ./stop-spark-streaming.sh
    ```
    This script safely stops the running Spark streaming job by cleaning up resources and terminating the processes on the Spark master container.

> Note: Both scripts include status messages to indicate the progress and result of their operations. Any errors during execution will be clearly displayed with appropriate error messages.
