import copy
import datetime
import json
import os
import aiohttp
import asyncio
from Lexcovery_Sanctions import settings
import requests
from bs4 import BeautifulSoup

API_URL = 'https://api.opencorporates.com/v0.4/'


async def find_officer_count_by_name(name: str):
    async with aiohttp.ClientSession() as session:
        req_text_low = name.replace(' ', '+')
        req_text_cap = name.upper().replace(' ', '+')
        low_count = 0
        cap_count = 0

        request_low = 'officers/search?q=' + req_text_low
        response_low = await session.request(method='GET', url=API_URL + request_low, params={'api_token': 'jxmgEivIjosarjaLoVyk'})
        if response_low.ok:
            doc = await response_low.read()
            res = json.loads(doc)
            low_count = res["results"]["total_count"]

        '''
        request_cap = 'officers/search?q='+req_text_cap
        response_cap = await session.request(method='GET', url=API_URL+request_low)
        if response_cap.ok:
            doc = await response_cap.text()
            cap_count = doc['results']['total_count']
        '''
        return low_count + cap_count


