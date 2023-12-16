import os
from pathlib import Path

from loguru import logger

from src.utils.image_creation.cutetext import grab_cute_text
from src.utils.image_creation.img_grab import grab_cute_img, save_url
from src.utils.image_creation.text_on_img import add_txt_to_image


def image_creator(iterations: int):
    for _ in range(iterations):
        url = grab_cute_img()
        save_url(url)

    logger.info(f"Grabbed {iterations} images")

    directory = "src/received_imgs"
    for filename in os.listdir(directory):
        fpath = Path(os.path.join(directory, filename))

        cute_txt = grab_cute_text()
        add_txt_to_image(fpath, cute_txt)

    logger.success(f"Added text to all images")


if __name__ == "__main__":
    image_creator(3)
