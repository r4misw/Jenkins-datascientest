# Jenkins Datascientest Demo

A lightweight CI/CD demo built with Flask, Docker, and Jenkins.

This repository contains a small Flask application, unit tests, a Docker image definition, and a declarative Jenkins pipeline.

## Stack

- Flask
- Docker
- Jenkins Pipeline

## Pipeline

The pipeline covers the following steps:

1. Build the application image on branches and pull requests
2. Run the unit tests automatically
3. Deploy the container locally on main
4. Wait for manual approval before publishing from main
5. Push the image to Docker Hub only from main

## Repository Layout

- app.py: Flask application used in the demo
- test_main.py: unit tests for the application
- requirements.txt: Python dependencies
- Dockerfile: container image definition
- Jenkinsfile: declarative Jenkins pipeline

## Run Locally

```bash
docker build -t datascientestapi:local .
docker run -d -p 8000:8000 --name jenkins datascientestapi:local
curl http://127.0.0.1:8000/api/hello
```