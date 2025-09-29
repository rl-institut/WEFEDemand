FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir .

# Set the PYTHONPATH environment variable to include the src directory
ENV PYTHONPATH=/app/src/wefe_demand:$PYTHONPATH

# Expose port
EXPOSE 5000

# Run with Gunicorn + Uvicorn
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "demo.app:app", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2"]
