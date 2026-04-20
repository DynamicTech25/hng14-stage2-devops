from fastapi import FastAPI
import redis
import uuid
import os

app = FastAPI()

# ---------- Redis Connection (SAFE + LAZY) ----------
def get_redis():
    return redis.Redis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379"),
        decode_responses=True
    )


# ---------- Health Check ----------
@app.get("/")
def root():
    return {"message": "API is running"}


# ---------- Create Job ----------
@app.post("/jobs")
def create_job():
    r = get_redis()

    job_id = str(uuid.uuid4())

    # push job to queue
    r.lpush("jobs", job_id)

    # store job status
    r.hset(f"job:{job_id}", "status", "queued")

    return {"job_id": job_id}


# ---------- Get Job Status ----------
@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    r = get_redis()

    status = r.hget(f"job:{job_id}", "status")

    if not status:
        return {"error": "not found"}

    return {
        "job_id": job_id,
        "status": status
    }