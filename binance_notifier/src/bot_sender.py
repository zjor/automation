import logging

import requests as req

from settings import get_app_settings

logging.basicConfig(level=logging.INFO)

url = "https://mqtt2telegram.projects.royz.cc/api/v1.0/send"


def send_message(topic, message):
    logging.info(f"send_message({topic}, {message})")

    json = {"topic": topic, "payload": message}

    login, password = (get_app_settings().TG_USER,
                       get_app_settings().TG_PASS)

    res = req.post(url, auth=(login, password), json=json)
    logging.info(f"http: {res.status_code}")
    return res.status_code, res.json()
