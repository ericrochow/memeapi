import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fuzzywuzzy.process import extractOne

load_dotenv()
app = FastAPI()
img_dir = os.getenv("IMG_DIR")
img_baseurl = os.getenv("IMG_BASEURL")
gif_dir = os.getenv("GIF_DIR")
gif_baseurl = os.getenv("GIF_BASEURL")


@app.get("/img")
async def return_img_link(query: str) -> str:
    """
    This method uses fuzzy matching on an argument and returns a link
    to the most relevant image.
    """
    best_match = extractOne(query.replace(" ", "_"), os.listdir(img_dir))
    if best_match[1] > 50:
        resp = f"{img_baseurl}/{best_match[0]}"
    else:
        resp = "Sorry, I wasn't able to find an appropriate image."
    return resp


@app.get("/gif")
async def return_gif_link(query: str) -> str:
    """
    This method uses fuzzy matching on an argument and returns a link
    to the most relevant gif.
    """
    best_match = extractOne(query.replace(" ", "_"), os.listdir(gif_dir))
    if best_match[1] > 50:
        resp = f"{gif_baseurl}/{best_match[0]}"
    else:
        resp = "Sorry, I wasn't able to find an appropriate gif."
    return resp
