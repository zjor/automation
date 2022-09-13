import os
import logging
from pydantic import BaseModel
from datetime import datetime
from airtable import airtable
from apscheduler.schedulers.background import BlockingScheduler

from multitenant_actions.bot_sender import BotSender
from multitenant_actions.actions.send_qotd import send_qotd_action

logging.basicConfig(level=logging.INFO)

api_key = os.getenv('AIRTABLE_API_KEY')
base_id = os.getenv('AIRTABLE_BASE_ID')
table_id = os.getenv('AIRTABLE_TABLE_ID')

at = airtable.Airtable(base_id, api_key)


class JobFields(BaseModel):
    username: str
    password: str
    topic: str
    action: str
    schedule: str
    is_enabled: bool = False


class Job(BaseModel):
    id: str
    createdTime: datetime
    fields: JobFields


def parse_cron_schedule(cron):
    tokens = cron.split(' ')
    return {
        'minute': tokens[0],
        'hour': tokens[1],
        'day': tokens[2],
        'month': tokens[3],
        'day_of_week': tokens[4]
    }


def build_action_func(login: str, password: str, topic: str, action: str):
    bot = BotSender(login, password)
    if action == 'QOTD':
        return lambda: send_qotd_action(bot, topic)
    else:
        return lambda: bot.send_message(topic, f'Unknown action: {action}')


if __name__ == "__main__":
    scheduler = BlockingScheduler()

    for r in at.get(table_id)['records']:
        job = Job(**r)

        login = job.fields.username
        password = job.fields.password
        topic = job.fields.topic
        action = job.fields.action
        job_func = build_action_func(login, password, topic, action)

        if job.fields.is_enabled:
            scheduler.add_job(job_func, 'cron', **parse_cron_schedule(job.fields.schedule))
        else:
            logging.info(f'Job: {job.id} is disabled')

    scheduler.start()
