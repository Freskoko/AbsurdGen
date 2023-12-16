import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from utils.image_creation.cutetext import grab_arabic_text


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


def add_txt_to_image(image_path: Path, text: str):

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

    img.save(f"src/finished_imgs/{image_path.name}", quality=85)


def add_random_text(image_path: Path, text_func: callable):

    # todo get colour random
    img = Image.open(str(image_path))
    draw = ImageDraw.Draw(img)

    # todo get this right

    for i in range(10):
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

    img.save(f"src/arabic_imgs/{image_path.name}", quality=85)


if __name__ == "__main__":
    test_text = "my bestie and your bestie"
    img = Path("src/received_imgs/output.jpg")
    add_txt_to_image(img, test_text)
