FROM docker.io/python:3.12.9-slim-bookworm

RUN apt-get update && \
    apt-get install -y git && \
    apt-get install coinor-cbc -y && \
    apt-get install graphviz -y

COPY task_queue/requirements.txt /tmp/

RUN python -m pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

run echo $(pip freeze)
COPY . /queue

# avoid running as root user
RUN useradd --create-home appuser
RUN chown -R appuser /queue
USER appuser

WORKDIR /queue

ENTRYPOINT celery -A task_queue.tasks worker --loglevel=info --queues=${CELERY_TASK_NAME}