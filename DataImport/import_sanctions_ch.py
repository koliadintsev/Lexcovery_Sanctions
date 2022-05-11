import copy
import datetime
import os

from lxml import etree
from DataModel.CH import sanction_CH, sanction_CH_place, sanction_CH_program
from DataModel.CH.sanction_CH import SanctionCH
from DataModel.CH.sanction_CH_address import SanctionCHAddress
from DataModel.CH.sanction_CH_date import SanctionCHDate
from DataModel.CH.sanction_CH_document import SanctionCHDocument
from DataModel.CH.sanction_CH_generic_attribute import SanctionCHGenericAttribute
from DataModel.CH.sanction_CH_identity import SanctionCHIdentity
from DataModel.CH.sanction_CH_name import SanctionCHName
from DataModel.CH.sanction_CH_name_part import SanctionCHNamePart
from DataModel.CH.sanction_CH_place import SanctionCHPlace
from DataModel.CH.sanction_CH_place_of_birth import SanctionCHPlaceOfBirth
from DataModel.CH.sanction_CH_program import SanctionCHProgram
from DataModel.CH.sanction_CH_relation import SanctionCHRelation
from Lexcovery_Sanctions.settings import STATIC_ROOT
from Lexcovery_Sanctions import settings
import requests
from dateutil.parser import parse
import aiohttp
import asyncio

SANCTIONS_LIST = os.path.join(settings.BASE_DIR,  'static') + "/Sanctions/CH/consolidated-list.xml"
XML_URL = "https://www.sesam.search.admin.ch/sesam-search-web/pages/downloadXmlGesamtliste.xhtml?lang=en&action=downloadXmlGesamtlisteAction"
sanctions = []
programs = []
places = []

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
    file = etree.fromstring(xml_text, parser=parser)
    await asyncio.gather(*[import_from_element_async(element) for element in file.getchildren()])
    for element in file.getchildren():
        if element.tag == "swiss-sanctions-list":
            text = element.get('date')
            date = parse(text).date()
            last_update = date.strftime("%d/%m/%Y")
            break
    await asyncio.gather(*[reveal_id_in_sanction_async(sanction) for sanction in sanctions])

    return sanctions, last_update


async def import_data_from_xml():
    global sanctions
    parser = etree.XMLParser(recover=True, huge_tree=True)
    last_update = ''

    tree = etree.parse(SANCTIONS_LIST, parser)
    file = tree.getroot()
    await asyncio.gather(*[import_from_element_async(element) for element in file.getchildren()])
    for element in file.getchildren():
        if element.tag == "swiss-sanctions-list":
            text = element.get('date')
            date = parse(text).date()
            last_update = date.strftime("%d/%m/%Y")
            break
    await asyncio.gather(*[reveal_id_in_sanction_async(sanction) for sanction in sanctions])

    return sanctions, last_update


async def import_from_element_async(element):
    if element.tag == "sanctions-program":
        import_program_from_element(element)
        element.clear()
    elif element.tag == "target":
        import_target_from_element(element)
        element.clear()
    elif element.tag == "place":
        import_place_from_element(element)
        element.clear()


def import_program_from_element(element):
    global programs

    origin = ''
    sanction_set_ssid = 0
    sanctions_set = ''
    program_name = ''
    program_key = ''
    predecessor_version_date_text = element.get('predecessor-version-date')
    predecessor_version_date = parse(predecessor_version_date_text).date().strftime("%d/%m/%Y")
    version_date_text = element.get('version-date')
    version_date = parse(version_date_text).date().strftime("%d/%m/%Y")
    ssid = int(element.get('ssid'))

    for item in element.getchildren():
        if item.tag == 'program-key':
            lang = item.get('lang')
            if lang == 'eng':
                program_key = item.text
        elif item.tag == 'program-name':
            lang = item.get('lang')
            if lang == 'eng':
                program_name = item.text
        elif item.tag == 'sanctions-set':
            lang = item.get('lang')
            if lang == 'eng':
                sanctions_set = item.text
                sanction_set_ssid = int(item.get('ssid'))
        elif item.tag == 'origin':
            origin = item.text
    program = sanction_CH_program.SanctionCHProgram(ssid=ssid, version_date=version_date, predecessor_version_date=predecessor_version_date,
                                                    program_key=program_key, program_name=program_name, sanctions_set=sanctions_set,
                                                    sanction_set_ssid=sanction_set_ssid, origin=origin)
    programs.append(program)


def import_target_from_element(element):
    global sanctions

    generic_attribute = []
    foreign_identifier = ''
    sanctions_set_id = int(element.get('sanctions-set-id'))
    ssid = int(element.get('ssid'))
    justification = []
    relation = []
    other_information = []
    identity = []
    sex = ''
    object_type = ''

    for item in element.getchildren():
        if item.tag == 'foreign-identifier':
            foreign_identifier = item.text
        elif item.tag == 'generic-attribute':
            attr_ssid = int(item.get('ssid'))
            attr_name = item.get('name')
            attr_value = item.text
            attribute = SanctionCHGenericAttribute(attr_ssid, attr_name, attr_value)
            generic_attribute.append(attribute)
        elif item.tag == 'individual' or item.tag == 'entity' or item.tag == 'object':
            if item.tag == 'individual':
                sex = item.get('sex')
            elif item.tag == 'object':
                object_type = item.get('object-type')
            for doc in item.getchildren():
                if doc.tag == 'justification':
                    justification.append(doc.text)
                elif doc.tag == 'relation':
                    remark = ''
                    relation_type = doc.get('relation-type')
                    target_id = int(doc.get('target-id'))
                    rel_ssid = int(doc.get('ssid'))
                    for child in doc.getchildren():
                        if child.tag == 'remark':
                            remark = child.text
                    rel = SanctionCHRelation(ssid=rel_ssid, target_id=target_id, relation_type=relation_type, remark=remark, target = None)
                    relation.append(rel)
                elif doc.tag == 'other-information':
                    other_information.append(doc.text)
                elif doc.tag == 'identity':
                    iden = import_identity_from_element(doc)
                    identity.append(iden)

    sanction = SanctionCH(ssid=ssid, sanctions_set_id=sanctions_set_id, foreign_identifier=foreign_identifier,
                          generic_attribute=generic_attribute, modification=None, sex=sex, object_type=object_type,
                          identity=identity, justification=justification, relation=relation,
                          other_information=other_information, sanction_set=None)
    sanctions.append(sanction)


def import_place_from_element(element):
    area_variant = []
    location_variant = []
    country = ''
    area = ''
    location = ''
    ssid = int(element.get('ssid'))

    for item in element.getchildren():
        if item.tag == 'location':
            location = item.text
        elif item.tag == 'location-variant':
            location_variant.append(item.text)
        elif item.tag == 'area':
            area = item.text
        elif item.tag == 'area-variant':
            area_variant.append(item.text)
        elif item.tag == 'country':
            country = item.text

    place = SanctionCHPlace(ssid=ssid, location=location, location_variant=location_variant, area=area,
                            area_variant=area_variant, country=country)
    places.append(place)


def import_identity_from_element(element):
    identification_document = []
    address = []
    place_of_birth = []
    day_month_year = []
    nationality = []
    name = []
    main = False
    if element.get('main') == 'true':
        main = True
    ssid = int(element.get('ssid'))

    for item in element.getchildren():
        if item.tag == 'day-month-year':
            date_quality = item.get('quality')
            calendar = item.get('calendar')
            year = item.get('year')
            month = item.get('month')
            day = item.get('day')
            date_ssid = item.get('ssid')
            ch_date = SanctionCHDate(ssid=date_ssid, day=day, month=month, year=year, calendar=calendar, quality=date_quality)
            day_month_year.append(ch_date)
        elif item.tag == 'place-of-birth':
            place_id = int(item.get('place-id'))
            place_quality = item.get('quality')
            place_ssid = int(item.get('ssid'))
            place = SanctionCHPlaceOfBirth(ssid=place_ssid, place_id=place_id, quality=place_quality, place = None)
            place_of_birth.append(place)
        elif item.tag == 'nationality':
            for child in item.getchildren():
                if child.tag == 'country':
                    nationality.append(child.text)
        elif item.tag == 'identification-document':
            remark = ''
            expiry_date = ''
            place_id = 0
            date_of_issue = ''
            issuer = ''
            number = ''
            document_type = item.get('document-type')
            document_ssid = int(item.get('ssid'))
            for child in item.getchildren():
                if child.tag == 'number':
                    number = child.text
                elif child.tag == 'issuer':
                    issuer = child.text
                elif child.tag == 'date-of-issue':
                    date_of_issue = parse(child.text).date().strftime("%d/%m/%Y")
                elif child.tag == 'expiry-date':
                    expiry_date = parse(child.text).date().strftime("%d/%m/%Y")
                elif child.tag == 'place-of-issue':
                    place_id = int(child.get('place-id'))
            document = SanctionCHDocument(ssid=document_ssid, document_type=document_type, number=number, issuer=issuer,
                                          date_of_issue=date_of_issue, place_of_issue = None, place_id=place_id, expiry_date=expiry_date, remark=remark)
            identification_document.append(document)
        elif item.tag == 'name':
            lang = item.get('lang')
            name_quality = item.get('quality')
            name_type = item.get('name-type')
            name_ssid = int(item.get('ssid'))
            name_part = []
            for child in item.getchildren():
                if child.tag == 'name-part':
                    spelling_variant = []
                    name_part_type = child.get('name-part-type')
                    order = child.get('order')
                    value = ''
                    for c in child.getchildren():
                        if c.tag == 'value':
                            value = c.text
                        elif c.tag == 'spelling-variant':
                            spelling_variant.append(c.text)
                    part = SanctionCHNamePart(value=value, spelling_variant=spelling_variant, order=order, name_part_type=name_part_type)
                    name_part.append(part)
            n = SanctionCHName(ssid=name_ssid, name_type=name_type, quality=name_quality, lang=lang, name_part=name_part)
            name.append(n)
        elif item.tag == 'address':
            remark = ''
            zip_code = ''
            p_o_box = ''
            address_details = ''
            c_o = ''
            current = True
            if item.get('current') == 'false':
                current = False
            address_quality = item.get('quality')
            place_id = int(item.get('place-id'))
            address_ssid = int(item.get('ssid'))
            for child in item.getchildren():
                if child.tag == 'remark':
                    remark = child.text
                elif child.tag == 'address-details':
                    address_details = child.text
                elif child.tag == 'c-o':
                    c_o = child.text
                elif child.tag == 'p-o-box':
                    p_o_box = child.text
                elif child.tag == 'zip-code':
                    zip_code = child.text
            addr = SanctionCHAddress(ssid=address_ssid, place_id=place_id, quality=address_quality, current=current, c_o=c_o, address_details=address_details, p_o_box=p_o_box,
                 zip_code=zip_code, remark=remark, place = None)
            address.append(addr)

    identity = SanctionCHIdentity(ssid=ssid, main=main, name=name, nationality=nationality, day_month_year=day_month_year, place_of_birth=place_of_birth,
                 address=address, identification_document=identification_document)
    return identity


async def reveal_id_in_sanction_async(sanction: SanctionCH):
    reveal_id_in_sanction(sanction)


def reveal_id_in_sanction(sanction: SanctionCH):
    for rel in sanction.relation:
        for s in sanctions:
            if rel.target_id == s.ssid:
                rel.target = s
    for program in programs:
        if program.sanction_set_ssid == sanction.sanctions_set_id:
            sanction.sanction_set = program
    for place in places:
        for identity in sanction.identity:
            for p in identity.place_of_birth:
                if p.place_id == place.ssid:
                    p.place = place
            for doc in identity.identification_document:
                if doc.place_id == place.ssid:
                    doc.place_of_issue = place
            for address in identity.address:
                if address.place_id == place.ssid:
                    address.place = place


def import_data_from_json(element):

    object_type = element.object_type
    sex = element.sex
    foreign_identifier = element.foreign_identifier
    sanctions_set_id = element.sanctions_set_id
    ssid = element.ssid
    generic_attribute = []
    modification = []
    other_information = []
    relation = []
    justification = []
    identity = []
    search_fields = []

    sanction_set = SanctionCHProgram()
    set = element.sanctions_set
    sanction_set.ssid = set['ssid']
    sanction_set.origin = set['origin']
    sanction_set.sanction_set_ssid = set['sanction_set_ssid']
    sanction_set.sanctions_set = set['sanctions_set']
    sanction_set.program_name = set['program_name']
    sanction_set.program_key = set['program_key']
    sanction_set.predecessor_version_date = set['predecessor_version_date']
    sanction_set.version_date = set['version_date']

    for item in element.other_information:
        other_information.append(item)
    for item in element.justification:
        justification.append(item)

    for item in element.relation:
        rel = SanctionCHRelation()
        rel.target = SanctionCH()
        target = item['target']
        for name in target['search_fields']:
            rel.target.search_fields.append(name)
        rel.remark = item['remark']
        rel.relation_type = item['relation_type']
        rel.target_id = item['target_id']
        rel.ssid = item['ssid']
        relation.append(rel)

    for item in element.identity:
        iden = SanctionCHIdentity()
        for addr in item['address']:
            a = SanctionCHAddress()
            a.place = SanctionCHPlace()
            place = addr['place']
            a.place.ssid = place['ssid']
            a.place.area = place['ssid']
            a.place.location = place['ssid']
            a.place.country = place['ssid']

            a.remark = addr['remark']
            a.zip_code = addr['zip_code']
            a.p_o_box = addr['p_o_box']
            a.address_details = addr['address_details']
            a.c_o = addr['c_o']
            a.current = addr['current']
            a.quality = addr['quality']
            a.place_id = addr['place_id']
            a.ssid = addr['ssid']
            iden.address.append(a)
        for nation in item['nationality']:
            iden.nationality.append(nation)
        iden.main = item['main']
        identity.append(iden)

    for name in element.search_fields:
        search_fields.append(name)

    sanction = SanctionCH(ssid=ssid, sanctions_set_id=sanctions_set_id, foreign_identifier=foreign_identifier,
                 generic_attribute=generic_attribute, modification=modification, sex=sex, object_type=object_type, identity=identity, justification=justification,
                 relation=relation, other_information=other_information, sanction_set=sanction_set)
    sanction.search_fields = search_fields

    return sanction

