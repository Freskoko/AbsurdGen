import os
from pathlib import Path

from loguru import logger

from utils.image_creation.cutetext import grab_arabic_text, grab_cute_text
from utils.image_creation.img_grab import grab_cute_img, save_url
from utils.image_creation.text_on_img import (
    add_random_images,
    add_random_text,
    add_txt_to_image,
)


def treat_files_in_dir(directory: Path, func: callable, **kwargs):
    for filename in os.listdir(directory):
        fpath = Path(os.path.join(directory, filename))
        func(fpath, **kwargs)


def image_creator(iterations: int):
    # for _ in range(iterations):
    #     url = grab_cute_img()
    #     save_url(url)

    # logger.info(f"Grabbed {iterations} images")

    # directory = "src/received_imgs"
    # for filename in os.listdir(directory):
    #     fpath = Path(os.path.join(directory, filename))
    #     add_txt_to_image(fpath)

    # directory = "src/step1"
    # for filename in os.listdir(directory):
    #     fpath = Path(os.path.join(directory, filename))
    #     add_random_text(fpath, grab_arabic_text)

    directory = "src/step2"
    for filename in os.listdir(directory):
        fpath = Path(os.path.join(directory, filename))
        add_random_images(fpath)

    logger.success(f"Added text to all images")


if __name__ == "__main__":
    image_creator(3)
