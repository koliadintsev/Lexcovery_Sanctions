import datetime

from DataModel import sanction_web


class SanctionUA:

    def __init__(self, act_number='', start_date=None, action='', changes='', number='', restrictions='',
                 term='', end_date=None, name_ukr='', name_orig='', name_alt='', name_latin='', date_of_birth=None,
                 citizenship='', place_of_birth='', work='', address='', address_additional='', iden_code='',
                 inn='', remarks='', responsive_body='', id=0, person = True):
        self.person = person
        self.id = id
        self.responsive_body = responsive_body
        self.inn = inn
        self.iden_code = iden_code
        self.address_additional = address_additional
        self.address = address
        self.work = work
        self.place_of_birth = place_of_birth
        self.citizenship = citizenship
        self.date_of_birth = date_of_birth
        self.name_latin = name_latin
        self.name_alt = name_alt
        self.name_orig = name_orig
        self.name_ukr = name_ukr
        self.end_date = end_date
        self.term = term
        self.restrictions = restrictions
        self.number = number
        self.changes = changes
        self.action = action
        self.start_date = start_date
        self.act_number = act_number
        self.remarks = remarks
        self.search_fields = [self.name_ukr, self.name_alt, self.name_orig, self.name_latin]

    def webify(self):
        main_name = self.name_latin
        names = ''
        if self.name_ukr:
            names = self.name_ukr + ';\n'
        if self.name_orig:
            names = self.name_orig + ';\n'
        if self.name_alt:
            names = self.name_alt + ';\n'

        start_date = ''
        end_date = ''
        date_of_birth = ''
        if isinstance(self.start_date, datetime.date):
            start_date = self.start_date.strftime("%d/%m/%Y")
        else:
            start_date = self.start_date
        if isinstance(self.end_date, datetime.date):
            end_date = self.end_date.strftime("%d/%m/%Y")
        else:
            end_date = self.end_date
        if isinstance(self.date_of_birth, datetime.date):
            date_of_birth = self.date_of_birth.strftime("%d/%m/%Y")
        else:
            date_of_birth = self.date_of_birth

        program = 'Act number: ' + self.act_number + ';\n' + 'Start: ' + start_date + ' End: ' + end_date + ';\n' + self.restrictions
        nationality = self.citizenship
        address = self.address + ';\n' + self.address_additional
        personal_details = ''
        if self.person:
            personal_details = self.work + ';\n' + date_of_birth + ';\n' + self.place_of_birth
        else:
            personal_details = self.iden_code + ';\n' + self.inn
        additional_info = self.remarks

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='ua',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=additional_info,
                                            id=self.id)
        return sanction
