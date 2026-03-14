# devops-docker-pipeline

![CI](https://github.com/your-username/devops-docker-pipeline/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)

A minimal FastAPI application containerized with Docker, with a full CI/CD pipeline via GitHub Actions.

---

## Overview

This project demonstrates a production-grade Python web service setup:

- RESTful API built with **FastAPI**
- **Multi-stage Docker build** with a non-root runtime user
- **PostgreSQL** service wired via Docker Compose
- **GitHub Actions** CI that runs tests and validates the Docker build on every push

---

## Features

- `GET /health` — liveness probe endpoint
- `GET /items` — retrieve all items from the in-memory store
- `POST /items` — add a new item (validated via Pydantic)
- Full pytest test suite using FastAPI's `TestClient`
- Multi-stage Dockerfile: slim runtime image, non-root user, layer caching
- `docker-compose.yml` with app + PostgreSQL + health checks
- GitHub Actions workflow: test → docker build (gated on passing tests)

---

## Tech Stack

| Component       | Technology                  |
|-----------------|-----------------------------|
| Web Framework   | FastAPI 0.110+              |
| ASGI Server     | Uvicorn                     |
| Testing         | pytest + httpx              |
| Containerization| Docker (multi-stage build)  |
| Orchestration   | Docker Compose              |
| CI/CD           | GitHub Actions              |
| Database        | PostgreSQL 15 (optional)    |

---

## API Endpoints

| Method | Path      | Description                  | Status Code |
|--------|-----------|------------------------------|-------------|
| GET    | /health   | Service liveness check       | 200         |
| GET    | /items    | List all items               | 200         |
| POST   | /items    | Create a new item            | 201         |

---

## Run Locally

```bash
# 1. Clone
git clone https://github.com/your-username/devops-docker-pipeline.git
cd devops-docker-pipeline

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn app.main:app --reload --port 8000
```

Visit: http://localhost:8000/docs for the interactive Swagger UI.

---

## Run with Docker

### Single container

```bash
docker build -t devops-docker-pipeline .
docker run -p 8000:8000 devops-docker-pipeline
```

### With Docker Compose (app + PostgreSQL)

```bash
docker-compose up --build
```

---

## Run Tests

```bash
pytest app/test_main.py -v
```

---

## Project Structure

```
devops-docker-pipeline/
├── app/
│   ├── main.py          # FastAPI application
│   └── test_main.py     # pytest test suite
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI pipeline
├── Dockerfile           # Multi-stage Docker build
├── docker-compose.yml   # App + PostgreSQL services
├── requirements.txt
└── README.md
```

---

## License

MIT
