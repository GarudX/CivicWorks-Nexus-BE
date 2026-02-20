# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory (optional, but good practice)
RUN mkdir -p logs

# Expose port (Cloud Run will set PORT env variable)
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Run the application with uvicorn
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1
