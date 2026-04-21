# ---------- STAGE 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------- STAGE 2: Final ----------
FROM python:3.11-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy app code
COPY . .

# Create non-root user properly
RUN adduser --disabled-password --gecos "" appuser

# Use non-root user
USER appuser

# Ensure Python can find installed packages
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1

# Start app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]