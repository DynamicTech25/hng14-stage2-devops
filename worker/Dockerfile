# ---------- STAGE 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------- STAGE 2: Final ----------
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages
COPY --from=builder /root/.local /root/.local

# Copy app code
COPY . .

# Create non-root user (proper format)
RUN adduser --disabled-password --gecos "" appuser

USER appuser

# Ensure Python finds installed packages
ENV PATH=/root/.local/bin:$PATH

CMD ["python", "worker.py"]