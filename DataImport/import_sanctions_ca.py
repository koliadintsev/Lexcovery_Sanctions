import os

from lxml import etree
from DataModel.CA import sanction_ca
from Lexcovery_Sanctions.settings import STATIC_ROOT
from Lexcovery_Sanctions import settings
import requests
import datetime
import copy
import aiohttp
import asyncio
import json

SANCTIONS_LIST = os.path.join(settings.BASE_DIR,  'static') + "/Sanctions/CA/sema-lmes.xml"
XML_URL = "https://www.international.gc.ca/world-monde/assets/office_docs/international_relations-relations_internationales/sanctions/sema-lmes.xml"

sanctions = []


async def get_list_xml(url, session):
    #response = requests.get(url)
    response = await session.request(method='GET', url=url)
    if response.ok:
        doc = await response.read()
        d = copy.deepcopy(doc)
        return d
    else:
        return


async def import_data_from_web(session):
    global sanctions
    parser = etree.XMLParser(recover=True, huge_tree=True)
    today = datetime.datetime.today()
    last_update = today.strftime("%d/%m/%Y")

    xml_text = await get_list_xml(XML_URL, session)

    #doc_id = 0

    file_xml = etree.fromstring(xml_text, parser=parser)

    await asyncio.gather(*[import_from_element_async(element) for element in file_xml.getchildren()])

    #print('import finished')

    return sanctions, last_update


async def import_from_element_async(element):
    doc_id = 0
    if element.tag == "record":
        import_data_from_element(element, doc_id)
        element.clear()
        doc_id = doc_id + 1


async def import_data_from_xml():
    global sanctions
    parser = etree.XMLParser(recover=True, huge_tree=True)
    today = datetime.datetime.today()
    last_update = today.strftime("%d/%m/%Y")

    doc_id = 0
    for event, element in etree.iterparse(SANCTIONS_LIST, tag="record", recover=True, huge_tree=True, ):
        import_data_from_element(element, doc_id)
        element.clear()
        doc_id = doc_id + 1

#    print('import finished')
    return sanctions, last_update


def import_data_from_element(doc, doc_id):
    global sanctions

    title = ''
    element_id = doc_id
    aliases = ''
    item_number = ''
    schedule = ''
    date_of_birth = ''
    given_name = ''
    last_name = ''
    entity = ''
    country = ''

    for item in doc.getchildren():
        if item.tag == 'Country':
            country = item.text
        elif item.tag == 'LastName':
            last_name = item.text
        elif item.tag == 'GivenName':
            given_name = item.text
        elif item.tag == 'DateOfBirth':
            date_of_birth = item.text
        elif item.tag == 'Schedule':
            schedule = item.text
        elif item.tag == 'Item':
            item_number = item.text
        elif item.tag == 'Title':
            title = item.text
        elif item.tag == 'Aliases':
            aliases = item.text
        elif item.tag == 'Entity':
            entity = item.text

    sanction = sanction_ca.SanctionCA(country=country, entity=entity, last_name=last_name, given_name=given_name,
                                      date_of_birth=date_of_birth, schedule=schedule, item=item_number, aliases=aliases,
                                      title=title, id=element_id)
    sanctions.append(sanction)


def import_data_from_json(element):

    title = element.title
    element_id = element.id
    aliases = element.aliases
    item_number = element.item
    schedule = element.schedule
    date_of_birth = element.date_of_birth
    given_name = element.given_name
    last_name = element.last_name
    entity = element.entity
    country = element.country

    sanction = sanction_ca.SanctionCA(country=country, entity=entity, last_name=last_name, given_name=given_name,
                                      date_of_birth=date_of_birth, schedule=schedule, item=item_number, aliases=aliases,
                                      title=title, id=element_id)
    return sanction


