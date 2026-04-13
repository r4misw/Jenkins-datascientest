# Jenkins Datascientest Demo

A lightweight CI/CD demo built with Flask, Docker, and Jenkins.

This repository contains a small Flask application, unit tests, a Docker image definition, and a declarative Jenkins pipeline.

## Stack

- Flask
- Docker
- Jenkins Pipeline

## Pipeline

The pipeline covers the following steps:

1. Build the application image on branches, pull requests, and tags
2. Run the unit tests automatically
3. Deploy the container locally on main
4. Publish the official Docker image only from a Git tag or GitHub release tag

The intended delivery flow is:

1. Open a pull request against main
2. Merge it once the jenkins/pr-ci status check is green
3. Create a release tag such as v1.0.0
4. Let Jenkins publish the matching Docker image tag automatically

The branch protection and review gate below are intentionally validated through temporary pull requests.

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