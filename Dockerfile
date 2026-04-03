# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc postgresql-client libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code only (no Dockerfile, docs, or other repo files)
COPY src/ ./src/

# Expose port (must match uvicorn --port)
EXPOSE 5000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]
