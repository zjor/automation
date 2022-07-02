import requests as req
from bot_sender import send_message


def get_quote(category="inspire"):
    url = f"https://quotes.rest/qod.json?category={category}"
    res = req.get(url).json()
    res = res['contents']['quotes'][0]
    return res['quote'], res['author']


if __name__ == "__main__":
    topic = 'qotd'
    quote, author = get_quote()
    message = f"\n`\"{quote}\"`\n\t\t\t`-- {author}`"
    print(send_message(topic, message))
