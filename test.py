import os
import re

import aiohttp

from Search import elasticsearch_handler, bulk_sanctions_search, bulk_companies_search, opencorporates_handler
from DataImport import translit, import_sanctions_ua, import_sanctions_uk, import_sanctions_jp, import_sanctions_ca, \
    import_sanctions_usa_consolidated, import_sanctions_ch, bg_checks_import
import asyncio


async def main():
    # print(translit.is_latin('hui'))
    # print(translit.is_latin('хуй'))
    # print(translit.is_latin('حاجی خيرالله و حاجی ستار صرافی'))

    # print(translit.is_cyrillic('hui'))
    # print(translit.is_cyrillic('хуй'))
    # print(translit.is_cyrillic('حاجی خيرالله و حاجی ستار صرافی'))

    # print(translit.to_latin('Федеральна державна бюджетна установа науки "Федеральний дослідний центр "Інститут біології південних морів ім. О.О.Ковалевського РАН"', 'ua'))
    # print(translit.to_latin('Федеральное государственное бюджетное учреждение науки "Федеральный исследовательский центр "Институт биологии южных морей им. А.О. Ковалевского РАН"', 'ru'))

    # r1, d1 = import_sanctions_ua.import_data_from_xls()
    # r = import_sanctions_uk.find_link_xml()

    # r = import_sanctions_jp.find_link_xls(None)
    # r1, d1 = import_sanctions_jp.import_data_from_xls()


    # r1, d1 = import_sanctions_ca.import_data_from_xml()

    # r1, d1 = import_sanctions_usa_consolidated.import_data_from_tsv()

    # r1, d1 = import_sanctions_ch.import_data_from_xml()
    # os.environ['AIOHTTP_NO_EXTENSIONS'] = '1'
    #print(os.environ.get('AIOHTTP_NO_EXTENSIONS'))
    #await elasticsearch_handler.create_index()
    #await bulk_sanctions_search.search_entities()

    # await elasticsearch_handler.import_ua_companies()
    # await bulk_companies_search.search_entities()
    # await bulk_companies_search.search_founders()

    #print(translit.to_cyrillic('LLC "DIESA"', 'ua'))

    async with aiohttp.ClientSession() as session:
        r1 = await opensanctions_handler.find_officer_count_by_name(session, 'Andrea Vallabh')
        #r1, d1 = await import_sanctions_jp.import_data_from_web(session)
    #bg_checks_import.parse_checks()


    print('done')
    return


asyncio.run(main())
