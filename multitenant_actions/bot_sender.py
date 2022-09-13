import logging

import requests as req
from requests_toolbelt.multipart.encoder import MultipartEncoder

logging.basicConfig(level=logging.INFO)


class BotSender:
    BASE_URL = "https://mqtt2telegram.projects.royz.cc/api/v1.0"

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def send_message(self, topic, message):
        logging.info(f"send_message({topic}, {message})")

        json = {
            "topic": topic,
            "payload": message
        }

        res = req.post(f"{BotSender.BASE_URL}/send", auth=(self.login, self.password), json=json)
        logging.info(f"http: {res.status_code}")
        return res.status_code, res.json()

    def send_image(self, topic, filename):
        logging.info(f"send_image({topic})")

        form = MultipartEncoder(
            fields={'topic': topic,
                    'image': ('filename', open(filename, 'rb'), 'image/jpeg')}
        )

        headers = {
            'content-type': form.content_type
        }

        res = req.post(f"{BotSender.BASE_URL}/sendImage", auth=(self.login, self.password), data=form, headers=headers)
        logging.info(f"http: {res.status_code} {res.reason}")
        return res.status_code, res.json()
