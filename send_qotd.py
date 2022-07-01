import os
import requests as req


def get_quote(category="inspire"):
    url = f"https://quotes.rest/qod.json?category={category}"
    res = req.get(url).json()
    res = res['contents']['quotes'][0]
    return res['quote'], res['author']


def send_message(message):
    url = "https://mqtt2telegram.projects.royz.cc/api/v1.0/send"

    login = os.getenv('TG_USER')
    password = os.getenv('TG_PASS')

    topic = "qotd"

    json = {
        "topic": topic,
        "payload": message
    }

    res = req.post(url, auth=(login, password), json=json)
    return res.status_code, res.json()


if __name__ == "__main__":
    quote, author = get_quote()
    message = f"\n`\"{quote}\"`\n\t\t\t`-- {author}`"
    print(send_message(message))
