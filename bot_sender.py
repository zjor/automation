import os
import requests as req

url = "https://mqtt2telegram.projects.royz.cc/api/v1.0/send"

login = os.getenv('TG_USER')
password = os.getenv('TG_PASS')


def send_message(topic, message):
    json = {
        "topic": topic,
        "payload": message
    }

    res = req.post(url, auth=(login, password), json=json)
    return res.status_code, res.json()
