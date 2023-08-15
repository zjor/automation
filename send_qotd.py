import os
import json
import requests as req
from bot_sender import send_message

qotd_token = os.getenv("QOTD_TOKEN")

def get_quote(category="inspire"):
    url = f"https://quotes.rest/qod.json?category={category}"
    
    headers = {
        "X-TheySaidSo-Api-Secret": qotd_token
    }

    res = req.get(url, headers=headers).json()
    print(json.dumps(res, indent=2))
    res = res['contents']['quotes'][0]
    return res['quote'], res['author']


if __name__ == "__main__":
    topic = 'qotd'
    quote, author = get_quote()
    message = f"\n`\"{quote}\"`\n\t\t\t`-- {author}`"
    print(send_message(topic, message))
