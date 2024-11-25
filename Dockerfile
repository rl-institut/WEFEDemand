FROM python:3.11.10

RUN echo POSTGRES
ENV APP_ROOT=/src
ENV CONFIG_ROOT=/config
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir ${CONFIG_ROOT}
COPY requirements/ ${CONFIG_ROOT}/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r ${CONFIG_ROOT}/deploy.txt

RUN pip install flower
RUN pip install redis
WORKDIR ${APP_ROOT}

ADD task_queue ${APP_ROOT}

RUN adduser appuser --system --no-create-home --shell /bin/sh \
    && chown -R appuser ${APP_ROOT}
USER appuser
