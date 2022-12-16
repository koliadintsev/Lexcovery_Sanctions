from DataModel import sanction_web


class IndividualNAZKUA:

    UA_RISK_WORDING = "THIS PERSON OR COMPANY IS NOT SANCTIONED\nHowever, this person or company " \
                      "is in close connection with sanctioned one\n and may be ' \
                    'sanctioned at any time\n"

    def __init__(self, person_id='', name_en='', name_ru='', name_uk='', country='', position_uk='',
                 position_en='', position_ru='', reasoning_uk='', reasoning_en='',
                 reasoning_ru='', category='', subcategory_1='',
                 subcategory_2='', subcategory_3='', sanctions_ua='', sanctions_ua_date='', url_es='', url_gb='',
                 url_us='', url_ca='', url_ch='', url_au='', url_jp='', url_ua='', url_nz='',
                 photo_name='', status='', top_50='', synchron='', date_bd='', date_dead='', itn='',
                 city_bd_uk='', city_bd_ru='', city_bd_en='',
                 link='', link_archive='',
                 relations_person=None, relations_company=None, id=0):
        self.sanctions_ua_date = sanctions_ua_date
        self.sanctions_ua = sanctions_ua
        self.id = id
        if relations_company is None:
            relations_company = []
        if relations_person is None:
            relations_person = []
        self.relations_company = relations_company
        self.relations_person = relations_person
        self.link_archive = link_archive
        self.link = link
        self.city_bd_en = city_bd_en
        self.city_bd_ru = city_bd_ru
        self.city_bd_uk = city_bd_uk
        self.itn = itn
        self.date_dead = date_dead
        self.date_bd = date_bd
        self.synchron = synchron
        self.top_50 = top_50
        self.status = status
        self.photo_name = photo_name
        self.url_nz = url_nz
        self.url_ua = url_ua
        self.url_jp = url_jp
        self.url_au = url_au
        self.url_ch = url_ch
        self.url_ca = url_ca
        self.url_us = url_us
        self.url_gb = url_gb
        self.url_es = url_es
        self.subcategory_3 = subcategory_3
        self.subcategory_2 = subcategory_2
        self.subcategory_1 = subcategory_1
        self.category = category
        self.reasoning_ru = reasoning_ru
        self.reasoning_en = reasoning_en
        self.reasoning_uk = reasoning_uk
        self.position_ru = position_ru
        self.position_en = position_en
        self.position_uk = position_uk
        self.country = country
        self.name_uk = name_uk
        self.name_ru = name_ru
        self.name_en = name_en
        self.person_id = person_id
        self.search_fields = [self.name_en, self.name_uk, self.name_ru]

    def webify(self):
        country = 'ua'
        main_name = self.name_en
        names = ''
        if self.name_uk:
            names = self.name_uk + ';\n'
        if self.name_ru:
            names = self.name_ru + ';\n'

        start_date = self.sanctions_ua_date
        urls = ''
        if self.url_ua:
            urls = '<a href="' + self.url_ua + '">Sanctions List</a>' + '\n'
        if self.link:
            urls = urls + '<a href="' + self.link + '">OpenSanctions</a>' + '\n'
        if self.link_archive:
            urls = urls + '<a href="' + self.link_archive + '">Archive</a>' + '\n'
        program = ''
        if self.status == '2':
            program = sanction_web.UA_RISK_WORDING
            country = 'xx'
        program = program + self.position_en + ';\n' + self.reasoning_en + ';\n'
        if start_date:
            program = program + 'Start date: ' + start_date
        nationality = self.country
        address = 'City of birth: ' + self.city_bd_en
        personal_details = ''
        if self.itn:
            personal_details = 'ITN: ' + self.itn + ';\n'
        if self.date_bd:
            personal_details = personal_details + 'Date of birth: ' + self.date_bd + ';\n'
        if self.date_dead:
            personal_details = personal_details + 'Date of death: ' + self.date_dead + ';\n'
        else:
            personal_details = personal_details + 'Date of death: ' + 'Not yet' + ';\n'
        if self.category:
            personal_details = personal_details + self.category + ';\n'
        if self.subcategory_1:
            personal_details = personal_details + self.subcategory_1 + ';\n'
        if self.subcategory_2:
            personal_details = personal_details + self.subcategory_2 + ';\n'
        if self.subcategory_3:
            personal_details = personal_details + self.subcategory_3 + ';\n'

        additional_info = urls

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by=country,
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=additional_info,
                                            id=self.id)
        return sanction
