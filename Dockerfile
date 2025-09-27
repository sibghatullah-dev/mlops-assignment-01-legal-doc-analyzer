FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies including wget and unzip for model download
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY app/requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# Copy application code
COPY app/ .

# Create model directory and download model files from Google Drive
RUN mkdir -p model

# Download model files automatically during build
RUN echo "Downloading model files from Google Drive..." && \
    wget --no-check-certificate "https://drive.google.com/uc?export=download&id=1QqgKPDfdIdgMuBGSpcM5DPEL2BHsVHHg" -O model.zip && \
    unzip -q model.zip -d ./model/ && \
    rm model.zip && \
    echo "Model files downloaded successfully" || \
    echo "Model download failed, will use mock model"

# Copy any existing local model files as fallback
COPY app/model/ ./model/

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120"]
