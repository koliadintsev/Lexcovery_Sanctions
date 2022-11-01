from DataModel import sanction_web


class CompanyNAZKUA:

    def __init__(self, company_id='', sort_order='', status='', logo='', logo_ru='', logo_en='',
                 name='', name_en='', name_uk='', name_ru='', country='', category='', subcategory_1='',
                 subcategory_2='', subcategory_3='', ogrn='', inn='', reasoning_uk='', reasoning_en='',
                 reasoning_ru='', address_uk='', address_en='', address_ru='', sanctions_ua='', sanctions_ua_date='',
                 url_es='', url_gb='',
                 url_us='', url_ca='', url_ch='', url_au='', url_jp='', url_ua='', url_nz='', link='', link_archive='',
                 relations_person=None, relations_company=None, id=0):

        self.sanctions_ua = sanctions_ua
        self.sanctions_ua_date = sanctions_ua_date
        self.id = id
        if relations_company is None:
            relations_company = []
        if relations_person is None:
            relations_person = []
        self.relations_company = relations_company
        self.relations_person = relations_person
        self.link_archive = link_archive
        self.link = link
        self.url_nz = url_nz
        self.url_ua = url_ua
        self.url_jp = url_jp
        self.url_au = url_au
        self.url_ch = url_ch
        self.url_ca = url_ca
        self.url_us = url_us
        self.url_gb = url_gb
        self.url_es = url_es
        self.address_ru = address_ru
        self.address_en = address_en
        self.address_uk = address_uk
        self.reasoning_ru = reasoning_ru
        self.reasoning_en = reasoning_en
        self.reasoning_uk = reasoning_uk
        self.inn = inn
        self.ogrn = ogrn
        self.subcategory_3 = subcategory_3
        self.subcategory_2 = subcategory_2
        self.subcategory_1 = subcategory_1
        self.category = category
        self.country = country
        self.name_ru = name_ru
        self.name_uk = name_uk
        self.name_en = name_en
        self.name = name
        self.logo_en = logo_en
        self.logo_ru = logo_ru
        self.logo = logo
        self.status = status
        self.sort_order = sort_order
        self.company_id = company_id
        self.search_fields = [self.name_en, self.name_uk, self.name_ru]

    def webify(self):
        main_name = self.name_en
        names = ''
        if self.name_uk:
            names = self.name_uk + ';\n'
        if self.name_ru:
            names = self.name_ru + ';\n'
        if self.name:
            names = self.name + ';\n'

        start_date = self.sanctions_ua_date
        urls = ''
        if self.url_ua:
            urls = '<a href="' + self.url_ua + '">Sanctions List</a>' + ';\n'
        if self.link:
            urls = urls + '<a href="' + self.link + '">OpenSanctions</a>' + ';\n'
        if self.link_archive:
            urls = urls + '<a href="' + self.link_archive + '">Archive</a>'
        program = self.reasoning_en + ';\n' + 'Start date: ' + start_date
        nationality = self.country
        address = self.address_en
        personal_details = ''
        if self.inn:
            personal_details = 'INN: ' + self.inn + ';\n'
        if self.ogrn:
            personal_details = personal_details + 'OGRN: ' + self.ogrn + ';\n'
        if self.category:
            personal_details = personal_details + self.category + ';\n'
        if self.subcategory_1:
            personal_details = personal_details + self.subcategory_1 + ';\n'
        if self.subcategory_2:
            personal_details = personal_details + self.subcategory_2 + ';\n'
        if self.subcategory_3:
            personal_details = personal_details + self.subcategory_3

        additional_info = urls

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='ua',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=additional_info,
                                            id=self.id)
        return sanction
