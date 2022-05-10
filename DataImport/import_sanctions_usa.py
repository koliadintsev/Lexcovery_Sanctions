import os

from lxml import etree
from DataModel.USA import sanction_USA, sanction_USA_aka, sanction_USA_address, \
    sanction_USA_document, sanction_USA_nationality, sanction_USA_placeofbirth, sanction_USA_dateofbirth
from DataModel.USA import sanction_USA_vessel
from Lexcovery_Sanctions.settings import STATIC_ROOT
from Lexcovery_Sanctions import settings
import requests
import datetime
import copy
import aiohttp
import asyncio
import json

SANCTIONS_SDN = os.path.join(settings.BASE_DIR,  'static') + "/Sanctions/USA/sdn.xml"
SANCTIONS_CONS = os.path.join(settings.BASE_DIR,  'static') + "/Sanctions/USA/consolidated.xml"

XML_URL_SDN = "https://www.treasury.gov/ofac/downloads/sdn.xml"
XML_URL_CONS = "https://www.treasury.gov/ofac/downloads/consolidated/consolidated.xml"

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
    last_update = ''
    update_sdn = datetime.datetime.today()
    update_cons = datetime.datetime.today()

    sdn_xml_text = await get_list_xml(XML_URL_SDN, session)
    cons_xml_text = await get_list_xml(XML_URL_CONS, session)

    #doc_id = 0

    file_sdn = etree.fromstring(sdn_xml_text, parser=parser)
    file_cons = etree.fromstring(cons_xml_text, parser=parser)

    await asyncio.gather(*[import_from_element_async(element) for element in file_sdn.getchildren()])
    await asyncio.gather(*[import_from_element_async(element) for element in file_cons.getchildren()])

    for element in file_sdn.getchildren():
        if element.tag == "{http://tempuri.org/sdnList.xsd}publshInformation":
            for item in element.getchildren():
                item.tag = item.tag.split('}')[-1]
                if item.tag == 'Publish_Date':
                    update_sdn = datetime.datetime.strptime(item.text, "%m/%d/%Y").date()

    for element in file_cons.getchildren():
        if element.tag == "{http://tempuri.org/sdnList.xsd}publshInformation":
            for item in element.getchildren():
                item.tag = item.tag.split('}')[-1]
                if item.tag == 'Publish_Date':
                    update_cons = datetime.datetime.strptime(item.text, "%m/%d/%Y").date()

    if update_sdn > update_cons:
        last_update = update_sdn.strftime("%d/%m/%Y")
    else:
        last_update = update_cons.strftime("%d/%m/%Y")

    #print('import finished')

    return sanctions, last_update

async def import_from_element_async(element):
    doc_id = 0
    if element.tag == "{http://tempuri.org/sdnList.xsd}sdnEntry":
        import_data_from_element(element, doc_id)
        element.clear()
        doc_id = doc_id + 1

async def import_data_from_xml():
    global sanctions
    #parser = etree.XMLParser(recover=True, huge_tree=True)
    last_update = ''
    update_sdn = datetime.datetime.today()
    update_cons = datetime.datetime.today()

    doc_id = 0
    for event, element in etree.iterparse(SANCTIONS_SDN, tag="{http://tempuri.org/sdnList.xsd}sdnEntry", recover=True, huge_tree=True, ):
        import_data_from_element(element, doc_id)
        element.clear()
        doc_id = doc_id +1
    for event, element in etree.iterparse(SANCTIONS_SDN, tag="{http://tempuri.org/sdnList.xsd}publshInformation", recover=True, huge_tree=True, ):
        for item in element.getchildren():
            item.tag = item.tag.split('}')[-1]
            if item.tag == 'Publish_Date':
                update_sdn = datetime.datetime.strptime(item.text, "%m/%d/%Y").date()

    for event, element in etree.iterparse(SANCTIONS_CONS, tag="{http://tempuri.org/sdnList.xsd}sdnEntry", recover=True, huge_tree=True):
        import_data_from_element(element, doc_id)
        element.clear()
        doc_id = doc_id+1
    for event, element in etree.iterparse(SANCTIONS_CONS, tag="{http://tempuri.org/sdnList.xsd}publshInformation", recover=True, huge_tree=True):
        for item in element.getchildren():
            item.tag = item.tag.split('}')[-1]
            if item.tag == 'Publish_Date':
                update_cons = datetime.datetime.strptime(item.text, "%m/%d/%Y").date()

    if update_sdn > update_cons:
        last_update = update_sdn.strftime("%d/%m/%Y")
    else:
        last_update = update_cons.strftime("%d/%m/%Y")

    """
    tree = ET.fromstring(file.read().strip())
    executor = concurrent.futures.ThreadPoolExecutor(100)
    futures = [executor.submit(import_data_from_element, item, companies) for item in tree.findall('.//document')]
    concurrent.futures.wait(futures)
    """
#    print('import finished')
    return sanctions, last_update


def import_data_from_element(doc, doc_id):
    global sanctions

    uid = ''
    firstName = ''
    lastName = ''
    title = ''
    sdnType = ''
    remarks = ''
    programList = []
    idList = []
    akaList = []
    addressList = []
    nationalityList = []
    citizenshipList = []
    dateOfBirthList = []
    placeOfBirthList = []
    vesselInfo = []

    for item in doc.getchildren():
        item.tag=item.tag.split('}')[-1]
        if item.tag == 'uid':
            uid = int(item.text)
        elif item.tag == 'firstName':
            firstName = item.text
        elif item.tag == 'lastName':
            lastName = item.text
        elif item.tag == 'title':
            title = item.text
        elif item.tag == 'sdnType':
            sdnType = item.text
        elif item.tag == 'remarks':
            remarks = item.text
        elif item.tag == 'programList':
            for child in item.getchildren():
                programList.append(child.text)
        elif item.tag == 'idList':
            for child in item.getchildren():
                document = sanction_USA_document.SanctionUSADocument()
                for c in child.getchildren():
                    c.tag = c.tag.split('}')[-1]
                    if c.tag == 'uid':
                        document.uid = int(c.text)
                    elif c.tag == 'idType':
                        document.idType = c.text
                    elif c.tag == 'issueDate':
                        document.issueDate = c.text
                    elif c.tag == 'expirationDate':
                        document.expirationDate = c.text
                    elif c.tag == 'idNumber':
                        document.idNumber = c.text
                    elif c.tag == 'idCountry':
                        document.idCountry = c.text
                idList.append(document)
        elif item.tag == 'akaList':
            for child in item.getchildren():
                aka = sanction_USA_aka.SanctionUSAAka()
                for c in child.getchildren():
                    c.tag = c.tag.split('}')[-1]
                    if c.tag == 'uid':
                        aka.uid = int(c.text)
                    elif c.tag == 'type':
                        aka.type = c.text
                    elif c.tag == 'lastName':
                        aka.lastName = c.text
                    elif c.tag == 'firstName':
                        aka.firstName = c.text
                    elif c.tag == 'category':
                        aka.category = c.text
                if not aka.firstName:
                    aka.wholeName = aka.lastName
                else:
                    aka.wholeName = aka.firstName + ' ' + aka.lastName
                akaList.append(aka)
        elif item.tag == 'addressList':
            for child in item.getchildren():
                child.tag = child.tag.split('}')[-1]
                address = sanction_USA_address.SanctionUSAAddress()
                for c in child.getchildren():
                    c.tag = c.tag.split('}')[-1]
                    if c.tag == 'uid':
                        address.uid = int(c.text)
                    elif c.tag == 'address1':
                        address.address1 = c.text
                    elif c.tag == 'address2':
                        address.address2 = c.text
                    elif c.tag == 'address3':
                        address.address3 = c.text
                    elif c.tag == 'country':
                        address.country = c.text
                    elif c.tag == 'city':
                        address.city = c.text
                    elif c.tag == 'postalCode':
                        address.postalCode = c.text
                    elif c.tag == 'stateOrProvince':
                        address.stateOrProvince = c.text
                addressList.append(address)
        elif item.tag == 'nationalityList':
            for child in item.getchildren():
                nationality = sanction_USA_nationality.SanctionUSANationality()
                for c in child.getchildren():
                    c.tag = c.tag.split('}')[-1]
                    if c.tag == 'uid':
                        nationality.uid = int(c.text)
                    elif c.tag == 'country':
                        nationality.country = c.text
                    elif c.tag == 'mainEntry':
                        result = False
                        if c.text == 'true':
                            result = True
                        nationality.mainEntry = result
                nationalityList.append(nationality)
        elif item.tag == 'citizenshipList':
            for child in item.getchildren():
                citizenship = sanction_USA_nationality.SanctionUSANationality()
                for c in child.getchildren():
                    c.tag = c.tag.split('}')[-1]
                    if c.tag == 'uid':
                        citizenship.uid = int(c.text)
                    elif c.tag == 'country':
                        citizenship.country = c.text
                    elif c.tag == 'mainEntry':
                        result = False
                        if c.text == 'true':
                            result = True
                        citizenship.mainEntry = result
                citizenshipList.append(citizenship)
        elif item.tag == 'dateOfBirthList':
            for child in item.getchildren():
                dateOfBirth = sanction_USA_dateofbirth.SanctionUSADateOfBirth()
                for c in child.getchildren():
                    c.tag = c.tag.split('}')[-1]
                    if c.tag == 'uid':
                        dateOfBirth.uid = int(c.text)
                    elif c.tag == 'dateOfBirth':
                        dateOfBirth.dateOfBirth = c.text
                    elif c.tag == 'mainEntry':
                        result = False
                        if c.text == 'true':
                            result = True
                        dateOfBirth.mainEntry = result
                dateOfBirthList.append(dateOfBirth)
        elif item.tag == 'placeOfBirthList':
            for child in item.getchildren():
                placeOfBirth = sanction_USA_placeofbirth.SanctionUSAPlaceOfBirth()
                for c in child.getchildren():
                    c.tag = c.tag.split('}')[-1]
                    if c.tag == 'uid':
                        placeOfBirth.uid = int(c.text)
                    elif c.tag == 'placeOfBirth':
                        placeOfBirth.placeOfBirth = c.text
                    elif c.tag == 'mainEntry':
                        result = False
                        if c.text == 'true':
                            result = True
                        placeOfBirth.mainEntry = result
                placeOfBirthList.append(placeOfBirth)
        elif item.tag == 'vesselInfo':
            for child in item.getchildren():
                vessel = sanction_USA_vessel.SanctionUSAVessel()
                for c in child.getchildren():
                    c.tag = c.tag.split('}')[-1]
                    if c.tag == 'uid':
                        vessel.uid = int(c.text)
                    elif c.tag == 'vesselOwner':
                        vessel.vesselOwner = c.text
                    elif c.tag == 'vesselType':
                        vessel.vesselType = c.text
                    elif c.tag == 'vesselFlag':
                        vessel.vesselFlag = c.text
                    elif c.tag == 'tonnage':
                        vessel.tonnage = c.text
                    elif c.tag == 'callSign':
                        vessel.callSign = c.text
                    elif c.tag == 'grossRegisteredTonnage':
                        vessel.grossRegisteredTonnage = c.text
                vesselInfo.append(vessel)
    sanction = sanction_USA.SanctionUSA(uid, firstName, lastName, title, sdnType, remarks, programList, idList,
                                        akaList, addressList, nationalityList, citizenshipList, dateOfBirthList,
                                        placeOfBirthList, vesselInfo, doc_id)
    sanctions.append(sanction)
    #print(str(uid) + ' added successfully')


def import_data_from_json(element):

    uid = element.uid
    firstName = element.firstName
    lastName = element.lastName
    title = element.title
    sdnType = element.sdnType
    remarks = element.remarks
    programList = element.programList
    idList = []
    akaList = []
    addressList = []
    nationalityList = []
    citizenshipList = []
    dateOfBirthList = []
    placeOfBirthList = []
    vesselInfo = []

    for item in element.idList:
        passport = sanction_USA_document.SanctionUSADocument()
        passport.uid = int(item['uid'])
        passport.idType = item['idType']
        passport.issueDate = item['issueDate']
        passport.expirationDate = item['expirationDate']
        passport.idNumber = item['idNumber']
        passport.idCountry = item['idCountry']
        idList.append(passport)

    for item in element.akaList:
        aka = sanction_USA_aka.SanctionUSAAka()
        aka.uid = int(item['uid'])
        aka.type = item['type']
        aka.lastName = item['lastName']
        aka.firstName = item['firstName']
        aka.category = item['category']
        aka.wholeName = item['wholeName']
        akaList.append(aka)

    for item in element.addressList:
        address = sanction_USA_address.SanctionUSAAddress()
        address.uid = int(item['uid'])
        address.address1 = item['address1']
        address.address2 = item['address2']
        address.address3 = item['address3']
        address.country = item['country']
        address.city = item['city']
        address.postalCode = item['postalCode']
        address.stateOrProvince = item['stateOrProvince']
        addressList.append(address)

    for item in element.nationalityList:
        nationality = sanction_USA_nationality.SanctionUSANationality()
        nationality.uid = int(item['uid'])
        nationality.country = item['country']
        nationality.mainEntry = item['mainEntry']
        nationalityList.append(nationality)

    for item in element.citizenshipList:
        nationality = sanction_USA_nationality.SanctionUSANationality()
        nationality.uid = int(item['uid'])
        nationality.country = item['country']
        nationality.mainEntry = item['mainEntry']
        citizenshipList.append(nationality)

    for item in element.dateOfBirthList:
        dateOfBirth = sanction_USA_dateofbirth.SanctionUSADateOfBirth()
        dateOfBirth.uid = int(item['uid'])
        dateOfBirth.dateOfBirth = item['dateOfBirth']
        dateOfBirth.mainEntry = item['mainEntry']
        dateOfBirthList.append(dateOfBirth)

    for item in element.placeOfBirthList:
        placeOfBirth = sanction_USA_placeofbirth.SanctionUSAPlaceOfBirth()
        placeOfBirth.uid = int(item['uid'])
        placeOfBirth.placeOfBirth = item['placeOfBirth']
        placeOfBirth.mainEntry = item['mainEntry']
        placeOfBirthList.append(placeOfBirth)

    for item in element.vesselInfo:
        vessel = sanction_USA_vessel.SanctionUSAVessel()
        vessel.uid = int(item['uid'])
        vessel.vesselOwner = item['vesselOwner']
        vessel.vesselType = item['vesselType']
        vessel.vesselFlag = item['vesselFlag']
        vessel.tonnage = item['tonnage']
        vessel.callSign = item['callSign']
        vessel.grossRegisteredTonnage = item['grossRegisteredTonnage']
        vesselInfo.append(vessel)

    return sanction_USA.SanctionUSA(uid, firstName, lastName, title, sdnType, remarks, programList, idList,
                                        akaList, addressList, nationalityList, citizenshipList, dateOfBirthList,
                                        placeOfBirthList, vesselInfo, element.id)


