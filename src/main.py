import os
from pathlib import Path

from loguru import logger

from utils.image_creation.cutetext import grab_arabic_text
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
    for _ in range(iterations):
        url = grab_cute_img()
        save_url(url)

    logger.info(f"Grabbed {iterations} images")

    treat_files_in_dir(directory="src/images/received_imgs", func=add_txt_to_image)

    treat_files_in_dir(
        directory="src/images/step1", func=add_random_text, text_func=grab_arabic_text
    )

    treat_files_in_dir(directory="src/images/step2", func=add_random_images)

    logger.success(f"Completed image process")


if __name__ == "__main__":
    image_creator(3)
