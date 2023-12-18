import os
import re
import shutil
from pathlib import Path

import cv2
import moviepy.video.io.ImageSequenceClip
import numpy as np
from moviepy.editor import AudioFileClip, VideoFileClip
from natsort import natsorted
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

from utils.image_creation.img_grab import random_str


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

    shutil.rmtree("src/images/many_images", ignore_errors=True)

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
        # image_enhanced = image_enhanced.rotate((abs(i / 3)))

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
    clip.write_videofile("src/images/movies/temp.mp4")

    return


def add_sound_to_mp4(video_location: Path, music_location: Path):
    # Load video and audio
    video = VideoFileClip(str(video_location))
    audio = AudioFileClip(str(music_location))

    # Add audio to the video
    final_video = video.set_audio(audio)

    # Write the result to a file. ".set_duration(video.duration)" ensures that audio will not run beyond video length.
    rando = random_str(5)
    final_video.set_duration(video.duration).write_videofile(
        f"src/images/movies/movie_{rando}.mp4"
    )
    shutil.rmtree("src/images/many_images", ignore_errors=True)
    shutil.rmtree("src/images/movies/temp.mp4", ignore_errors=True)
    return


if __name__ == "__main__":
    fpath = Path("src/images/step3/output_P8J3M.jpg")
    img_to_many(fpath)
    fpath = Path("src/images/many_images")
    img_to_video(fpath)

    vpath = Path("src/images/temp.mp4")
    apath = Path("src/utils/image_creation/sample_sound/epic.mp3")
    add_sound_to_mp4(vpath, apath)


# if __name__ == "__main__":
#     fpath = Path("src/images/step3/output_P8J3M.jpg")
#     img_to_many(fpath)
