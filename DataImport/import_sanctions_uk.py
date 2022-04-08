import copy
import datetime
import os
import aiohttp
import asyncio

from lxml import etree
from DataModel.UK import sanction_UK, sanction_UK_individual, sanction_UK_name, sanction_UK_indicator, \
    sanction_UK_address
from DataModel.UK import sanction_UK_Entity
from Lexcovery_Sanctions.settings import STATIC_ROOT
from Lexcovery_Sanctions import settings
import requests
from bs4 import BeautifulSoup

SANCTIONS_LIST = os.path.join(settings.BASE_DIR,  'static') + "/Sanctions/UK/UK_sanctions_list.xml"
XML_URL = "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1067399/UK_Sanctions_List.xml"
SANCTIONS_WEBSITE = 'https://www.gov.uk/government/publications/the-uk-sanctions-list'
sanctions = []


async def find_link_xml(session):
    response = await session.request(method='GET', url=SANCTIONS_WEBSITE)
    xml_url_web = XML_URL
    if response.ok:
        doc = await response.text()
        text = BeautifulSoup(doc, 'html.parser')
        for link in text.find_all('a'):
            url = link.get('href')
            if 'UK_Sanctions_List.xml' in url:
                xml_url_web = url
        return xml_url_web
    else:
        return XML_URL


async def get_list_xml(session):
    #response = requests.get(XML_URL)
    link = await find_link_xml(session)
    response = await session.request(method='GET', url=link)
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

    await asyncio.gather(*[import_from_element_async(element) for element in file.getchildren()])

    for element in file.getchildren():
        if element.tag == "DateGenerated":
            #date = datetime.datetime.strptime(element.text, "%d/%m/%Y").date()
            #last_update = date.strftime("%d/%m/%Y")
            last_update = element.text

    #print('import finished')

    return sanctions, last_update


async def import_from_element_async(element):
    doc_id = 0
    if element.tag == "Designation":
        import_data_from_element(element, doc_id)
        element.clear()
        doc_id = doc_id + 1

async def import_data_from_xml():
    global sanctions
    #parser = etree.XMLParser(recover=True, huge_tree=True)
    last_update = ''

    doc_id = 0
    for event, element in etree.iterparse(SANCTIONS_LIST, tag="Designation", recover=True, huge_tree=True, ):
        import_data_from_element(element, doc_id)
        element.clear()
        doc_id = doc_id + 1
    for event, element in etree.iterparse(SANCTIONS_LIST, tag="DateGenerated", recover=True, huge_tree=True, ):
        last_update = element.text

    """
    tree = ET.fromstring(file.read().strip())
    executor = concurrent.futures.ThreadPoolExecutor(100)
    futures = [executor.submit(import_data_from_element, item, companies) for item in tree.findall('.//document')]
    concurrent.futures.wait(futures)
    """
    #print('import finished')

    return sanctions, last_update


def import_data_from_element(doc, doc_id):
    global sanctions

    LastUpdated = ''
    DateDesignated = ''
    UniqueID = ''
    OFSIGroupID = ''
    UNReferenceNumber = ''
    RegimeName = ''
    Names = []
    NonLatinNames = []
    IndividualEntityShip = ''
    DesignationSource = ''
    SanctionsImposed=''
    SanctionsImposedIndicators = []
    OtherInformation = ''
    UKStatementofReasons = ''
    Addresses = []
    PhoneNumbers = []
    EmailAddresses = []
    IndividualDetails = []
    EntityDetails = []

    for item in doc.getchildren():
        #item.tag=item.tag.split('}')[-1]
        if item.tag == 'LastUpdated':
            LastUpdated = item.text
        elif item.tag == 'DateDesignated':
            DateDesignated = item.text
        elif item.tag == 'UniqueID':
            UniqueID = item.text
        elif item.tag == 'OFSIGroupID':
            OFSIGroupID = item.text
        elif item.tag == 'UNReferenceNumber':
            UNReferenceNumber = item.text
        elif item.tag == 'RegimeName':
            RegimeName = item.text
        elif item.tag == 'Names':
            for child in item.getchildren():
                name = sanction_UK_name.SanctionUKName()
                for c in child.getchildren():
                    if c.tag == 'NameType':
                        name.NameType = c.text
                    elif c.tag == 'AliasStrength':
                        name.AliasStrength = c.text
                    else:
                        t = name.Name + c.text + ' '
                        name.Name = t
                Names.append(name)
        elif item.tag == 'NonLatinNames':
            for child in item.getchildren():
                for c in child.getchildren():
                    if c.text != '':
                        NonLatinNames.append(c.text)
        elif item.tag == 'IndividualEntityShip':
            IndividualEntityShip=item.text
        elif item.tag == 'DesignationSource':
            DesignationSource=item.text
        elif item.tag == 'OtherInformation':
            OtherInformation=item.text
        elif item.tag == 'UKStatementofReasons':
            UKStatementofReasons=item.text
        elif item.tag == 'SanctionsImposed':
            SanctionsImposed = item.text
        elif item.tag == 'SanctionsImposedIndicators':
            indicator = sanction_UK_indicator.SanctionUKIndicator()
            for child in item.getchildren():
                if child.tag == 'TechnicalAssistanceRelatedToAircraft':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.TechnicalAssistanceRelatedToAircraft = result
                elif child.tag == 'PreventionOfCharteringOfShipsAndAircraft':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.PreventionOfCharteringOfShipsAndAircraft = result
                elif child.tag == 'PreventionOfCharteringOfShips':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.PreventionOfCharteringOfShips = result
                elif child.tag == 'TravelBan':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.TravelBan = result
                elif child.tag == 'ProhibitionOfPortEntry':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.ProhibitionOfPortEntry = result
                elif child.tag == 'PreventionOfBusinessArrangements':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.PreventionOfBusinessArrangements = result
                elif child.tag == 'Deflag':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.Deflag = result
                elif child.tag == 'CrewServicingOfShipsAndAircraft':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.CrewServicingOfShipsAndAircraft = result
                elif child.tag == 'ClosureOfRepresentativeOffices':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.ClosureOfRepresentativeOffices = result
                elif child.tag == 'CharteringOfShips':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.CharteringOfShips = result
                elif child.tag == 'TargetedArmsEmbargo':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.TargetedArmsEmbargo = result
                elif child.tag == 'ArmsEmbargo':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.ArmsEmbargo = result
                elif child.tag == 'AssetFreeze':
                    result = False
                    if child.text == 'true':
                        result = True
                    indicator.AssetFreeze = result
            SanctionsImposedIndicators.append(indicator)
        elif item.tag == 'Addresses':
            for child in item.getchildren():
                address = sanction_UK_address.SanctionUKAddress()
                for c in child.getchildren():
                    if c.tag == 'AddressCountry':
                        address.AddressCountry = c.text
                    else:
                        t = address.Address + c.text + '; '
                        address.Address = t
                Addresses.append(address)
        elif item.tag == 'PhoneNumbers':
            for child in item.getchildren():
                if child.text != '':
                    PhoneNumbers.append(child.text)
        elif item.tag == 'EmailAddresses':
            for child in item.getchildren():
                if child.text != '':
                    EmailAddresses.append(child.text)
        elif item.tag == 'IndividualDetails':
            for child in item.getchildren():
                individual = sanction_UK_individual.SanctionUKIndividual()
                for c in child.getchildren():
                    if c.tag == 'DOBs':
                        for dob in c.getchildren():
                            individual.DOB.append(dob.text)
                    elif c.tag == 'PassportDetails':
                        for passport in c.getchildren():
                            t = ''
                            for detail in passport.getchildren():
                                t = t + detail.text + '; '
                            individual.PassportDetails.append(t)
                    elif c.tag == 'Nationalities':
                        for nationality in c.getchildren():
                            individual.Nationalities.append(nationality.text)
                    elif c.tag == 'NationalIdentifierDetails':
                        for passport in c.getchildren():
                            t = ''
                            for detail in passport.getchildren():
                                t = t + detail.text + '; '
                            individual.NationalIdentifierDetails.append(t)
                    elif c.tag == 'BirthDetails':
                        for passport in c.getchildren():
                            t = ''
                            for detail in passport.getchildren():
                                t = t + detail.text + '; '
                            individual.BirthDetails.append(t)
                    elif c.tag == 'Positions':
                        for position in c.getchildren():
                            individual.Positions.append(position.text)
                    elif c.tag == 'Genders':
                        for position in c.getchildren():
                            individual.Gender = position.text
                IndividualDetails.append(individual)
        elif item.tag == 'EntityDetails':
            for child in item.getchildren():
                entity = sanction_UK_Entity.SanctionUKEntity()
                for c in child.getchildren():
                    if c.tag == 'ParentCompanies':
                        for company in c.getchildren():
                            entity.ParentCompanies.append(company.text)
                    elif c.tag == 'BusinessRegistrationNumbers':
                        for company in c.getchildren():
                            entity.BusinessRegistrationNumbers.append(company.text)
                    elif c.tag == 'TypeOfEntities':
                        for company in c.getchildren():
                            entity.TypeOfEntities.append(company.text)
                    elif c.tag == 'Subsidiaries':
                        for company in c.getchildren():
                            entity.Subsidiaries.append(company.text)
                EntityDetails.append(entity)
    sanction = sanction_UK.SanctionUK(LastUpdated, DateDesignated, UniqueID, OFSIGroupID, UNReferenceNumber, RegimeName,
                 Names, NonLatinNames, IndividualEntityShip, DesignationSource, SanctionsImposed,
                 SanctionsImposedIndicators, OtherInformation, UKStatementofReasons, Addresses,
                 PhoneNumbers, EmailAddresses, IndividualDetails, EntityDetails, doc_id)
    sanctions.append(sanction)
    #print(UniqueID + ' added successfully')


def import_data_from_json(element):
    LastUpdated = element.LastUpdated
    DateDesignated = element.DateDesignated
    UniqueID = element.UniqueID
    OFSIGroupID = element.OFSIGroupID
    UNReferenceNumber = element.UNReferenceNumber
    RegimeName = element.RegimeName
    IndividualEntityShip = element.IndividualEntityShip
    DesignationSource = element.DesignationSource
    SanctionsImposed = element.SanctionsImposed
    OtherInformation = element.OtherInformation
    UKStatementofReasons = element.UKStatementofReasons
    Names = []
    NonLatinNames = element.NonLatinNames
    SanctionsImposedIndicators = []
    Addresses = []
    PhoneNumbers = element.PhoneNumbers
    EmailAddresses = element.EmailAddresses
    IndividualDetails = []
    EntityDetails = []

    for item in element.Names:
        name = sanction_UK_name.SanctionUKName()
        name.NameType = item['NameType']
        name.AliasStrength = item['NameType']
        name.Name = item['Name']
        Names.append(name)

    for item in element.SanctionsImposedIndicators:
        indicator = sanction_UK_indicator.SanctionUKIndicator()
        indicator.TechnicalAssistanceRelatedToAircraft = item['TechnicalAssistanceRelatedToAircraft']
        indicator.PreventionOfCharteringOfShipsAndAircraft = item['PreventionOfCharteringOfShipsAndAircraft']
        indicator.PreventionOfCharteringOfShips = item['PreventionOfCharteringOfShips']
        indicator.TravelBan = item['TravelBan']
        indicator.ProhibitionOfPortEntry = item['ProhibitionOfPortEntry']
        indicator.Deflag = item['Deflag']
        indicator.CrewServicingOfShipsAndAircraft = item['CrewServicingOfShipsAndAircraft']
        indicator.ClosureOfRepresentativeOffices = item['ClosureOfRepresentativeOffices']
        indicator.CharteringOfShips = item['CharteringOfShips']
        indicator.TargetedArmsEmbargo = item['TargetedArmsEmbargo']
        indicator.ArmsEmbargo = item['ArmsEmbargo']
        indicator.AssetFreeze = item['AssetFreeze']
        SanctionsImposedIndicators.append(indicator)

    for item in element.Addresses:
        address = sanction_UK_address.SanctionUKAddress()
        address.Address = item['Address']
        address.AddressCountry = item['AddressCountry']
        Addresses.append(address)

    for item in element.IndividualDetails:
        individual = sanction_UK_individual.SanctionUKIndividual()
        individual.BirthDetails = item['BirthDetails']
        individual.PassportDetails = item['PassportDetails']
        individual.Nationalities = item['Nationalities']
        individual.NationalIdentifierDetails = item['NationalIdentifierDetails']
        individual.Gender = item['Gender']
        individual.Positions = item['Positions']
        individual.DOB = item['DOB']
        IndividualDetails.append(individual)

    for item in element.EntityDetails:
        entity = sanction_UK_Entity.SanctionUKEntity()
        entity.BusinessRegistrationNumbers = item['BusinessRegistrationNumbers']
        entity.TypeOfEntities = item['TypeOfEntities']
        entity.Subsidiaries = item['Subsidiaries']
        entity.ParentCompanies = item['ParentCompanies']
        EntityDetails.append(entity)

    sanction = sanction_UK.SanctionUK(LastUpdated, DateDesignated, UniqueID, OFSIGroupID, UNReferenceNumber, RegimeName,
                                      Names, NonLatinNames, IndividualEntityShip, DesignationSource, SanctionsImposed,
                                      SanctionsImposedIndicators, OtherInformation, UKStatementofReasons, Addresses,
                                      PhoneNumbers, EmailAddresses, IndividualDetails, EntityDetails, element.id)
    return sanction
    # print(UniqueID + ' added successfully')