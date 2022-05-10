import datetime

from DataModel import sanction_web


class SanctionJP:

    def __init__(self, id=0, start_date='', number='', name_jp='', name_eng='', alias='', date_of_birth='',
                 place_of_birth='', contacts = '',
                 position='', country='', id_details='', address='', program='', remark=''):
        self.contacts = contacts
        self.remark = remark
        self.program = program
        self.address = address
        self.id_details = id_details
        self.country = country
        self.position = position
        self.place_of_birth = place_of_birth
        self.date_of_birth = date_of_birth
        self.alias = alias
        self.name_eng = name_eng
        self.name_jp = name_jp
        self.number = number
        self.start_date = start_date
        self.id = id
        self.search_fields = [self.name_jp, self.name_eng, self.alias]


    def webify(self):
        main_name = self.name_eng
        names = 'Main name (jp): ' + self.name_jp + ';\n' + 'Other names:\n' + self.alias
        start_date = ''
        if isinstance(self.start_date, datetime.date):
            start_date = self.start_date.strftime("%d/%m/%Y")
        else:
            start_date = self.start_date
        program = 'Program (jp): ' + self.program + ';\n' + 'Number: ' + self.number + ';\n' + 'Start: ' + start_date
        nationality = self.country
        address = self.address
        date_of_birth = ''
        if isinstance(self.date_of_birth, datetime.date):
            date_of_birth = self.date_of_birth.strftime("%d/%m/%Y")
        else:
            date_of_birth = self.date_of_birth
        personal_details = 'Position: ' + self.position + ';\n' + 'Birth details:\n' + date_of_birth + ';\n' + \
                           self.place_of_birth + ';\n' + 'ID:\n' + self.id_details + 'Contacts:\n' + self.contacts
        additional_info = self.remark

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='jp',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=additional_info,
                                            id=self.id)
        return sanction
