import logging
import tempfile
import requests
from datetime import datetime
from PIL import Image

from multitenant_actions.bot_sender import BotSender

logging.basicConfig(level=logging.INFO)

base_url = "https://en.wikipedia.org/w/api.php"


def fetch_picture_of_the_day():
    date_iso = datetime.now().date().isoformat()
    title = "Template:POTD_protected/" + date_iso

    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "images",
        "titles": title
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    filename = data["query"]["pages"][0]["images"][0]["title"]
    return filename


def fetch_image_url(filename):
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "titles": filename
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    image_info = page["imageinfo"][0]
    image_url = image_info["url"]
    return image_url


def download_image(image_url):
    print(f"Downloading image: {image_url}")

    headers = {
        "user-agent": "cURL"
    }

    img_response = requests.get(image_url, headers=headers)
    content_length = img_response.headers['Content-Length']
    print(f"Content-Length: {content_length}")

    temp_file = tempfile.NamedTemporaryFile().name
    with open(temp_file, 'wb') as f:
        f.write(img_response.content)

    print(f"Saved to {temp_file}")

    return temp_file


def resize_image(filename, width):
    img = Image.open(filename)
    w, h = img.size
    resized_img = img.resize((width, round(h / w * width)))
    resized_filename = filename + "_small.jpg"
    resized_img.save(resized_filename)
    return resized_filename


def send_potd_action(sender: BotSender, topic: str):
    filename = fetch_picture_of_the_day()
    logging.info(f"Fetched image of the day: {filename}")

    image_url = fetch_image_url(filename)
    logging.info(f"Fetched image URL: {image_url}")

    temp_file = download_image(image_url)
    logging.info(f"Downloaded image to {temp_file}")

    resized_filename = resize_image(temp_file, 600)

    sender.send_image(topic, resized_filename)
