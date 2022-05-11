from Search import elasticsearch_handler
from DataImport import translit, import_sanctions_ua, import_sanctions_uk, import_sanctions_jp, import_sanctions_ca, \
    import_sanctions_usa_consolidated, import_sanctions_ch
import asyncio


def main():
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

    r1, d1 = import_sanctions_ch.import_data_from_xml()
    print('a')
    return r1, d1

main()
