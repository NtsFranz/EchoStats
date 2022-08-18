from typing import Union

import requests
from fastapi import FastAPI, Response, Cookie, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from config import *

app = FastAPI()

redirect_uri = "https://tools.echopedia.gg/callback/arena_block_map"

templates = Jinja2Templates(directory="templates")


# app.mount("/", StaticFiles(directory="static"), name="static")


def get_oauth_url() -> str:
    return f"https://discord.com/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=identify&response_type=code"


def get_access_token(code: str) -> dict:
    r = requests.post(
        "https://discord.com/api/oauth2/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
    return r.json()


def get_user(token: str):
    print(token)
    r = requests.get(
        "https://discordapp.com/api/users/@me",
        headers={
            'Authorization': f'Bearer {token}'
        })
    return r.json()


@app.get('/vrml/match_twitch_link/{match_id}')
async def vrml_match_twitch(match_id: str):
    try:
        r = requests.get(f"https://api.vrmasterleague.com/EchoArena/Matches/UpcomingProduction/{match_id}").json()
    except:
        return "Not a valid match id"

    if r["castingInfo"]["channelURL"] is not None:
        return RedirectResponse(r["castingInfo"]["channelURL"])
    else:
        return "No Twitch URL for that match yet. Check back later"


@app.get("/login", tags=["Discord Auth"])
async def login():
    return RedirectResponse(get_oauth_url())


@app.get("/callback/{location}", tags=["Discord Auth"])
async def callback(response: Response, code: str, location: str):
    print(code)
    r = get_access_token(code)
    print(r)
    response = RedirectResponse("/" + location)
    response.set_cookie(key="discord_auth_token", value=r['access_token'])
    response.set_cookie(key="discord_refresh_token", value=r['refresh_token'])
    return response


@app.get(
    "/user",
    tags=["Discord Auth"]
)
async def get_user_route(discord_auth_token: Union[str, None] = Cookie(default=None)):
    return get_user(discord_auth_token)


@app.get(
    "/logged_in",
    tags=["Discord Auth"]
)
async def get_logged_in(discord_auth_token: Union[str, None] = Cookie(default=None)):
    user = get_user(discord_auth_token)
    if "id" in user:
        return {"logged_in": True}
    else:
        return {"logged_in": False}


@app.get("/arena_block_map", tags=["Pages"], response_class=HTMLResponse)
async def arena_block_map(request: Request):
    return templates.TemplateResponse("arena_block_map.html", {"request": request})
