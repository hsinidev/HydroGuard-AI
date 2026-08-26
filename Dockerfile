# Multi-Stage Dockerfile for HydroGuard AI

# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --prefer-offline --no-audit
COPY frontend/ ./
RUN npm run build

# Stage 2: Production Python Backend + Static Frontend
FROM python:3.10-slim
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    GEMINI_MODEL_NAME=gemini-3.5-flash

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code and benchmark test cases
COPY backend/ ./backend/
COPY data/ ./data/
COPY IMPLEMENTATION_DECISIONS.md .

# Copy built static frontend from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose port
EXPOSE 8000

# Run FastAPI backend with Uvicorn
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
