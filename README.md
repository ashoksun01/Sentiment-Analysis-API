# Sentiment Analysis API - FastAPI, Docker, Kubernetes, and Azure Cloud

## Overview

This project is an end-to-end machine learning API that performs sentiment analysis on user-provided text inputs. The API is built using FastAPI, managed with Poetry for dependencies, containerized with Docker, orchestrated using Kubernetes, and designed for deployment on a cloud platform (e.g., Microsoft Azure). The API supports the following endpoints:

- **`/`**: A root GET endpoint that returns a "Not Found" response.
- **`/docs`**: A GET endpoint providing a browsable documentation UI (Swagger UI).
- **`/openapi.json`**: A GET endpoint returning a JSON object compliant with the OpenAPI specification.
- **`/health`**: A GET endpoint returning the status of the application.
- **`/bulk-predict`**: A POST endpoint that accepts a JSON payload containing a list of text inputs, performs sentiment analysis, and returns sentiment scores with "POSITIVE" and "NEGATIVE" labels and their confidence scores.

---

## Features
- **FastAPI** for building a robust and scalable RESTful API.
- **Poetry** for efficient dependency management and virtual environment handling.
- **Docker** for containerization, enabling easy deployment across different environments.
- **Kubernetes** for scalable orchestration of containers in a cloud environment.
- **Cloud-Ready Architecture**: Easily deployable on any cloud provider (e.g., Azure, AWS, GCP).
- **Real-Time Sentiment Analysis** using a pre-trained machine learning model.

---

## Repository Structure

- **`src/`**: Contains the FastAPI application code.
  - **`main.py`**: FastAPI application code.
  - **`model.py`**: Model loading and prediction logic.
- **`tests/`**: Contains test cases for API endpoints using pytest.
- **`Dockerfile`**: Configuration for building Docker images.
- **`pyproject.toml`**: Poetry configuration file for dependency management.
- **`k8s/`**: Kubernetes deployment configuration files for scalable cloud deployment.

---
