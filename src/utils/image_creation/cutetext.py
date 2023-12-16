import random

from loguru import logger
from openai import OpenAI

client = OpenAI()


def grab_cute_text():

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a funny cat loving assisstant. You dont say 'did you know', you just provide what is asked of you",
            },
            {
                "role": "user",
                "content": "Make up an absurd but convincing fact about evil cats. Only reply in one short line. DO NOT say 'did you know' ",
            },
        ],
    )
    out = completion.choices[0].message.content
    if out is None:
        logger.error("NO TEXT GRABBED")
    return out


def grab_arabic_text(n: int) -> str:
    arabic_text = "طبیعت زیبای دوست داشتنی"
    return "".join(random.choice(arabic_text) for _ in range(n))


if __name__ == "__main__":
    print(grab_cute_text())
