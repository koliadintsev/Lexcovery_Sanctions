import copy
import datetime
import os

from DataModel.UA import company_nazk_ua, individual_nazk_ua
from Lexcovery_Sanctions import settings
from DataImport import translit
import requests
from dateutil.parser import parse
import aiohttp
import json
import asyncio
from io import BytesIO
from csv import reader

COMPANIES_LIST = os.path.join(settings.BASE_DIR, 'static') + "/Sanctions/UA_NAZK/company.csv"
COMPANIES_RISK_LIST = os.path.join(settings.BASE_DIR, 'static') + "/Sanctions/UA_NAZK/company_risk.csv"
PERSONS_LIST = os.path.join(settings.BASE_DIR, 'static') + "/Sanctions/UA_NAZK/person.csv"
PERSONS_RISK_LIST = os.path.join(settings.BASE_DIR, 'static') + "/Sanctions/UA_NAZK/person_risk.csv"
sanctions_companies = []
sanctions_persons = []
COMPANIES_URL = "https://sanctions.nazk.gov.ua/api/company/"
COMPANIES_RISK_URL = "https://sanctions.nazk.gov.ua/api/company-warning/"
PERSONS_URL = "https://sanctions.nazk.gov.ua/api/person/"
PERSONS_RISK_URL = "https://sanctions.nazk.gov.ua/api/person-warning/"


async def import_company_from_web(session):

    # Define variable to load the workbook
    today = datetime.datetime.today()
    last_update = today.strftime("%d/%m/%Y")

    response_company = await session.request(method='GET', url=COMPANIES_URL)
    response_company_risk = await session.request(method='GET', url=COMPANIES_RISK_URL)

    company = []
    company_risk = []

    if response_company.ok:
        doc = await response_company.read()
        res = json.loads(doc)
        company = res["data"]

    if response_company_risk.ok:
        doc = await response_company_risk.read()
        res = json.loads(doc)
        company_risk = res["data"]
        company.append(company_risk)

    await asyncio.gather(*[import_company_from_json(record) for record in company])
    await asyncio.gather(*[import_company_from_json(record) for record in company_risk])

    return sanctions_companies, last_update


async def import_person_from_web(session):

    # Define variable to load the workbook
    today = datetime.datetime.today()
    last_update = today.strftime("%d/%m/%Y")

    response_person = await session.request(method='GET', url=PERSONS_URL)
    response_person_risk = await session.request(method='GET', url=PERSONS_RISK_URL)

    person = []
    person_risk = []

    if response_person.ok:
        doc = await response_person.read()
        res = json.loads(doc)
        person = res["data"]

    if response_person_risk.ok:
        doc = await response_person_risk.read()
        res = json.loads(doc)
        person_risk = res["data"]
        person.append(person_risk)

    await asyncio.gather(*[import_person_from_json(record) for record in person])
    await asyncio.gather(*[import_person_from_json(record) for record in person_risk])

    return sanctions_persons, last_update


async def import_person_from_json(record):
    sanction = import_person_record_from_json(record)
    sanctions_persons.append(sanction)


async def import_company_from_json(record):
    sanction = import_company_record_from_json(record)
    sanctions_companies.append(sanction)


async def import_company_list_from_csv():
    # Define variable to load the workbook
    today = datetime.datetime.today()
    last_update = today.strftime("%d/%m/%Y")

    companies_csv = open(COMPANIES_LIST, "r")
    companies_risk_csv = open(COMPANIES_RISK_LIST, "r")

    companies_csv_file = reader(companies_csv, delimiter=",")
    # skip first line with headers
    next(companies_csv_file)

    companies_risk_csv_file = reader(companies_risk_csv, delimiter=",")
    # skip first line with headers
    next(companies_risk_csv_file)

    # Define variable to read the active sheet:
    await asyncio.gather(*[import_company_from_csv(row) for row in companies_csv_file])
    await asyncio.gather(*[import_company_from_csv(row) for row in companies_risk_csv_file])

    # print('import finished')

    return sanctions_companies, last_update


async def import_person_list_from_csv():
    # Define variable to load the workbook
    today = datetime.datetime.today()
    last_update = today.strftime("%d/%m/%Y")

    persons_csv = open(PERSONS_LIST, "r")
    persons_risk_csv = open(PERSONS_RISK_LIST, "r")

    persons_csv_file = reader(persons_csv, delimiter=",")
    # skip first line with headers
    next(persons_csv_file)

    persons_risk_csv_file = reader(persons_risk_csv, delimiter=",")
    # skip first line with headers
    next(persons_risk_csv_file)

    # Define variable to read the active sheet:
    await asyncio.gather(*[import_person_from_csv(row) for row in persons_csv_file])
    await asyncio.gather(*[import_person_from_csv(row) for row in persons_risk_csv_file])

    # print('import finished')

    return sanctions_persons, last_update


async def import_person_from_csv(row):
    sanction = import_person_record_from_csv(row)
    sanctions_persons.append(sanction)


async def import_company_from_csv(row):
    sanction = import_company_record_from_csv(row)
    sanctions_companies.append(sanction)


def import_person_record_from_csv(row):
    sanctions_ua_date = ''
    sanctions_ua = row[23]
    relations_company = []
    relations_person = []
    link_archive = row[31]
    link = row[30]
    city_bd_en = row[29]
    city_bd_ru = row[28]
    city_bd_uk = row[27]
    itn = row[25]
    date_dead = ''
    date_bd = row[26]
    synchron = ''
    top_50 = ''
    status = row[24]
    photo_name = row[9]
    url_nz = ''
    url_ua = ''
    url_jp = ''
    url_au = ''
    url_ch = ''
    url_ca = ''
    url_us = ''
    url_gb = ''
    url_es = ''
    subcategory_3 = row[8]
    subcategory_2 = row[7]
    subcategory_1 = row[6]
    category = row[5]
    reasoning_ru = row[15]
    reasoning_en = row[14]
    reasoning_uk = row[13]
    position_ru = row[12]
    position_en = row[11]
    position_uk = row[10]
    country = row[4]
    name_uk = row[3]
    name_ru = row[2]
    name_en = row[1]
    person_id = row[0]

    #    try:
    #        start_date = parse(row[9]).date().strftime("%d/%m/%Y")
    #    except Exception:
    #        start_date = row[9]

    sanction = individual_nazk_ua.IndividualNAZKUA(person_id=person_id, name_en=name_en, name_ru=name_ru, name_uk=name_uk, country=country,
                                                   position_uk=position_uk,
                                                   position_en=position_en, position_ru=position_ru, reasoning_uk=reasoning_uk, reasoning_en=reasoning_en,
                                                   reasoning_ru=reasoning_ru, category=category, subcategory_1=subcategory_1,
                                                   subcategory_2=subcategory_2, subcategory_3=subcategory_3, sanctions_ua=sanctions_ua,
                                                   sanctions_ua_date=sanctions_ua_date, url_es=url_es, url_gb=url_gb,
                                                   url_us=url_us, url_ca=url_ca, url_ch=url_ch, url_au=url_au, url_jp=url_jp, url_ua=url_ua,
                                                   url_nz=url_nz,
                                                   photo_name=photo_name, status=status, top_50=top_50, synchron=synchron, date_bd=date_bd,
                                                   date_dead=date_dead, itn=itn,
                                                   city_bd_uk=city_bd_uk, city_bd_ru=city_bd_ru, city_bd_en=city_bd_en,
                                                   link=link, link_archive=link_archive,
                                                   relations_person=relations_person, relations_company=relations_company)

    return sanction


def import_company_record_from_csv(row):
        sanctions_ua = row[20]
        sanctions_ua_date = ''
        relations_company = []
        relations_person = []
        link_archive = ''
        link = ''
        url_nz = ''
        url_ua = ''
        url_jp = ''
        url_au = ''
        url_ch = ''
        url_ca = ''
        url_us = ''
        url_gb = ''
        url_es = ''
        address_ru = ''
        address_en = ''
        address_uk = ''
        reasoning_ru = ''
        reasoning_en = ''
        reasoning_uk = ''
        inn = row[12]
        ogrn = row[11]
        subcategory_3 = row[10]
        subcategory_2 = row[9]
        subcategory_1 = row[8]
        category = row[7]
        country = row[6]
        name_ru = row[5]
        name_uk = row[4]
        name_en = row[3]
        name = ''
        logo_en = ''
        logo_ru = ''
        logo = row[2]
        status = row[1]
        sort_order = ''
        company_id = row[0]

        #    try:
        #        start_date = parse(row[9]).date().strftime("%d/%m/%Y")
        #    except Exception:
        #        start_date = row[9]

        sanction = company_nazk_ua.CompanyNAZKUA(company_id=company_id, sort_order=sort_order, status=status, logo=logo, logo_ru=logo_ru, logo_en=logo_en,
                 name=name, name_en=name_en, name_uk=name_uk, name_ru=name_ru, country=country, category=category, subcategory_1=subcategory_1,
                 subcategory_2=subcategory_2, subcategory_3=subcategory_3, ogrn=ogrn, inn=inn, reasoning_uk=reasoning_uk, reasoning_en=reasoning_en,
                 reasoning_ru=reasoning_ru, address_uk=address_uk, address_en=address_en, address_ru=address_ru, sanctions_ua=sanctions_ua, sanctions_ua_date=sanctions_ua_date,
                 url_es=url_es, url_gb=url_gb,
                 url_us=url_us, url_ca=url_ca, url_ch=url_ch, url_au=url_au, url_jp=url_jp, url_ua=url_ua, url_nz=url_nz, link=link, link_archive=link_archive,
                 relations_person=relations_person, relations_company=relations_company)

        return sanction


def import_person_record_from_json(record):
    sanctions_ua_date = record.sanctions_ua_date
    sanctions_ua = record.sanctions_ua
    relations_company = record.relations_company
    relations_person = record.relations_person
    link_archive = record.link_archive
    link = record.link
    city_bd_en = record.city_bd_en
    city_bd_ru = record.city_bd_ru
    city_bd_uk = record.city_bd_uk
    itn = record.itn
    date_dead = record.date_dead
    date_bd = record.date_bd
    synchron = record.synchron
    top_50 = record.top_50
    status = record.status
    photo_name = record.photo_name
    url_nz = record.url_nz
    url_ua = record.url_ua
    url_jp = record.url_jp
    url_au = record.url_au
    url_ch = record.url_ch
    url_ca = record.url_ca
    url_us = record.url_us
    url_gb = record.url_gb
    url_es = record.url_es
    subcategory_3 = record.subcategory_3
    subcategory_2 = record.subcategory_2
    subcategory_1 = record.subcategory_1
    category = record.category
    reasoning_ru = record.reasoning_ru
    reasoning_en = record.reasoning_en
    reasoning_uk = record.reasoning_uk
    position_ru = record.position_ru
    position_en = record.position_en
    position_uk = record.position_uk
    country = record.country
    name_uk = record.name_uk
    name_ru = record.name_ru
    name_en = record.name_en
    person_id = record.person_id

    #    try:
    #        start_date = parse(row[9]).date().strftime("%d/%m/%Y")
    #    except Exception:
    #        start_date = row[9]

    sanction = individual_nazk_ua.IndividualNAZKUA(person_id=person_id, name_en=name_en, name_ru=name_ru, name_uk=name_uk, country=country,
                                                   position_uk=position_uk,
                                                   position_en=position_en, position_ru=position_ru, reasoning_uk=reasoning_uk, reasoning_en=reasoning_en,
                                                   reasoning_ru=reasoning_ru, category=category, subcategory_1=subcategory_1,
                                                   subcategory_2=subcategory_2, subcategory_3=subcategory_3, sanctions_ua=sanctions_ua,
                                                   sanctions_ua_date=sanctions_ua_date, url_es=url_es, url_gb=url_gb,
                                                   url_us=url_us, url_ca=url_ca, url_ch=url_ch, url_au=url_au, url_jp=url_jp, url_ua=url_ua,
                                                   url_nz=url_nz,
                                                   photo_name=photo_name, status=status, top_50=top_50, synchron=synchron, date_bd=date_bd,
                                                   date_dead=date_dead, itn=itn,
                                                   city_bd_uk=city_bd_uk, city_bd_ru=city_bd_ru, city_bd_en=city_bd_en,
                                                   link=link, link_archive=link_archive,
                                                   relations_person=relations_person, relations_company=relations_company)

    return sanction

def import_company_record_from_json(record):
    sanctions_ua = record.sanctions_ua
    sanctions_ua_date = record.sanctions_ua_date
    relations_company = record.relations_company
    relations_person = record.relations_person
    link_archive = record.link_archive
    link = record.link
    url_nz = record.url_nz
    url_ua = record.url_ua
    url_jp = record.url_jp
    url_au = record.url_au
    url_ch = record.url_ch
    url_ca = record.url_ca
    url_us = record.url_us
    url_gb = record.url_gb
    url_es = record.url_es
    address_ru = record.address_ru
    address_en = record.address_en
    address_uk = record.address_uk
    reasoning_ru = record.reasoning_ru
    reasoning_en = record.reasoning_en
    reasoning_uk = record.reasoning_uk
    inn = record.inn
    ogrn = record.ogrn
    subcategory_3 = record.subcategory_3
    subcategory_2 = record.subcategory_2
    subcategory_1 = record.subcategory_1
    category = record.category
    country = record.country
    name_ru = record.name_ru
    name_uk = record.name_uk
    name_en = record.name_en
    name = record.name
    logo_en = record.logo_en
    logo_ru = record.logo_ru
    logo = record.logo
    status = record.status
    sort_order = record.sort_order
    company_id = record.company_id

    #    try:
    #        start_date = parse(row[9]).date().strftime("%d/%m/%Y")
    #    except Exception:
    #        start_date = row[9]

    sanction = company_nazk_ua.CompanyNAZKUA(company_id=company_id, sort_order=sort_order, status=status, logo=logo,
                                             logo_ru=logo_ru, logo_en=logo_en,
                                             name=name, name_en=name_en, name_uk=name_uk, name_ru=name_ru,
                                             country=country, category=category, subcategory_1=subcategory_1,
                                             subcategory_2=subcategory_2, subcategory_3=subcategory_3, ogrn=ogrn,
                                             inn=inn, reasoning_uk=reasoning_uk, reasoning_en=reasoning_en,
                                             reasoning_ru=reasoning_ru, address_uk=address_uk, address_en=address_en,
                                             address_ru=address_ru, sanctions_ua=sanctions_ua,
                                             sanctions_ua_date=sanctions_ua_date,
                                             url_es=url_es, url_gb=url_gb,
                                             url_us=url_us, url_ca=url_ca, url_ch=url_ch, url_au=url_au, url_jp=url_jp,
                                             url_ua=url_ua, url_nz=url_nz, link=link, link_archive=link_archive,
                                             relations_person=relations_person, relations_company=relations_company)
    return sanction