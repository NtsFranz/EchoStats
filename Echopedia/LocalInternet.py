# Saves a version of the website locally or performs a request to the internet

import os
import requests
from pyquery import PyQuery as pq
import json
import asyncio
from pyppeteer import launch

from WikiCommon import *

local_internet = {}

print_urls = False

requests.packages.urllib3.util.connection.HAS_IPV6 = False


def load():
    global local_internet
    local_internet = loadJSON('local_internet')


def save():
    global local_internet
    dumpJSON('local_internet', local_internet)


def get(url: str, force: bool = False):
    global local_internet
    if url not in local_internet or force:
        print(url)
        r = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        })
        local_internet[url] = r.text
        save()
        return r.text
    else:
        if print_urls:
            print(url)
        return local_internet[url]


def local_pq(url: str, force: bool = False):
    return pq(get(url))


async def innerHTMLPuppet(url: str, force: bool = False) -> str:
    global local_internet
    if url not in local_internet or force:
        print(url)

        browser = await launch(headless=False)
        page = await browser.newPage()
        await page.goto(url)
        local_internet[url] = await page.evaluate('document.body.innerHTML')
        await browser.close()
        save()
        return pq(local_internet[url])
    else:
        if print_urls:
            print(url)
        return pq(local_internet[url])
