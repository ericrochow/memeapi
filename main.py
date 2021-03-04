import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fuzzywuzzy.process import extractOne
from pydantic import BaseModel

load_dotenv()
app = FastAPI()
img_dir = os.getenv("IMG_DIR")
img_baseurl = os.getenv("IMG_BASEURL")
gif_dir = os.getenv("GIF_DIR")
gif_baseurl = os.getenv("GIF_BASEURL")


class ImgSuccess(BaseModel):
    success: bool
    query: str
    link: Optional[str] = None


class GifSuccess(BaseModel):
    success: bool
    query: str
    link: Optional[str] = None


@app.get("/img", response_model=ImgSuccess)
async def return_img_link(query: str) -> dict:
    """
    Uses fuzzy matching on an argument to returns a link to the most relevant image.

    Args:
      query: A string containing the search query argument
    Returns:
      A dict containing the results of the search.
    """
    best_match = extractOne(query.replace(" ", "_"), os.listdir(img_dir))
    if best_match[1] > 50:
        resp = {
            "success": True,
            "query": query,
            "link": f"{img_baseurl}/{best_match[0]}",
        }
    else:
        resp = {
            "success": False,
            "query": query,
            "reason": "Was not able to find an appropriate image",
        }
    return resp


@app.get("/gif", response_model=GifSuccess)
async def return_gif_link(query: str) -> dict:
    """
    Uses fuzzy matching on an argument and returns a link to the most relevant gif.

    Args:
      query: A string containing the search query argument
    Returns:
      A dict containing the results of the search.
    """
    best_match = extractOne(query.replace(" ", "_"), os.listdir(gif_dir))
    if best_match[1] > 50:
        resp = {
            "success": True,
            "query": query,
            "link": f"{gif_baseurl}/{best_match[0]}",
        }
    else:
        resp = {
            "success": False,
            "query": query,
            "reason": "Was not able to find an appropriate image",
        }
    return resp
