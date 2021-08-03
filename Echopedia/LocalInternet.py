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
        r = requests.get(url)
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