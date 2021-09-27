import timer

import util
import os
from telegram.ext import CallbackContext

UPDATE_TIME_FILENAME = "jin_kuan_hair_update_time.csv"


def create_daily_job(job_queue, hour, minute, second, chat_id):
    """Creates a daily job with given hour, minute, second and chat_id"""
    time_for_alarm = util.return_time_object(hour, minute, second)
    dictionary = {"hour": hour, "minute": minute, "second": second, "chat_id": chat_id}

    name = f"{chat_id}_{hour:02d}{minute:02d}{second:02d}"
    job_queue.run_daily(timer.alarm, time_for_alarm, context=dictionary, name=name)

    # with open(UPDATE_TIME_FILENAME, "r") as file:
    #     with open("tempfile", "w") as output:
    #         for line in file:
    #             if chat_id not in line.split(","):
    #                 output.write(line)
    #
    # os.replace('tempfile', UPDATE_TIME_FILENAME)

    with open(UPDATE_TIME_FILENAME, "a") as file:
        file.write(f"{hour},{minute},{second},{chat_id}\n")


def init_daily_job(job_queue):
    chat_ids = []
    if os.path.exists(UPDATE_TIME_FILENAME):
        with open(UPDATE_TIME_FILENAME, "r") as file:
            lines = file.readlines()
            if lines:
                for line in lines:
                    hour, min, second, chat_id = [int(x) for x in line.split(",")]
                    create_daily_job(job_queue, hour, min, second, chat_id)
                    chat_ids.append(chat_id)
    return chat_ids


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True
