import copy
import datetime
import os

import openpyxl
from DataModel.USA import sanction_USA_consolidated
from Lexcovery_Sanctions import settings
from DataImport import translit
import requests
from dateutil.parser import parse
import aiohttp
import asyncio
from io import BytesIO
from csv import reader

SANCTIONS_LIST = os.path.join(settings.BASE_DIR,  'static') + "/Sanctions/USA/consolidated.tsv"
sanctions = []
TSV_URL = "http://api.trade.gov/static/consolidated_screening_list/consolidated.tsv"


async def get_list_tsv(session):
    #response = requests.get(XML_URL)
    response = await session.request(method='GET', url=TSV_URL)
    if response.ok:
        doc = await response.text()
        d = copy.deepcopy(doc)
        return d
    else:
        return


async def import_data_from_web(session):
    global sanctions

    # Define variable to load the workbook
    today = datetime.datetime.today()
    last_update = today.strftime("%d/%m/%Y")

    tsv_file = await get_list_tsv(session)
    file = reader(tsv_file.splitlines(), delimiter="\t")
    # skip first line with headers
    next(file)

    # Define variable to read the active sheet:
    await asyncio.gather(*[import_from_element_async(row) for row in file])

    # print('import finished')

    return sanctions, last_update


async def import_from_element_async(row):
    import_data_from_element(row)


async def import_data_from_tsv():
    global sanctions

    # Define variable to load the workbook
    today = datetime.datetime.today()
    last_update = today.strftime("%d/%m/%Y")

    tsv_file = open(SANCTIONS_LIST, "r")
    file = reader(tsv_file, delimiter="\t")
    # skip first line with headers
    next(file)

    # Define variable to read the active sheet:
    await asyncio.gather(*[import_from_element_async(row) for row in file])

    #print('import finished')
    return sanctions, last_update


def import_data_from_element(row):
    global sanctions

    doc_id = row[0]
    source = row[1]
    entity_number = row[2]
    doc_type = row[3]
    programs = row[4]
    name = row[5]
    title = row[6]
    addresses = row[7]
    federal_register_notice = row[8]
    start_date = row[9]
    end_date = row[10]
    standard_order = row[11]
    license_requirement = row[12]
    license_policy = row[13]
    call_sign = row[14]
    vessel_type = row[15]
    gross_tonnage = row[16]
    gross_registered_tonnage = row[17]
    vessel_flag = row[18]
    vessel_owner = row[19]
    remarks = row[20]
    source_list_url = row[21]
    alt_names = row[22]
    citizenships = row[23]
    dates_of_birth = row[24]
    nationalities = row[25]
    places_of_birth = row[26]
    source_information_url = row[27]
    ids = row[28]

    try:
        start_date = parse(row[9]).date().strftime("%d/%m/%Y")
    except Exception:
        start_date = row[9]
    try:
        end_date = parse(row[10]).date().strftime("%d/%m/%Y")
    except Exception:
        end_date = row[10]

    sanction = sanction_USA_consolidated.SanctionUSAConsolidated(doc_id = doc_id, source=source,entity_number=entity_number,
                                                                 doc_type=doc_type,programs=programs,name=name,title=title,addresses=addresses,
                                                                 federal_register_notice=federal_register_notice,start_date=start_date,
                                                                 end_date=end_date,standard_order=standard_order,license_requirement=license_requirement,
                                                                 license_policy=license_policy,call_sign=call_sign,
                                                                 vessel_type=vessel_type,gross_tonnage=gross_tonnage,gross_registered_tonnage=gross_registered_tonnage,
                                                                 vessel_flag=vessel_flag,vessel_owner=vessel_owner,remarks=remarks,source_list_url=source_list_url,
                                                                 alt_names=alt_names,citizenships=citizenships, dates_of_birth=dates_of_birth,
                                                                 nationalities=nationalities,places_of_birth=places_of_birth,
                                                                 source_information_url=source_information_url,ids=ids)
    sanctions.append(sanction)


def import_data_from_json(element):

    doc_id = element.doc_id
    source = element.source
    entity_number = element.entity_number
    doc_type = element.doc_type
    programs = element.programs
    name = element.name
    title = element.title
    addresses = element.addresses
    federal_register_notice = element.federal_register_notice
    start_date = element.start_date
    end_date = element.end_date
    standard_order = element.standard_order
    license_requirement = element.license_requirement
    license_policy = element.license_policy
    call_sign = element.call_sign
    vessel_type = element.vessel_type
    gross_tonnage = element.gross_tonnage
    gross_registered_tonnage = element.gross_registered_tonnage
    vessel_flag = element.vessel_flag
    vessel_owner = element.vessel_owner
    remarks = element.remarks
    source_list_url = element.source_list_url
    alt_names = element.alt_names
    citizenships = element.citizenships
    dates_of_birth = element.dates_of_birth
    nationalities = element.nationalities
    places_of_birth = element.places_of_birth
    source_information_url = element.source_information_url
    ids = element.ids

    sanction = sanction_USA_consolidated.SanctionUSAConsolidated(doc_id = doc_id, source=source,entity_number=entity_number,
                                                                 doc_type=doc_type,programs=programs,name=name,title=title,addresses=addresses,
                                                                 federal_register_notice=federal_register_notice,start_date=start_date,
                                                                 end_date=end_date,standard_order=standard_order,license_requirement=license_requirement,
                                                                 license_policy=license_policy,call_sign=call_sign,
                                                                 vessel_type=vessel_type,gross_tonnage=gross_tonnage,gross_registered_tonnage=gross_registered_tonnage,
                                                                 vessel_flag=vessel_flag,vessel_owner=vessel_owner,remarks=remarks,source_list_url=source_list_url,
                                                                 alt_names=alt_names,citizenships=citizenships, dates_of_birth=dates_of_birth,
                                                                 nationalities=nationalities,places_of_birth=places_of_birth,
                                                                 source_information_url=source_information_url,ids=ids)
    return sanction