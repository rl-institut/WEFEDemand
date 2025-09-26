FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements/default.txt

# Set the PYTHONPATH environment variable to include the src directory
ENV PYTHONPATH=/app/src/wefe_demand:$PYTHONPATH

# Expose port
EXPOSE 5000

# Run with Gunicorn + Uvicorn
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2"]