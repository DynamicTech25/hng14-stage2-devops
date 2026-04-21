# ---------- STAGE 1: Builder ----------
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# ---------- STAGE 2: Production ----------
FROM node:18-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy built app from builder
COPY --from=builder /app /app

# Create non-root user (clean format)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

USER appuser

EXPOSE 3000

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:3000 || exit 1

CMD ["npm", "start"]