# Create your views here.
from django.shortcuts import render
from Search import elasticsearch_handler, opencorporates_handler
import re
import datetime
import aiohttp
import asyncio
import nest_asyncio


def main_view(request):
    return render(request, 'main.html', {})


async def search(request):
    search_string = request.POST["search"]
    nominal = False

    sanctions = await elasticsearch_handler.search_fuzzy_request(search_string)
    try:
        officer_count = await opencorporates_handler.find_officer_count_by_name(request)
    except Exception:
        officer_count = 0

    if officer_count > 5:
        nominal = True

    i = 0
    for sanction in sanctions:
        sanction.names = re.sub(r'\n', r' <br> ', sanction.names)
        sanction.additional_info = re.sub(r'\n', r' <br> ', sanction.additional_info)
        sanction.personal_details = re.sub(r'\n', r' <br> ', sanction.personal_details)
        sanction.address = re.sub(r'\n', r' <br> ', sanction.address)
        sanction.nationality = re.sub(r'\n', r' <br> ', sanction.nationality)
        sanction.program = re.sub(r'\n', r' <br> ', sanction.program)
        sanction.id = i
        i = i+1

    return render(request, 'search.html', {'search_string': search_string, 'sanctions': sanctions,
                                           'count': len(sanctions), 'nominal': nominal, 'officer_count': officer_count})


def donate(request):
    return render(request, 'donate.html', {})


def support(request):
    return render(request, 'support.html', {})


def sources(request):
    last_update_us = elasticsearch_handler.last_update_us
    last_update_us_cons = elasticsearch_handler.last_update_us_cons
    last_update_uk = elasticsearch_handler.last_update_uk
    last_update_eu = elasticsearch_handler.last_update_eu
    last_update_ua = elasticsearch_handler.last_update_ua
    last_update_uk_cons = elasticsearch_handler.last_update_uk_cons
    last_update_jp = elasticsearch_handler.last_update_jp
    last_update_au = elasticsearch_handler.last_update_au
    last_update_ca = elasticsearch_handler.last_update_ca

    return render(request, 'sources.html', {'last_update_us': last_update_us, 'last_update_uk': last_update_uk,
                                         'last_update_eu': last_update_eu, 'last_update_ua': last_update_ua,
                                         'last_update_uk_cons': last_update_uk_cons, 'last_update_jp': last_update_jp,
                                         'last_update_au': last_update_au, 'last_update_ca': last_update_ca,
                                         'last_update_us_cons': last_update_us_cons})


async def upload(request):
    result = 'Upload lists first'
    if request.GET.get('createIndexBtn'):
        update_time = datetime.datetime.now().time()
        update = update_time.strftime("%H:%M")
        await elasticsearch_handler.create_index()
        result = 'Index created at ' + update
    return render(request, 'upload.html', {'result': result})

