# ---------- STAGE 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


# ---------- STAGE 2: Final ----------
FROM python:3.11-slim

WORKDIR /app

# Install curl (safe + hadolint compliant)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Create user FIRST (fix ownership issues)
RUN useradd -m appuser

# Copy dependencies to correct home
COPY --from=builder /root/.local /home/appuser/.local

# Copy app
COPY . .

# Switch user
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

# Healthcheck (CI-safe)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
