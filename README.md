# HNG14-stage2-devops CI/CD Pipeline
## Overview

This project demonstrates a production-ready multi-service application built with a complete CI/CD pipeline using GitHub Actions.

# The system consists of:

- A FastAPI backend (API)
- A Redis queue
- A Worker service
- A Frontend interface

The pipeline enforces code quality, automated testing, containerization, security scanning, integration testing, and deployment simulation.



## Tech Stack
- Python (FastAPI)
- Redis
- Docker and Docker Compose
- GitHub Actions (CI/CD)
- Trivy (Security scanning)
- Pytest (Unit testing)
- Flake8 (Python Linting)
- ESLint (JavaScript Linting)
- Hadolint (Dockerfile Linting)

## CI/CD Pipeline Architecture
Lint → Test → Build → Security Scan → Integration Test → Deploy

## Pipeline Breakdown
1. Lint
- Python linting using flake8
- JavaScript linting using eslint
- Dockerfile linting using hadolint

2. Test
- Unit tests executed using pytest
- Redis is mocked for isolation
- Test coverage report generated
- Coverage uploaded as pipeline artifact

3. Build
- Docker images built for:
  - API
  - Worker
  - Frontend
  - Images tagged with: latest
  - Git commit SHA

4. Security Scan
- Images scanned using Trivy
- Pipeline fails on CRITICAL vulnerabilities
- Results exported as SARIF
- Uploaded to GitHub Security tab

5. Integration Test
- Full stack started inside CI environment
- Job submitted through API
- System polled until completion
- Final state validated
- Stack torn down after test

6. Deploy (Simulated Rolling Update)
- Runs only on main branch
- New container starts first
- Health check is performed
- Old container is stopped only after success
- If health check fails within 60 seconds → rollback

## How to Run Locally
docker compose up --build
pytest api -v

##  Running the Project Locally (From Scratch)

This guide allows you to run the entire application stack on a clean machine.


### 📌 Prerequisites

Ensure the following are installed:

- Docker (v20+)
- Docker Compose (v2+)
- Git
- Python (3.11+) *(optional for local testing)*

Verify installations:

```bash
docker --version
docker compose version
git --version
```

## Clone the Repository
git clone https://github.com/DynamicTech25/hng14-stage2-devops.git
cd hng14-stage2-devops

## Create Environment File
- Create a .env file inside the api/ directory:
   - touch api/.env.example
- Add:
   - REDIS_HOST=redis
   - REDIS_PORT=6379

## Build and Start All Services
using: docker compose up --build

- This will start:

  - API (FastAPI)
  - Redis
  - Worker
  - Frontend

## Wait for Services to Be Ready

- You should see logs like:
  - API started on http://localhost:8000
  - Connected to Redis
  - Worker listening for jobs

## Verify the Application

- Open your browser:

  - http://localhost:8000

Expected response:

{
  "message": "Hello World"
}

## Test Job Processing

- Submit a job:

curl -X POST http://localhost:8000/jobs

- Then check status:

curl http://localhost:8000/jobs/<job_id>

- Expected result:

{
  "status": "completed"
}

## Stop the Application
docker compose down

## Security Note
All container images are scanned using Trivy.  
The pipeline fails on CRITICAL vulnerabilities.  
Scan results are uploaded to GitHub Security (Code Scanning).

## Production Readiness

This application is production-ready in terms of:
- Containerized architecture
- Automated CI/CD pipeline
- Security scanning
- Integration testing
- Rolling deployment strategy with health checks

This Deployment is simulated within GitHub Actions and can be extended to cloud platforms like AWS, Azure, or GCP.

## Architecture Overview
- User → Frontend → API → Redis → Worker → Result

## Notes
- No secrets are hardcoded in the repository
- .env is not tracked
- Pipeline runs entirely on GitHub free tier
- No external cloud infrastructure required

# In Conclusion, This project demonstrates a complete DevOps workflow, including:
- Automation
- Testing
- Security
- Deployment strategy

# Screenshots
### CI Pipeline Success
![CI](screenshots/CI-pipeline-success.png)

### Security Scan (Trivy)
![Security](screenshots/security-scanning-trivy.png)
