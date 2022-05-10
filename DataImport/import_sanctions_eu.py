import copy
import datetime
import os

from lxml import etree
from DataModel.EU import sanction_EU_additionailnfo, sanction_EU_contactinfo, sanction_EU, sanction_EU_regulationSummary, \
    sanction_EU_regulationSummary, sanction_EU_name, sanction_EU_regulation, sanction_EU_birthdate, sanction_EU_address, \
    sanction_EU_citizenship, sanction_EU_identificationType, sanction_EU_generic
from Lexcovery_Sanctions.settings import STATIC_ROOT
from Lexcovery_Sanctions import settings
import requests
from dateutil.parser import parse
import aiohttp
import asyncio

SANCTIONS_LIST = os.path.join(settings.BASE_DIR,  'static') + "/Sanctions/EU/sanctions.xml"
sanctions = []
XML_URL = "https://webgate.ec.europa.eu/fsd/fsf/public/files/xmlFullSanctionsList_1_1/content?token=n009exmj"


async def get_list_xml(session):
    #response = requests.get(XML_URL)
    response = await session.request(method='GET', url=XML_URL)
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

    xml_text = await get_list_xml(session)

    doc_id = 0
    file = etree.fromstring(xml_text, parser=parser)
    text = file.get('generationDate')
    date = parse(text).date()
    last_update = date.strftime("%d/%m/%Y")

    await asyncio.gather(*[import_from_element_async(element) for element in file.getchildren()])

    for element in file.getchildren():
        if element.tag == "{http://eu.europa.ec/fpi/fsd/export}export":
            text = element.get('generationDate')
            date = parse(text).date()
            last_update = date.strftime("%d/%m/%Y")

    # print('import finished')

    return sanctions, last_update


async def import_from_element_async(element):
    doc_id = 0
    if element.tag == "{http://eu.europa.ec/fpi/fsd/export}sanctionEntity":
        import_data_from_element(element, doc_id)
        element.clear()
        doc_id = doc_id + 1


async def import_data_from_xml():
    global sanctions
    #parser = etree.XMLParser(recover=True, huge_tree=True)
    last_update = ''

    doc_id = 0
    for event, element in etree.iterparse(SANCTIONS_LIST, tag="{http://eu.europa.ec/fpi/fsd/export}sanctionEntity", recover=True, huge_tree=True, ):
        import_data_from_element(element, doc_id)
        element.clear()
        doc_id = doc_id+1

    for event, element in etree.iterparse(SANCTIONS_LIST, tag="{http://eu.europa.ec/fpi/fsd/export}export", recover=True, huge_tree=True, ):
        text = element.get('generationDate')
        date = parse(text).date()
        last_update = date.strftime("%d/%m/%Y")
    """
    tree = ET.fromstring(file.read().strip())
    executor = concurrent.futures.ThreadPoolExecutor(100)
    futures = [executor.submit(import_data_from_element, item, companies) for item in tree.findall('.//document')]
    concurrent.futures.wait(futures)
    """
    #print('import finished')
    return sanctions, last_update


def find_additional_info(doc):
    info = []
    for child in doc.getchildren():
        child.tag = child.tag.split('}')[-1]
        if child.tag == 'additionalInformation':
            additionalInformation = sanction_EU_additionailnfo.SanctionEUAdditionalInfo()
            additionalInformation.key = child.get('key')
            additionalInformation.value = child.get('value')
            info.append(additionalInformation)
    return info

def find_remark(doc):
    remark = ''
    for child in doc.getchildren():
        child.tag = child.tag.split('}')[-1]
        if child.tag == 'remark':
            if remark == '':
                remark = child.text
            else:
                text = remark + child.text + "; "
                remark = text
    return remark

def find_regulation_summary(doc):
    summary = sanction_EU_regulationSummary.SanctionEURegulationSummary()
    for child in doc.getchildren():
        child.tag = child.tag.split('}')[-1]
        if child.tag == 'regulationSummary':
            summary.publicationDate = child.get('publicationDate')
            summary.numberTitle = child.get('numberTitle')
            summary.publicationUrl = child.get('publicationUrl')
            summary.regulationType = child.get('regulationType')
    return summary

def import_data_from_element(doc, doc_id):
    global sanctions

    code = ''
    classificationCode = 'P'
    nameAlias = []
    citizenship = []
    birthdate = []
    address = []
    identification = []
    regulation = sanction_EU_regulation.SanctionEURegulation()
    delistingDate = doc.get('delistingDate')
    designationDate = doc.get('designationDate')
    unitedNationId = doc.get('unitedNationId')
    euReferenceNumber = doc.get('euReferenceNumber')
    remark = find_remark(doc)
    additionalInformation = find_additional_info(doc)

    for item in doc.getchildren():
        item.tag=item.tag.split('}')[-1]
        if item.tag == 'regulation':
            regulation = sanction_EU_regulation.SanctionEURegulation()
            regulation.programme = item.get('programme')
            regulation.numberTitle = item.get('numberTitle')
            regulation.entryIntoForceDate = item.get('entryIntoForceDate')
            regulation.publicationDate = item.get('publicationDate')
            regulation.organisationType = item.get('organisationType')
            regulation.regulationType = item.get('regulationType')
            for child in item.getchildren():
                child.tag = child.tag.split('}')[-1]
                if child.tag == 'publicationUrl':
                    regulation.publicationUrl = child.text
                elif child.tag == 'corrigendum':
                    summary = sanction_EU_regulationSummary.SanctionEURegulationSummary()
                    summary.publicationDate = child.get('publicationDate')
                    summary.numberTitle = child.get('numberTitle')
                    summary.publicationUrl = child.get('publicationUrl')
                    summary.regulationType = child.get('regulationType')
                    regulation.corrigendum = find_regulation_summary(child)
        elif item.tag == 'subjectType':
            code = item.get('code')
            classificationCode = item.get('classificationCode')
        elif item.tag == 'nameAlias':
            name = sanction_EU_name.SanctionEUName()
            name.regulationSummary = find_regulation_summary(item)
            name.regulationLanguage = item.get('regulationLanguage')
            name.title = item.get('title')
            if item.get('strong') == 'true':
                name.strong = True
            name.nameLanguage = item.get('nameLanguage')
            name.gender = item.get('gender')
            name.function = item.get('function')
            name.wholeName = item.get('wholeName')
            name.lastName = item.get('lastName')
            name.middleName = item.get('middleName')
            name.firstName = item.get('firstName')
            name.remark = find_remark(item)
            name.additionalInformation = find_additional_info(item)
            nameAlias.append(name)
        elif item.tag == 'citizenship':
            citizen = sanction_EU_citizenship.SanctionEUCitizenship()
            citizen.regulationSummary = find_regulation_summary(item)
            citizen.regulationLanguage = item.get('regulationLanguage')
            citizen.countryDescription = item.get('countryDescription')
            citizen.countryIso2Code = item.get('countryIso2Code')
            citizen.region = item.get('region')
            citizen.disenfranchisementDate = item.get('disenfranchisementDate')
            citizen.acquisitionDate = item.get('acquisitionDate')
            citizen.remark = find_remark(item)
            citizen.additionalInformation = find_additional_info(item)
            citizenship.append(citizen)
        elif item.tag == 'birthdate':
            birth = sanction_EU_birthdate.SanctionEUBirthdate()
            birth.regulationSummary = find_regulation_summary(item)
            birth.remark = find_remark(item)
            birth.additionalInformation = find_additional_info(item)
            birth.regulationLanguage = item.get('regulationLanguage')
            birth.countryDescription = item.get('countryDescription')
            birth.countryIso2Code = item.get('countryIso2Code')
            birth.place = item.get('place')
            birth.region = item.get('region')
            birth.yearRangeTo = item.get('yearRangeTo')
            birth.yearRangeFrom = item.get('yearRangeFrom')
            birth.year = item.get('year')
            birth.monthOfYear = item.get('monthOfYear')
            birth.dayOfMonth = item.get('dayOfMonth')
            birth.birthdate = item.get('birthdate')
            birth.zipCode = item.get('zipCode')
            birth.city = item.get('city')
            birth.calendarType = item.get('calendarType')
            if item.get('circa') == 'true':
                birth.circa = True
            birthdate.append(birth)
        elif item.tag == 'address':
            add = sanction_EU_address.SanctionEUAddress()
            add.regulationSummary = find_regulation_summary(item)
            add.remark = find_remark(item)
            add.additionalInformation = find_additional_info(item)
            info = []
            for child in item.getchildren():
                child.tag = child.tag.split('}')[-1]
                if child.tag == 'contactInfo':
                    contactInfo = sanction_EU_contactinfo.SanctionEUContactInfo()
                    contactInfo.key = child.get('key')
                    contactInfo.value = child.get('value')
                    info.append(contactInfo)
            add.contactInfo = info
            if item.get('asAtListingTime') == 'true':
                add.asAtListingTime = True
            add.zipCode = item.get('zipCode')
            add.poBox = item.get('poBox')
            add.city = item.get('city')
            add.street = item.get('street')
            add.regulationSummary = item.get('regulationSummary')
            add.regulationLanguage = item.get('regulationLanguage')
            add.countryDescription = item.get('countryDescription')
            add.countryIso2Code = item.get('countryIso2Code')
            add.place = item.get('place')
            add.region = item.get('region')
            address.append(add)
        elif item.tag == 'identification':
            document = sanction_EU_identificationType.SanctionEUIdentificationType()
            document.regulationSummary = find_regulation_summary(item)
            document.remark = find_remark(item)
            document.additionalInformation = find_additional_info(item)
            if item.get('diplomatic') == 'true':
                document.diplomatic = True
            if item.get('knownExpired') == 'true':
                document.knownExpired = True
            if item.get('knownFalse') == 'true':
                document.knownFalse = True
            if item.get('reportedLost') == 'true':
                document.reportedLost = True
            if item.get('revokedByIssuer') == 'true':
                document.revokedByIssuer = True
            document.regulationLanguage = item.get('regulationLanguage')
            document.countryDescription = item.get('countryDescription')
            document.identificationTypeDescription = item.get('identificationTypeDescription')
            document.identificationTypeCode = item.get('identificationTypeCode')
            document.region = item.get('region')
            document.countryIso2Code = item.get('countryIso2Code')
            document.validTo = item.get('validTo')
            document.validFrom = item.get('validFrom')
            document.number = item.get('number')
            document.nameOnDocument = item.get('nameOnDocument')
            document.latinNumber = item.get('latinNumber')
            document.issuedBy = item.get('issuedBy')
            document.issueDate = item.get('issueDate')
            identification.append(document)

    sanction = sanction_EU.SanctionEU(code=code, classificationCode=classificationCode, nameAlias=nameAlias,
                                      citizenship=citizenship, birthdate=birthdate, address=address, regulation=regulation,
                                      identification=identification, delistingDate=delistingDate, designationDate=designationDate,
                                      unitedNationId=unitedNationId, euReferenceNumber=euReferenceNumber, id=doc_id)
    sanction.additionalInformation = additionalInformation
    sanction.remark = remark
    sanctions.append(sanction)
    #print(euReferenceNumber + ' added successfully')


def import_data_from_json(element):
    code = element.code
    classificationCode = element.classificationCode
    nameAlias = []
    citizenship = []
    birthdate = []
    address = []
    identification = []
    regulation = sanction_EU_regulation.SanctionEURegulation()
    delistingDate = element.delistingDate
    designationDate = element.designationDate
    unitedNationId = element.unitedNationId
    euReferenceNumber = element.euReferenceNumber

    sanction = sanction_EU.SanctionEU()

    sanction.id = element.id
    sanction.remark = element.remark

    reg = element.regulation
    regulation.programme = reg['programme']
    regulation.numberTitle = reg['numberTitle']
    regulation.entryIntoForceDate = reg['entryIntoForceDate']
    regulation.publicationDate = reg['publicationDate']
    regulation.organisationType = reg['organisationType']
    regulation.regulationType = reg['regulationType']
    regulation.publicationUrl = reg['publicationUrl']
    if reg['corrigendum']:
        summary = sanction_EU_regulationSummary.SanctionEURegulationSummary()
        item = reg['corrigendum']
        summary.publicationDate = item['publicationDate']
        summary.numberTitle = item['numberTitle']
        summary.publicationUrl = item['publicationUrl']
        summary.regulationType = item['regulationType']
        regulation.corrigendum = summary

    add_info = []
    for item in element.additionalInformation:
        additionalInformation = sanction_EU_additionailnfo.SanctionEUAdditionalInfo()
        additionalInformation.key = item['key']
        additionalInformation.value = item['value']
        add_info.append(additionalInformation)
    sanction.additionalInformation = add_info

    for item in element.nameAlias:
        name = sanction_EU_name.SanctionEUName()
        name.regulationSummary = find_regulation_summary_json(item)
        name.regulationLanguage = item['regulationLanguage']
        name.title = item['title']
        name.strong = item['strong']
        name.nameLanguage = item['nameLanguage']
        name.gender = item['gender']
        name.function = item['function']
        name.wholeName = item['wholeName']
        name.lastName = item['lastName']
        name.middleName = item['middleName']
        name.firstName = item['firstName']
        name.remark = item['remark']
        name.additionalInformation = find_additional_info_json(item)
        nameAlias.append(name)

    for item in element.citizenship:
        citizen = sanction_EU_citizenship.SanctionEUCitizenship()
        citizen.regulationSummary = find_regulation_summary_json(item)
        citizen.regulationLanguage = item['regulationLanguage']
        citizen.countryDescription = item['countryDescription']
        citizen.countryIso2Code = item['countryIso2Code']
        citizen.region = item['region']
        citizen.disenfranchisementDate = item['disenfranchisementDate']
        citizen.acquisitionDate = item['acquisitionDate']
        citizen.remark = item['remark']
        citizen.additionalInformation = find_additional_info_json(item)
        citizenship.append(citizen)

    for item in element.birthdate:
        birth = sanction_EU_birthdate.SanctionEUBirthdate()
        birth.regulationSummary = find_regulation_summary_json(item)
        birth.remark = item['remark']
        birth.additionalInformation = find_additional_info_json(item)
        birth.regulationLanguage = item['regulationLanguage']
        birth.countryDescription = item['countryDescription']
        birth.countryIso2Code = item['countryIso2Code']
        birth.place = item['place']
        birth.region = item['region']
        birth.yearRangeTo = item['yearRangeTo']
        birth.yearRangeFrom = item['yearRangeFrom']
        birth.year = item['year']
        birth.monthOfYear = item['monthOfYear']
        birth.dayOfMonth = item['dayOfMonth']
        birth.birthdate = item['birthdate']
        birth.zipCode = item['zipCode']
        birth.city = item['city']
        birth.calendarType = item['calendarType']
        birth.circa = item['circa']
        birthdate.append(birth)

    for item in element.address:
        add = sanction_EU_address.SanctionEUAddress()
        #add.regulationSummary = find_regulation_summary_json(item)
        add.remark = item['remark']
        add.additionalInformation = find_additional_info_json(item)
        info = []
        for contact in item['contactInfo']:
            contactInfo = sanction_EU_contactinfo.SanctionEUContactInfo()
            contactInfo.key = contact['key']
            contactInfo.value = contact['value']
            info.append(contactInfo)
        add.contactInfo = info
        add.asAtListingTime = item['asAtListingTime']
        add.zipCode = item['zipCode']
        add.poBox = item['poBox']
        add.city = item['city']
        add.street = item['street']
        add.regulationSummary = item['regulationSummary']
        add.regulationLanguage = item['regulationLanguage']
        add.countryDescription = item['countryDescription']
        add.countryIso2Code = item['countryIso2Code']
        add.place = item['place']
        add.region = item['region']
        address.append(add)

    for item in element.identification:
        document = sanction_EU_identificationType.SanctionEUIdentificationType()
        document.regulationSummary = find_regulation_summary_json(item)
        document.remark = item['remark']
        document.additionalInformation = find_additional_info_json(item)
        document.diplomatic = item['diplomatic']
        document.knownExpired = item['knownExpired']
        document.knownFalse = item['knownFalse']
        document.reportedLost = item['reportedLost']
        document.revokedByIssuer = item['revokedByIssuer']
        document.regulationLanguage = item['regulationLanguage']
        document.countryDescription = item['countryDescription']
        document.identificationTypeDescription = item['identificationTypeDescription']
        document.identificationTypeCode = item['identificationTypeCode']
        document.region = item['region']
        document.countryIso2Code = item['countryIso2Code']
        document.validTo = item['validTo']
        document.validFrom = item['validFrom']
        document.number = item['number']
        document.nameOnDocument = item['nameOnDocument']
        document.latinNumber = item['latinNumber']
        document.issuedBy = item['issuedBy']
        document.issueDate = item['issueDate']
        identification.append(document)

    sanction.code = code
    sanction.classificationCode = classificationCode
    sanction.nameAlias = nameAlias
    sanction.regulation = regulation
    sanction.citizenship = citizenship
    sanction.birthdate = birthdate
    sanction.address = address
    sanction.identification = identification
    sanction.delistingDate = delistingDate
    sanction.designationDate = designationDate
    sanction.unitedNationId = unitedNationId
    sanction.euReferenceNumber = euReferenceNumber
    return sanction


def find_additional_info_json(doc):
    info = []
    for item in doc['additionalInformation']:
        additionalInformation = sanction_EU_additionailnfo.SanctionEUAdditionalInfo()
        additionalInformation.key = item['key']
        additionalInformation.value = item['value']
        info.append(additionalInformation)
    return info


def find_regulation_summary_json(doc):
    summary = sanction_EU_regulationSummary.SanctionEURegulationSummary()
    item = doc['regulationSummary']
    summary.publicationDate = item['publicationDate']
    summary.numberTitle = item['numberTitle']
    summary.publicationUrl = item['publicationUrl']
    summary.regulationType = item['regulationType']
    return summary

