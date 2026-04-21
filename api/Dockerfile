# ---------- STAGE 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies (no extra packages, clean install)
COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


# ---------- STAGE 2: Final ----------
FROM python:3.11-slim

WORKDIR /app

# Install curl (fixed for hadolint DL3008 + DL3015)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m appuser

# Switch to non-root user
USER appuser

# Ensure Python sees installed packages
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

# Healthcheck (clean + reliable)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl --fail http://localhost:8000 || exit 1

# Start app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
