# Create your views here.
import os

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from Search import elasticsearch_handler, opencorporates_handler, bulk_sanctions_search
from Lexcovery_Sanctions import settings
import re
import datetime
import aiohttp
import asyncio
import nest_asyncio
from forms import UploadFileForm
import mimetypes


def main_view(request):
    return render(request, 'main.html', {})


async def search(request):
    search_string = request.POST["search"]
    req_text = search_string.replace(' ', '+')
    nominal = False

    sanctions = await elasticsearch_handler.search_fuzzy_request(search_string)
    try:
        officer_count = await opencorporates_handler.find_officer_count_by_name(search_string)
    except Exception as e:
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
                                           'count': len(sanctions), 'nominal': nominal, 'officer_count': officer_count,
                                           'req_text': req_text})


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


async def bulk_search(request):
    link = False
    file = ''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            await bulk_sanctions_search.search_entities(request.FILES['file'])
            link = True
            file = bulk_sanctions_search.result_file
            #file = os.path.join(settings.BASE_DIR, 'tmp') + '/result.xlsx'
    else:
        form = UploadFileForm()
    return render(request, 'bulk_search.html', {'form': form, 'link': link, 'file' : file})


async def download_file(request):
    #file = request.GET.get('file')
    file = 'result.xlsx'
    # Open the file for reading content
    #path = open(file, 'rb')
    #path_name = request.GET.get('file')
    #path = bulk_sanctions_search.result_file[path_name]
    #path = open(path_name, 'rb')
    path = bulk_sanctions_search.result_file
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(file)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=result.xlsx"
    # Return the response value
    return response