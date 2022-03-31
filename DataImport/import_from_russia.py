# -*- coding: utf-8 -*-
from lxml import etree
import copy
from Lexcovery_Sanctions.settings import STATIC_ROOT
import requests
import json

API_URL = 'https://egrul.itsoft.ru/'
FILENAME = STATIC_ROOT + "/Crimea_ogrn.txt"
RUSSIAN_COMPANIES = STATIC_ROOT + "/russian_edr_full.xml"
companies = []
founders = etree


def find_founders_from_crimea():
    global founders
    root = founders.Element('root')
    #parser = etree.XMLParser(recover=True, huge_tree=True)

    with open(FILENAME, 'r') as ft:  # Write in XML file as utf-8
        ogrn_list = ft.readlines()

    #ogrn = str.replace(ogrn_list[0], '\n', '')
    #root.append(get_single_case_xml(ogrn))

    for item in ogrn_list:
        ogrn = str.replace(item, '\n', '')
        root.append(get_single_case_xml(ogrn))

    print('import finished')

    xml_data = etree.tounicode(root)  # binary string
    with open(STATIC_ROOT + "/crimean_bastards.xml", 'w') as f:  # Write in XML file as utf-8
        f.write(xml_data)

    print('russians found and recorded')


def get_single_case_xml(ogrn):
    request_params = {'Accept - encoding': "gzip\r\n"}
    response = requests.get(API_URL+'/'+ogrn+'.xml', params=request_params)
    if response.ok:
        doc = etree.fromstring(response.content)
        d = copy.deepcopy(doc)
        return d
    else:
        return


