import os
import logging
import requests as req
from requests_toolbelt.multipart.encoder import MultipartEncoder

logging.basicConfig(level=logging.INFO)

base_url = "https://mqtt2telegram.projects.royz.cc/api/v1.0"

login = os.getenv('TG_USER')
password = os.getenv('TG_PASS')


def send_message(topic, message):
    logging.info(f"send_message({topic}, {message})")

    json = {
        "topic": topic,
        "payload": message
    }

    res = req.post(f"{base_url}/send", auth=(login, password), json=json)
    logging.info(f"http: {res.status_code}")
    return res.status_code, res.json()


def send_image(topic, filename):
    logging.info(f"send_image({topic})")

    form = MultipartEncoder(
        fields={'topic': topic,
                'image': ('filename', open(filename, 'rb'), 'image/jpeg')}
    )

    headers = {
        'content-type': form.content_type
    }

    res = req.post(f"{base_url}/sendImage", auth=(login, password), data=form, headers=headers)
    logging.info(f"http: {res.status_code} {res.reason}")
    return res.status_code, res.json()
