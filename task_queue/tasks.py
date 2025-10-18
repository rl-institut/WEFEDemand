import os
import traceback
import json
from contextlib import contextmanager

from celery import Celery
from celery.utils.log import get_task_logger

from task_queue.demo.ramp_simulation_demo import main as run_ramp_simulation


logger = get_task_logger(__name__)
CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

CELERY_TASK_NAME = os.environ.get("CELERY_TASK_NAME", "grid")

app = Celery(CELERY_TASK_NAME, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@contextmanager
def temporary_env(**items):
    """Temporarily set environment variables."""
    old = {}
    try:
        for k, v in items.items():
            old[k] = os.environ.get(k)
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = str(v)
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


@app.task(name=f"dev.run_simulation")
def run_simulation(simulation_input: dict,) -> dict:
    logger.info("Start new simulation")

    kobo_token = os.getenv("KOBO_TOKEN")
    if not kobo_token:
        raise RuntimeError("KOBO_TOKEN is not set in worker environment")

    survey_id = simulation_input.get("survey_id", os.getenv("SURVEY_KEY"))

    # set SURVEY_KEY only for the duration of this task
    with temporary_env(SURVEY_KEY=survey_id):
        logger.info("Starting simulation (survey_id=%s, kobo_token_present=%s)",
                    survey_id, bool(kobo_token))

        try:
            agg_mean = run_ramp_simulation(simulation_input)
            simulation_output = {"data": agg_mean.to_dict(orient="list")}
        except Exception as e:
            logger.error(
                "An exception occured in the simulation task: {}".format(
                    traceback.format_exc()
                )
            )
            simulation_output = json.dumps(dict(
                SERVER=CELERY_TASK_NAME,
                ERROR="{}".format(traceback.format_exc()),
                INPUT_JSON=simulation_input,
            ))
        return simulation_output
