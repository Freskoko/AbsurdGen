import os
from pathlib import Path

from loguru import logger

from utils.image_creation.clear import clear_folders
from utils.image_creation.cutetext import grab_arabic_text
from utils.image_creation.img_grab import grab_cute_img, save_url
from utils.image_creation.imgtovid import add_sound_to_mp4, img_to_many, img_to_video
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

    clear_folders()

    for _ in range(iterations):
        url = grab_cute_img()
        save_url(url)

    logger.info(f"Grabbed {iterations} images")

    treat_files_in_dir(
        directory="src/images/received_imgs",
        func=add_random_text,
        text_func=grab_arabic_text,
    )

    treat_files_in_dir(directory="src/images/step1", func=add_random_images)

    treat_files_in_dir(directory="src/images/step2", func=add_txt_to_image)

    logger.success(f"Completed image processing")

    directory = "src/images/step3"
    for filename in os.listdir(Path(directory)):
        fpath = Path(os.path.join(directory, filename))
        img_to_many(fpath)

        img_to_video("src/images/many_images")

        vpath = Path("src/images/movies/temp.mp4")
        apath = Path("src/utils/image_creation/sample_sound/epic.mp3")
        add_sound_to_mp4(vpath, apath)

    logger.success(f"Completed movie processing")


if __name__ == "__main__":
    image_creator(1)
