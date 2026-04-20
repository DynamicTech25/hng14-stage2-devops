## Fix 1
File: api/main.py
Issue: FastAPI dependency not installed causing ModuleNotFoundError
Fix: Created virtual environment and installed dependencies using requirements.txt

## Fix 2
File: api/main.py
Issue: No root endpoint defined, causing "Not Found" at base URL
Fix: Added a root ("/") endpoint for basic health response

## Fix 3 — Redis container not running
File: environment / infrastructure
Issue: Worker failed with connection refused
Fix: Started Redis using Docker on port 6379

## Fix 4 — Worker appeared idle
File: worker/worker.py
Issue: Worker seemed unresponsive
Fix: Confirmed correct blocking behavior using Redis queue

## Fix 5 — System integration validated
Issue: Uncertainty if worker actually processes jobs
Fix: Verified full pipeline via Redis → Worker execution logs

## Fix 6 - Redis Connection Host Misconfiguration
Issue: Services initially attempted to connect to Redis using incorrect or inconsistent hostnames (e.g. localhost or missing service name), causing connection failures inside Docker containers.
Fix: Updated Redis host to Docker service name: redis.Redis(host="redis", port=6379)

## Fix 7 - Worker Not Processing Jobs (Silent Execution)
Issue: Worker appeared “running” but produced no logs or job processing visibility due to:
lack of logging feedback
stdout buffering in Docker
Fix: Added explicit logging and unbuffered output:
import sys
sys.stdout.reconfigure(line_buffering=True)
print("Worker started and waiting for jobs...")

## Fix 8 - Frontend Undefined Job ID 
Issue: Frontend displayed Submitted: undefined because API response was returned as a raw string instead of an object.
Fix: Standardized API response format:
res.json({ job_id: response.data.job_id });

## Fix 9 - Hardcoded API URL in Frontend
File: frontend/app.js
Issue: Frontend used:
const API_URL = "http://localhost:8000";
Fix: Replaced with environment variable:
const API_URL = process.env.API_URL || "http://api:8000";

## Fix 10 - Docker Compose Service Startup Order Issue
File: docker-compose.yml
Issue: Services started before Redis was fully ready, causing intermittent connection failures.
Fix:Added Redis healthcheck and dependency condition:
depends_on:
  redis:
    condition: service_healthy 

## Fix 11 - Frontend API Response Parsing Mismatch
File: frontend/app.js
Issue: Frontend expected structured JSON but received inconsistent response format.
Fix: Standardized API responses across backend:
return {"job_id": job_id}

## Fix 12 - Docker Networking Confusion (Localhost Misuse)
Issue: Using localhost inside containers caused cross-service communication failure.
Fix: Replaced all internal communication with Docker service names:
api
redis
frontend
