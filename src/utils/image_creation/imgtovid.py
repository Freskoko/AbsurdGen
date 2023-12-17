import os
import re
import shutil
from pathlib import Path

import cv2
import moviepy.video.io.ImageSequenceClip
import numpy as np
from natsort import natsorted
from PIL import Image, ImageDraw, ImageEnhance, ImageFont


def warp_perspective(img):
    rows, cols = img.shape[:2]

    src_points = np.float32(
        [[0, 0], [cols - 1, 0], [0, rows - 1], [cols - 1, rows - 1]]
    )
    dst_points = np.float32(
        [[0, 0], [cols - 1, 0], [0, rows - 1], [cols - 1, rows - 1]]
    )

    projective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    img = cv2.warpPerspective(img, projective_matrix, (cols, rows))

    src_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
    dst_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])

    affine_matrix = cv2.getAffineTransform(src_points, dst_points)
    img_output = cv2.warpAffine(img, affine_matrix, (cols, rows))

    return img_output.clip(0, 255).astype("uint8")


def img_to_many(image_path: Path):

    shutil.rmtree("src/images/many_images")
    (Path("src/images/many_images")).mkdir(parents=True, exist_ok=True)
    img = Image.open(image_path)
    img.save(f"src/images/many_images/0_{image_path.name}", quality=85)

    for i in range(-1080, 1081, 25):
        enhancement_factor = i * 0.01  # go from 0-1

        enhancements = [
            "Contrast",
            "Color",
            "Sharpness",
        ]

        image_enhanced = img

        for enh_name in enhancements:
            enh_function = getattr(ImageEnhance, enh_name)
            enhancer = enh_function(image_enhanced)
            image_enhanced = enhancer.enhance(enhancement_factor)

        # rotate
        image_enhanced = image_enhanced.rotate((abs(i / 3)))

        # warp
        img_numpy = np.array(image_enhanced)
        img_warped = warp_perspective(img_numpy)
        img_warped = Image.fromarray(img_warped)

        # save
        img_warped.save(f"src/images/many_images/{i}_{image_path.name}", quality=85)


def img_to_video(image_folder: Path):

    fps = 10

    image_files = [
        os.path.join(image_folder, img)
        for img in os.listdir(image_folder)
        if img.endswith(".jpg")
    ]

    # Sort image files based on numbers in their names
    image_files = natsorted(
        image_files, key=lambda x: int(re.findall(r"\d+", os.path.basename(x))[0])
    )

    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile("src/images/movie.mp4")

    return


# def add_sound


if __name__ == "__main__":
    fpath = Path("src/images/step3/output_P8J3M.jpg")
    img_to_many(fpath)
    fpath = Path("src/images/many_images")
    img_to_video(fpath)


# if __name__ == "__main__":
#     fpath = Path("src/images/step3/output_P8J3M.jpg")
#     img_to_many(fpath)
