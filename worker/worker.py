import redis
import time
import os
import sys

# Force unbuffered logs (VERY IMPORTANT in Docker)
sys.stdout.reconfigure(line_buffering=True)

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

print("🚀 Worker started and waiting for jobs...")

def process_job(job_id):
    print(f"📦 Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"✅ Done: {job_id}")

while True:
    job = r.brpop("jobs", timeout=10)

    if job:
        _, job_id = job
        process_job(job_id)
    else:
        print("⏳ No jobs in queue, waiting...")