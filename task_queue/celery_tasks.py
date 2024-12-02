import asyncio


from celery_worker import worker


@worker.task(
    name="worker.task_demand",
    force=True,
    track_started=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 1, "countdown": 10},
)
def task_demand(user_id, project_id):
    # TODO provide here some argument of the task
    result = 42
    return result


@worker.task(bind=True, name="refresh")
def refresh():
    return "Hello world"


def get_status_of_task(task_id):
    status = worker.AsyncResult(task_id).status.lower()
    return status


def task_is_finished(task_id):
    status = get_status_of_task(task_id)
    if status in ["success", "failure", "revoked"]:
        return True
    else:
        return False
