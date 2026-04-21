# ---------- STAGE 1: Builder ----------
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# ---------- STAGE 2: Production ----------
FROM node:18-alpine

WORKDIR /app

# Install curl (hadolint-safe)
RUN apk add --no-cache curl

# Create user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy ONLY necessary built files (cleaner + safer)
COPY --from=builder /app /app

USER appuser

EXPOSE 3000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

CMD ["npm", "start"]
