FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements/default.txt

# Set the PYTHONPATH environment variable to include the src directory
ENV PYTHONPATH=/app/src/wefe_demand:$PYTHONPATH

# Run the flask app for the API endpoint
CMD ["python", "demo/app.py"]
