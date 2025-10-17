import os
import time
import traceback
import json
from copy import deepcopy
from celery import Celery
from celery.utils.log import get_task_logger

from demo.ramp_simulation_demo import main as run_ramp_simulation


logger = get_task_logger(__name__)
CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

CELERY_TASK_NAME = os.environ.get("CELERY_TASK_NAME", "grid")

app = Celery(CELERY_TASK_NAME, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@app.task(name=f"dev.run_simulation")
def run_simulation(simulation_input: dict,) -> dict:
    logger.info("Start new simulation")
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
