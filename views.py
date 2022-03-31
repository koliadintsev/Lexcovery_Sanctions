# Create your views here.
from django.shortcuts import render
from Search import elasticsearch_handler
import re


def main_view(request):
    return render(request, 'main.html', {})


def search(request):
    search_string = request.POST["search"]
    sanctions = elasticsearch_handler.search_fuzzy_request(search_string)
    for sanction in sanctions:
        sanction.names = re.sub(r'\n', r' <br> ', sanction.names)
        sanction.additional_info = re.sub(r'\n', r' <br> ', sanction.additional_info)
        sanction.personal_details = re.sub(r'\n', r' <br> ', sanction.personal_details)
        sanction.address = re.sub(r'\n', r' <br> ', sanction.address)
        sanction.nationality = re.sub(r'\n', r' <br> ', sanction.nationality)
        sanction.program = re.sub(r'\n', r' <br> ', sanction.program)

    return render(request, 'search.html', {'search_string': search_string, 'sanctions': sanctions})


def donate(request):
    return render(request, 'donate.html', {})


def support(request):
    return render(request, 'support.html', {})


def upload(request):
    return render(request, 'upload.html', {'result': 'Upload lists first'})


def create_index(request):
    elasticsearch_handler.create_index()
    return render(request, 'upload.html', {'result': 'Index created'})
