import logging
import requests as req
from multitenant_actions.bot_sender import BotSender

logging.basicConfig(level=logging.INFO)


# TODO: cache during 12h
def get_quote(category="inspire"):
    url = f"https://quotes.rest/qod.json?category={category}"
    res = req.get(url).json()
    res = res['contents']['quotes'][0]
    return res['quote'], res['author']


def send_qotd_action(sender: BotSender, topic: str):
    quote, author = get_quote()
    message = f"\n`\"{quote}\"`\n\t\t\t`-- {author}`"
    sender.send_message(topic, message)
