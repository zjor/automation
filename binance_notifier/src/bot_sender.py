import os
import logging
import requests as req

logging.basicConfig(level=logging.INFO)

url = "https://mqtt2telegram.projects.royz.cc/api/v1.0/send"

login = os.getenv("TG_USER")
password = os.getenv("TG_PASS")


def send_message(topic, message):
    logging.info(f"send_message({topic}, {message})")

    json = {"topic": topic, "payload": message}

    res = req.post(url, auth=(login, password), json=json)
    logging.info(f"http: {res.status_code}")
    return res.status_code, res.json()
