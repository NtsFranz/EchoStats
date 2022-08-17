from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import requests

app = FastAPI()



@app.get('/more/vrml_match_twitch/{match_id}')
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
    return RedirectResponse(discord.oauth_login_url)


@app.get("/callback/{location}", tags=["Discord Auth"])
async def callback(code: str, location: str):
    token, refresh_token = await discord.get_access_token(code)
    response = RedirectResponse("location")
    response.set_cookie(key="discord_auth_token", value=token)
    return response


@app.get(
    "/authenticated",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=bool,
    tags=["Discord Auth"]
)
async def is_authenticated(token: str = Depends(discord.get_token)):
    try:
        auth = await discord.isAuthenticated(token)
        return auth
    except Unauthorized:
        return False


@app.exception_handler(Unauthorized)
async def unauthorized_error_handler(_, __):
    # return RedirectResponse(discord.oauth_login_url)
    return JSONResponse({"error": "Unauthorized"}, status_code=401)


@app.exception_handler(RateLimited)
async def rate_limit_error_handler(_, e: RateLimited):
    return JSONResponse(
        {"error": "RateLimited", "retry": e.retry_after, "message": e.message},
        status_code=429,
    )
