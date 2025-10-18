FROM python:3.11-slim-bookworm

# System deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends git coinor-cbc graphviz && \
    rm -rf /var/lib/apt/lists/*

# Python deps
COPY task_queue/requirements.txt /tmp/requirements.txt
COPY requirements/default.txt /tmp/default.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    pip install --no-cache-dir -r /tmp/default.txt

# App code (copy everything once, as root)
WORKDIR /queue
COPY . /queue
# Shared src for imports
COPY src /src
ENV PYTHONPATH=/src:$PYTHONPATH

# Non-root user
RUN useradd --create-home appuser && \
    chown -R appuser:appuser /queue /src
USER appuser

# Celery worker
ENTRYPOINT celery -A task_queue.tasks worker --loglevel=info --queues=${CELERY_TASK_NAME}