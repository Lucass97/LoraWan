## Table of Contents

- [Requirements](#requirements)
   - [Setup Python enviroment](#setup-python-enviroment)
- [Dataset](#dataset)
   - [Acknowledgements](#acknowledgements)
   - [Columns](#columns)
- [Architecture](#architecture)
   - [batch-analysis](#batch-analysis)
   - [cassandra](#cassandra)
   - [kafka](#kafka)
   - [streaming](#streaming)
   - [visualization](#visualization)
- [How to Run](#how-to-run)
- [Results](#results)

## Requirements

In this section, we will discuss the software requirements for the project, including Docker, Python, and other necessary tools.

Used tools:

| Requirement                                                 | Docker Image              | Version | Description                                                                                                                   |
| ----------------------------------------------------------- | ------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [Docker](https://docs.docker.com)                           | N/A                       | 27.2.1  | A platform for automating the deployment of applications inside lightweight, portable containers.                             |
| [Docker Compose](https://docs.docker.com/compose/)       | N/A          | N/A   | Docker Compose is a tool for defining and running multi-container applications. It is the key to unlocking a streamlined and efficient development and deployment experience.                                                  |
| [Hadoop](https://hadoop.apache.org/docs/stable/)            | apache/hadoop:3.3.6                      | 3.3.6  | An open-source framework for distributed storage and processing of large datasets.                                            |

> Per installare [Docker](https://docs.docker.com)  si consiglia di seguire la seguente [guida](https://docs.docker.com/engine/install/ubuntu/). Seguendo la guida si aggiungerà alla propria distribuzione ubuntu la repository ufficiale di Docker. Una volta soddisfatto il requisito di Docker è possibile procedere con l'installazione del plugin Docker Compose seguendo quanto descritto in questa [documentazione](https://docs.docker.com/compose/install/linux/).


## Cose da fare
- scrievere i requirements di conda (con l'installazione di java versione 11 a partire dal channel forge)