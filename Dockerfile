# Stage 1: Build the Next.js Frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
# Build production static or node assets
RUN npm run build

# Stage 2: Final Runner with Python Backend + Node Runtime
FROM python:3.11-slim

# Install system dependencies for EasyOCR & Node.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libglib2.0-0 \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK stopwords ahead of time
RUN python -c "import nltk; nltk.download('stopwords', quiet=True)"

# Pre-download EasyOCR English weights so it doesn't download on user clicks
RUN python -c "import easyocr; easyocr.Reader(['en'], gpu=False)"

# Copy backend code
COPY backend.py .

# Copy built frontend assets
COPY --from=frontend-builder /app/frontend ./frontend

# Hugging Face Spaces exposes port 7860
EXPOSE 7860

# Startup script to run FastAPI on 8000 and Next.js on 7860
CMD sh -c "uvicorn backend:app --host 0.0.0.0 --port 8000 & cd frontend && PORT=7860 HOSTNAME=0.0.0.0 npm start"