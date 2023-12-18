import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from utils.config import CONFIG
from utils.image_creation.cutetext import grab_cute_text


def grab_random_colour():
    return random.choice(
        [
            (255, 255, 128),
            (225, 193, 235),
            (255, 228, 225),
            (240, 248, 255),
            (245, 245, 220),
            (176, 224, 230),
            (100, 149, 237),
            (255, 192, 203),
            (152, 251, 152),
            (250, 235, 215),
            (240, 230, 140),
            (135, 206, 250),
        ]
    )


def add_txt_to_image(image_path: Path):
    text = grab_cute_text()

    # todo get colour random
    img = Image.open(str(image_path))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("FreeMonoBold.ttf", 70)

    # todo get this right
    para = textwrap.wrap(text, width=20)

    current_h, pad = (500), 150
    for line in para:

        random_colour = grab_random_colour()
        current_h = current_h + pad
        # print(f"{current_h} {line}")
        draw.text(
            (img.width / 2, current_h / 2),
            line,
            font=font,
            anchor="mm",
            fill=random_colour,
            stroke_width=3,
            stroke_fill="black",
        )

    img.save(f"src/images/step3/{image_path.name}", quality=85)


def add_random_text(image_path: Path, text_func: callable):

    img = Image.open(str(image_path))
    draw = ImageDraw.Draw(img)

    for _ in range(CONFIG["arabic"]):
        text = text_func(30)
        para = textwrap.wrap(text, width=random.randint(15, 50))
        font = ImageFont.truetype(
            "src/utils/fonts/FontsFree-Net-Vazir-Regular.ttf", random.randint(25, 80)
        )
        current_h, pad = (random.randint(-100, 2000)), random.randint(50, 300)
        width = img.width - random.randint(-1000, 1000)
        for line in para:

            random_colour = grab_random_colour()
            current_h = current_h + pad
            # print(f"{current_h} {line}")
            draw.text(
                (width / 2, current_h / 2),
                line,
                font=font,
                anchor="mm",
                fill=random_colour,
                stroke_width=random.randint(0, 10),
                stroke_fill="black",
            )

    img.save(f"src/images/step1/{image_path.name}", quality=85)


def add_random_images(image_path: Path):
    # main img
    img = Image.open(image_path)
    img_w, img_h = img.size

    # random images
    dir_path = Path("src/utils/image_creation/sample_images")
    files = list(dir_path.glob("*"))

    for _ in range(CONFIG["other_imgs"]):
        # thing to put on top
        random_overlay_file = random.choice(
            files
        )  # Choose a random file for the overlay
        overlay = Image.open(random_overlay_file)
        overlay = overlay.resize((random.randint(109, 300), random.randint(100, 300)))
        overlay_w, overlay_h = overlay.size

        overlay.putalpha(random.randint(50, 150))

        offset = (
            (img_w - overlay_w + random.randint(-1000, 1000)) // 2,
            (img_h - overlay_h + random.randint(-1000, 1000)) // 2,
        )
        img.paste(overlay, offset, overlay)

    img.save(f"src/images/step2/{image_path.name}", quality=85)


if __name__ == "__main__":
    test_text = "my bestie and your bestie"
    img = Path("src/received_imgs/output.jpg")
    add_txt_to_image(img, test_text)
