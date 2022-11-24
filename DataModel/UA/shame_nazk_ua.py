from DataModel import sanction_web

class ShameNAZKUA:

    def __init__(self, shame_id='', person_id='', company_id='', status='',
                 logo_ganba='', photo_ganba='', category='',
                 name_en='', name_ru='', name_uk='', country='', position_uk='',
                 position_en='', position_ru='',
                 company_name_ru='', company_name_uk='', company_name_en='',
                 ogrn='', ipn='', work_other_ru='', work_other_uk = '', work_other_en='',
                 linkedin='', date_bd='', birthplace_ru='', birthplace_uk='', birthplace_en='', id=0):
        self.id = id
        self.birthplace_en = birthplace_en
        self.birthplace_uk = birthplace_uk
        self.birthplace_ru = birthplace_ru
        self.date_bd = date_bd
        self.linkedin = linkedin
        self.work_other_en = work_other_en
        self.work_other_ru = work_other_ru
        self.ipn = ipn
        self.ogrn = ogrn
        self.company_name_en = company_name_en
        self.company_name_uk = company_name_uk
        self.company_name_ru = company_name_ru
        self.position_ru = position_ru
        self.position_en = position_en
        self.country = country
        self.position_uk = position_uk
        self.work_other_uk = work_other_uk
        self.name_uk = name_uk
        self.name_ru = name_ru
        self.name_en = name_en
        self.category = category
        self.photo_ganba = photo_ganba
        self.logo_ganba = logo_ganba
        self.status = status
        self.company_id = company_id
        self.person_id = person_id
        self.shame_id = shame_id
        self.search_fields = [self.name_en, self.name_uk, self.name_ru]

    def webify(self):
        main_name = self.name_en
        names = ''
        if self.name_uk:
            names = self.name_uk + ';\n'
        if self.name_ru:
            names = self.name_ru + ';\n'

        urls = ''
        if self.linkedin:
            urls = '<a href="' + self.linkedin + '">LinkedIn</a>' + ';\n'
        program = sanction_web.UA_RISK_WORDING + 'Position' + self.position_en + ';\n' + 'Company:' + self.company_name_en + \
                  ';\n' + 'Details: ' + self.work_other_en
        nationality = self.country
        address = 'Place of birth: ' + self.birthplace_en
        personal_details = ''
        if self.ipn:
            personal_details = 'IPN: ' + self.ipn + ';\n'
        if self.ogrn:
            personal_details = personal_details + 'OGRN: ' + self.ogrn + ';\n'
        if self.category:
            personal_details = personal_details + self.category

        additional_info = urls

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='xx',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=additional_info,
                                            id=self.id)
        return sanction