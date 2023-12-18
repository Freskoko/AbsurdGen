import glob
import os

from loguru import logger


def clear_folders():
    # Folders to be cleared
    folders = [
        "src/images/received_imgs",
        "src/images/step1",
        "src/images/step2",
        "src/images/step3",
        "src/images/many_images",
    ]

    for folder in folders:
        # For every .jpg and .png file in the folder
        for filename in glob.glob(os.path.join(folder, "*.[pjP][npN][gG]")):
            # Remove the file
            os.remove(filename)

    # Log info
    logger.info("Cleared folders")


if __name__ == "__main__":
    clear_folders()
