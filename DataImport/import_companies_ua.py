# -*- coding: utf-8 -*-
import os

from lxml import etree
import copy
from DataModel.UA.company_ua import CompanyUa
from Lexcovery_Sanctions import settings
import asyncio

FILENAME = os.path.join(settings.BASE_DIR,  'static') + "/Companies/edr_full.xml"
RUSSIAN_COMPANIES = os.path.join(settings.BASE_DIR,  'static') + "/Companies/russian_edr_full.xml"
companies = []
russianCompanies = etree


def find_russian_data_from_xml():
    global russianCompanies
    root = russianCompanies.Element('root')
    #parser = etree.XMLParser(recover=True, huge_tree=True)

    for event, element in etree.iterparse(FILENAME, tag="SUBJECT", recover=True, huge_tree=True):
        find_russian_company(element, root)
        element.clear()

    #executor = concurrent.futures.ThreadPoolExecutor(100)
    #futures = [executor.submit(find_russian_company, item, root) for item in etree.iterparse(FILENAME, tag="RECORD")]
    #concurrent.futures.wait(futures)

    print('import finished')

    xml_data = etree.tounicode(root)  # binary string
    with open(RUSSIAN_COMPANIES, 'w') as f:  # Write in XML file as utf-8
        f.write(xml_data)

    print('russians found and recorded')


async def import_data_from_xml():
    global companies
    #parser = etree.XMLParser(recover=True, huge_tree=True)

    #tree = etree.parse(FILENAME, parser)
    #file = tree.getroot()
    await asyncio.gather(*[import_data_from_element(element) for event, element in etree.iterparse(FILENAME, tag="RECORD", recover=True, huge_tree=True)])

    '''for event, element in :
        import_data_from_element(element)
        element.clear()'''

    """
    tree = ET.fromstring(file.read().strip())
    executor = concurrent.futures.ThreadPoolExecutor(100)
    futures = [executor.submit(import_data_from_element, item, companies) for item in tree.findall('.//document')]
    concurrent.futures.wait(futures)
    """
    print('import finished')
    return companies


def find_russian_company(doc, root):
    global russianCompanies
    russian = False

    for item in doc.getchildren():
        if item.tag == 'STAN' and item.text == '??????????????????':
            return
        elif item.tag == 'BENEFICIARIES':
            for person in item.getchildren():
                if person.tag == 'BENEFICIARY':
                    if not isinstance(person.text, type(None)):
                        if person.text.find('??????????;') != -1 or person.text.find('?????????????????? ??????????????????;') != -1 or \
                                person.text.find(' ????;') != -1 or person.text.find('????????????????;') != -1 or person.text.find('??????????????????;') != -1:
                            russian = True
                            beneficiary = person.text
        elif item.tag == 'FOUNDERS':
            for person in item.getchildren():
                if person.tag == 'FOUNDER':
                    if not isinstance(person.text, type(None)):
                        if person.text.find('??????????;') != -1 or person.text.find('?????????????????? ??????????????????;') != -1 or \
                                person.text.find(' ????;') != -1 or person.text.find('????????????????;') != -1 or person.text.find('??????????????????;') != -1:
                            russian = True
                            founder = person.text
    if russian:
        child = copy.deepcopy(doc)
        root.append(child)


async def import_data_from_element(doc):
    global companies
    name = ''
    shortname = ''
    code = 0
    address = ''
    kved = ''
    boss = ''
    stan = ''
    beneficiaries = []
    founders = []

    for item in doc.getchildren():
        if item.tag == 'NAME':
            name = item.text
        elif item.tag == 'SHORT_NAME':
            shortname = item.text
        elif item.tag == 'EDRPOU':
            code = item.text
        elif item.tag == 'ADDRESS':
            address = item.text
        elif item.tag == 'KVED':
            kved = item.text
        elif item.tag == 'BOSS':
            boss = item.text
        elif item.tag == 'STAN':
            stan = item.text
            if stan == '??????????????????':
                return
        elif item.tag == 'BENEFICIARIES':
            for person in item.getchildren():
                if person.tag == 'BENEFICIARY':
                    if not isinstance(person.text, type(None)):
                        beneficiaries.append(person.text)
        elif item.tag == 'FOUNDERS':
            for person in item.getchildren():
                if person.tag == 'FOUNDER':
                    if not isinstance(person.text, type(None)):
                        founders.append(person.text)

    company = CompanyUa(name, shortname, code, address, kved, boss, stan)
    company.beneficiaries = beneficiaries
    company.founders = founders

    companies.append(company)
    # print(str(code) + ' added successfully')


def import_data_from_json(element):

    name = element.name
    shortname = element.shortname
    code = element.code
    address = element.address
    kved = element.kved
    boss = element.boss
    stan = element.stan
    beneficiaries = []
    founders = []

    for founder in element.founders:
        founders.append(founder)

    for beneficiary in element.beneficiaries:
        beneficiaries.append(beneficiary)

    company = CompanyUa(name, shortname, code, address, kved, boss, stan)
    company.beneficiaries = beneficiaries
    company.founders = founders

    return company