import copy
import datetime
import os

import xlrd
from DataModel.JP import sanction_jp
from Lexcovery_Sanctions import settings
import requests
from dateutil.parser import parse
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from io import BytesIO

SANCTIONS_LIST = os.path.join(settings.BASE_DIR, 'static') + "/Sanctions/JP/sanctions.xls"
XLS_URL = "https://www.mof.go.jp/policy/international_policy/gaitame_kawase/gaitame/economic_sanctions/shisantouketsu20220412.xls"
SANCTIONS_WEBSITE = 'https://www.mof.go.jp/policy/international_policy/gaitame_kawase/gaitame/economic_sanctions/'
sanctions = []
doc_id = 0


async def find_link_xls(session):

    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    response = requests.get(url=SANCTIONS_WEBSITE+'list.html')
    #response = await session.request(method='GET', url=SANCTIONS_WEBSITE + 'list.html')
    xls_url_web = XLS_URL
    if response.ok:
        doc = response.text
        text = BeautifulSoup(doc, 'html.parser')
        for link in text.find_all('a'):
            url = link.get('href')
            if 'shisantouketsu' and '.xls' in url:
                xls_url_web = url.replace('./', SANCTIONS_WEBSITE)
        return xls_url_web
    else:
        return XLS_URL


async def get_list_xls(session):
    link = await find_link_xls(session)
    #response = await session.request(method='GET', url=link)
    response = requests.get(url=link)
    if response.ok:
        doc = response.content
        d = copy.deepcopy(doc)
        return d, link
    else:
        return


async def import_data_from_web(session):
    global sanctions

    # Define variable to load the workbook
    xls_file, link = await get_list_xls(session)
    workbook = xlrd.open_workbook(file_contents=xls_file)

    today = link.replace('.xls', '').replace(SANCTIONS_WEBSITE + 'shisantouketsu', '')
    last_update = today[6:len(today)] + today[4:6] + today[0:4]

    # Define variable to read the active sheet:
    for sheet_num in range(1, len(workbook.sheets())):
        table_start = 99999
        sheet = workbook.sheet_by_index(sheet_num)
        for row_num in range(1, sheet.nrows):
            row_value = sheet.row_values(row_num)
            if row_value[0] == '????????????':
                table_start = row_num + 1
                #print(sheet.name + ': ' + str(table_start))
                # break
        await asyncio.gather(*[import_from_element_async(sheet.row_values(i), sheet.row_values(table_start - 1), sheet.name) for i in range(table_start, sheet.nrows)])

    # print('import finished')
    return sanctions, last_update


async def import_from_element_async(row, headers, sheet_title):
    global doc_id
    import_data_from_element(row, headers, sheet_title, doc_id)
    doc_id = doc_id + 1


async def import_data_from_xls():
    global sanctions

    today = datetime.datetime.today()
    last_update = today.strftime("%d/%m/%Y")

    # Define variable to load the workbook
    workbook = xlrd.open_workbook(SANCTIONS_LIST)

    # Define variable to read the active sheet:
    for sheet_num in range(1, len(workbook.sheets())):
        table_start = 99999
        sheet = workbook.sheet_by_index(sheet_num)
        for row_num in range(1, sheet.nrows):
            row_value = sheet.row_values(row_num)
            if row_value[0] == '????????????':
                table_start = row_num + 1
                #print(sheet.name + ': ' + str(table_start))
                # break
        await asyncio.gather(*[import_from_element_async(sheet.row_values(i), sheet.row_values(table_start - 1), sheet.name) for i in range(table_start, sheet.nrows)])

    """
    tree = ET.fromstring(file.read().strip())
    executor = concurrent.futures.ThreadPoolExecutor(100)
    futures = [executor.submit(import_data_from_element, item, companies) for item in tree.findall('.//document')]
    concurrent.futures.wait(futures)
    """
    # print('import finished')
    return sanctions, last_update


def import_data_from_element(row, headers, sheet_title, element_id):
    global sanctions
    doc = []

    for value in row:
        if value is None:
            value = ''
        doc.append(value)

    start_date = ''
    try:
        start_date_text = doc[0].split('.')
        start_date = datetime.date(int(start_date_text[0]), int(start_date_text[1]), int(start_date_text[2])).strftime("%d/%m/%Y")
    except Exception:
        start_date = doc[0]
    number = str(doc[1])
    name_jp = str(doc[2])
    if name_jp == '':
        return
    name_eng = str(doc[3])

    title = sheet_title.split(".", 1)
    program = title[1]

    remark = ''
    address = ''
    id_details = ''
    country = ''
    position = ''
    place_of_birth = ''
    date_of_birth = ''
    alias = ''
    contacts = ''

    for i in range(4, len(row)):
        header = headers[i].replace(' ', '').replace('???', '')
        value = doc[i]

        if value != '':
            if header == '????????????????????????' or header == '????????????':
                if value:
                    try:
                        date_of_birth = xlrd.xldate_as_datetime(float(value), 0).date().strftime("%d/%m/%Y")
                    except Exception:
                        date_of_birth = value
            elif header == '??????????????????' or header == '??????':
                remark = remark + str(value) + '\n'
            elif header == '???????????????' or header == '??????' or header == '???????????????' or header == '???????????????' or \
                    header == '?????????????????????' or header == '??????' or header == '????????????????????????' or \
                    header == '??????????????????????????????' or header == '???????????????' or header == '??????' or header == '???????????????':
                alias = alias + str(value) + '\n'
            elif header == '?????????' or header == '??????' or header == '???????????????':
                position = position + str(value) + '\n'
            elif header == '??????????????????' or header == '?????????' or header == '???????????????????????????????????????????????????' or header == '?????????????????????' or \
                    header == '??????':
                address = address + str(value) + '\n'
            elif header == '??????' or header == '????????????' or header == 'FAX':
                contacts = contacts + str(value) + '\n'
            elif header == '?????????' or header == '?????????????????????':
                place_of_birth = str(value)
            elif header == '??????':
                country = str(value)
            elif header == '???????????????????????????????????????' or header == '??????1483????????????' or header == '????????????????????????????????????':
                program = program + str(value) + '\n'
            elif header == '????????????' or header == '???????????????' or header == '??????????????????' or header == '????????????' or header == 'ID??????':
                id_details = id_details + str(value) + '\n'

    sanction = sanction_jp.SanctionJP(id=element_id, start_date=start_date, number=number, name_jp=name_jp, name_eng=name_eng,
                                      alias=alias, date_of_birth=date_of_birth,
                                      place_of_birth=place_of_birth, contacts=contacts,
                                      position=position, country=country, id_details=id_details, address=address,
                                      program=program, remark=remark)
    sanctions.append(sanction)


def import_data_from_json(element):

    contacts = element.contacts
    remark = element.remark
    program = element.program
    address = element.address
    id_details = element.id_details
    country = element.country
    position = element.position
    place_of_birth = element.place_of_birth
    alias = element.alias
    name_eng = element.name_eng
    name_jp = element.name_jp
    number = element.number
    element_id = element.id
    date_of_birth = element.date_of_birth
    start_date = element.start_date

    sanction = sanction_jp.SanctionJP(id=element_id, start_date=start_date, number=number, name_jp=name_jp, name_eng=name_eng,
                                      alias=alias, date_of_birth=date_of_birth,
                                      place_of_birth=place_of_birth, contacts=contacts,
                                      position=position, country=country, id_details=id_details, address=address,
                                      program=program, remark=remark)
    return sanction