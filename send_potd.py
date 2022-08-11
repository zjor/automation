import tempfile
import requests
from datetime import datetime
from PIL import Image

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
    resized_filename = temp_file + "_small.jpg"
    resized_img.save(resized_filename)
    return resized_filename


if __name__ == "__main__":
    from bot_sender import send_image

    filename = fetch_picture_of_the_day()
    image_url = fetch_image_url(filename)
    temp_file = download_image(image_url)

    resized_filename = resize_image(temp_file, 600)

    send_image('qotd', resized_filename)
