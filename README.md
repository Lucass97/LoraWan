## Table of Contents

- [Table of Contents](#table-of-contents)
- [Requirements](#requirements)
  - [Setup Python enviroment](#setup-python-enviroment)
- [Architecture](#architecture)
  - [Ingestion](#ingestion)
    - [`kafka`](#kafka)

## Requirements

In this section, we will discuss the software requirements for the project, including Docker, Python, and other necessary tools.

Used tools:

| Requirement                                                 | Docker Image              | Version | Description                                                                                                                   |
| ----------------------------------------------------------- | ------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [Docker](https://docs.docker.com)                           | N/A                       | 27.2.1  | A platform for automating the deployment of applications inside lightweight, portable containers.                             |
| [Docker Compose](https://docs.docker.com/compose/)       | N/A          | N/A   | Docker Compose is a tool for defining and running multi-container applications. It is the key to unlocking a streamlined and efficient development and deployment experience.                                                  |
| [Hadoop](https://hadoop.apache.org/docs/stable/)            | apache/hadoop:3.3.6                      | 3.3.6  | An open-source framework for distributed storage and processing of large datasets.                                            |

> Per installare [Docker](https://docs.docker.com)  si consiglia di seguire la seguente [guida](https://docs.docker.com/engine/install/ubuntu/). Seguendo la guida si aggiungerà alla propria distribuzione ubuntu la repository ufficiale di Docker. Una volta soddisfatto il requisito di Docker è possibile procedere con l'installazione del plugin Docker Compose seguendo quanto descritto in questa [documentazione](https://docs.docker.com/compose/install/linux/).

> For further details, refer to the [requirements.txt](environment/requirements.txt) file.


### Setup Python enviroment

> To install conda and/or setup server, refer to the [setup](.github/workflows/README.md) guide.

1. Clone the repository:
   ```shell
   git clone https://github.com/Lucass97/repository.git
   ```
2. Move into the project directory:
   ```shell
   cd repository
   ```
3. Create the environment:
    ```shell
    conda env create -f ./environment/environment.yml
    ```
4. Activate the conda environment:
    ```shell
    conda activate IoT-LoraWAN
    ```

## Architecture

### Ingestion

#### [`kafka`](kafka)

The `kafka` package implements a solution that leverages Apache Kafka, a distributed streaming platform, as part of the Lambda architecture. This package contains the necessary Python code to interact with Kafka, enabling real-time data streaming and processing.

The [kafka/producer.py](infrastructure/ingestion/kafka/producer.py) script serves as the Kafka producer. It establishes a connection to the Kafka brokers (`kafka1` and `kafka2`) defined in the Docker Compose configuration ([kafka/docker-compose.yml](infrastructure/ingestion/kafka/docker-compose.yml)). Additionally, the Docker Compose configuration includes instances of ZooKeeper, which are essential components for maintaining the coordination and synchronization of the Kafka cluster. The Kafka brokers, along with the ZooKeeper ensemble, form a distributed and fault-tolerant Kafka cluster. This cluster setup allows for high availability and scalability, ensuring the seamless handling of data streams and fault tolerance in case of any node failures within the cluster.