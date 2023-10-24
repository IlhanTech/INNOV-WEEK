import os
import openai


def generate_img_dalle(api_key_openai, prompt):
    openai.api_key = api_key_openai

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024",
    )
    return (response["data"][0]["url"])
