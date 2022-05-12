import copy
import datetime
import os

import xlrd
from DataModel.AU import sanction_au
from Lexcovery_Sanctions import settings
import requests
from dateutil.parser import parse
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from io import BytesIO

SANCTIONS_LIST = os.path.join(settings.BASE_DIR, 'static') + "/Sanctions/AU/regulation8_consolidated.xls"
XLS_URL = "https://www.dfat.gov.au/sites/default/files/regulation8_consolidated.xls"
sanctions = []
doc_id = 0


async def get_list_xls(session):
    response = await session.request(method='GET', url=XLS_URL)
    if response.ok:
        doc = await response.read()
        d = copy.deepcopy(doc)
        return d
    else:
        return


async def import_data_from_web(session):
    global sanctions

    today = datetime.datetime.today()
    last_update = today.strftime("%d/%m/%Y")

    # Define variable to load the workbook
    xls_file = await get_list_xls(session)
    workbook = xlrd.open_workbook(file_contents=xls_file)
    sheet = workbook.sheet_by_index(0)

    # Define variable to read the active sheet:
    await asyncio.gather(*[import_from_element_async(sheet.row_values(i)) for i in range(1, sheet.nrows)])

    # print('import finished')
    return sanctions, last_update


async def import_from_element_async(row):
    global doc_id
    import_data_from_element(row, doc_id)
    doc_id = doc_id + 1


async def import_data_from_xls():
    global sanctions

    today = datetime.datetime.today()
    last_update = today.strftime("%d/%m/%Y")

    # Define variable to load the workbook
    workbook = xlrd.open_workbook(SANCTIONS_LIST)
    sheet = workbook.sheet_by_index(0)

    # Define variable to read the active sheet:
    await asyncio.gather(*[import_from_element_async(sheet.row_values(i)) for i in range(1, sheet.nrows)])
    today = datetime.datetime.today()
    last_update = today.strftime("%d/%m/%Y")

    # print('import finished')
    return sanctions, last_update


def import_data_from_element(row, element_id):
    global sanctions
    doc = []

    for value in row:
        if value is None:
            value = ''
        doc.append(value)

    control_date = ''
    if doc[11]:
        try:
            control_date = xlrd.xldate_as_datetime(float(doc[11]), 0).date().strftime("%d/%m/%Y")
        except Exception:
            control_date = doc[11]
    committees = doc[10]
    listing_information = doc[9]
    additional_information = doc[8]
    citizenship = doc[6]
    place_of_birth = doc[5]
    date_of_birth = ''
    if doc[4]:
        try:
            date_of_birth = xlrd.xldate_as_datetime(float(doc[4]), 0).date().strftime("%d/%m/%Y")
        except Exception:
            date_of_birth = doc[4]
    name_type = doc[3]
    entity = doc[2]
    name = doc[1]
    number = str(doc[0])
    address = doc[7]

    sanction = sanction_au.SanctionAU(number=number, name=name, entity=entity, name_type=name_type, date_of_birth=date_of_birth,
                                      place_of_birth=place_of_birth, citizenship=citizenship, address=address,
                                      additional_information=additional_information, listing_information=listing_information,
                                      committees = committees, control_date=control_date, id=element_id)
    sanctions.append(sanction)


def import_data_from_json(element):

    element_id = element.id
    control_date = element.control_date
    committees = element.committees
    listing_information = element.listing_information
    additional_information = element.additional_information
    citizenship = element.citizenship
    place_of_birth = element.place_of_birth
    date_of_birth = element.date_of_birth
    name_type = element.name_type
    entity = element.entity
    name = element.name
    number = element.number
    address = element.address
    sanction = sanction_au.SanctionAU(number=number, name=name, entity=entity, name_type=name_type,
                                      date_of_birth=date_of_birth,
                                      place_of_birth=place_of_birth, citizenship=citizenship, address=address,
                                      additional_information=additional_information,
                                      listing_information=listing_information,
                                      committees=committees, control_date=control_date, id=element_id)
    return sanction