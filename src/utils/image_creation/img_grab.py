import base64
import random
import string

import requests
from loguru import logger
from openai import OpenAI

client = OpenAI()


def random_str(n: int) -> str:
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(n)
    )


def grab_cute_img():

    response = client.images.generate(
        model="dall-e-2",
        prompt="anm evil white siamese cat, scheming",
        size="1024x1024",
        quality="standard",
        # size="1024x1024",
        n=1,
    )

    image_url = response.data[0].url
    return image_url


def save_url(url: str):
    response = requests.get(url)

    if response.status_code == 200:
        with open(f"src/images/received_imgs/output_{random_str(5)}.jpg", "wb") as f:
            f.write(response.content)
        logger.info("Saved image")
    else:
        logger.error("Unable to retrieve image")


if __name__ == "__main__":
    img = grab_cute_img()
    save_url(img)
    print(img)
