import requests
import json

#################
# Init Wiki
#################
WIKI = True
S = requests.Session()

# URL = "http://localhost/mediawiki/api.php"
# URL = "http://192.168.1.128/mediawiki/api.php"
URL = "https://ignitevr.gg/echopedia/api.php"

# Step 1: GET request to fetch login token
PARAMS_0 = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
}

headers = {
    "Accept" : "*/*",
    "Content-Type" : "application/x-www-form-urlencoded",
    "User-Agent" : "Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
}


R = S.get(url=URL, params=PARAMS_0, headers=headers)
print(R.text)
DATA = R.json()

LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

# Step 2: POST request to log in. Use of main account for login is not
# supported. Obtain credentials via Special:BotPasswords
# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
# PARAMS_1 = {
#     "action": "login",
#     "lgname": "vrml_scraper_bot",
#     "lgpassword": "scraper23478237489",
#     "lgtoken": LOGIN_TOKEN,
#     "format": "json"
# }

PARAMS_1 = {
    "action": "login",
    "lgname": "Vrml scraper bot@echovr_scraper_bot",
    "lgpassword": "015ltgo4quqabqhfk8vvvpt1hf0381gk",
    "lgtoken": LOGIN_TOKEN,
    "format": "json"
}

R = S.post(URL, data=PARAMS_1, headers=headers)

# Step 3: GET request to fetch CSRF token
PARAMS_2 = {
    "action": "query",
    "meta": "tokens",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_2, headers=headers)
DATA = R.json()

CSRF_TOKEN = DATA['query']['tokens']['csrftoken']
################