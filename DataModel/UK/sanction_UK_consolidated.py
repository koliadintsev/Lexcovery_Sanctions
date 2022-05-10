import datetime
from DataModel import sanction_web


class SanctionUKConsolidated:

    def __init__(self, name='', title='', name_non_latin_script='', date_of_birth='', place_of_birth='',
                 nationality='', id_details='', position='', address='', additional_info='', group_type='',
                 alias_type='', alias_quality='', regime='', listed_on='', designation_date='', last_update='',
                 group_id='', id=0):
        self.id = id
        self.group_id = group_id
        self.last_update = last_update
        self.designation_date = designation_date
        self.listed_on = listed_on
        self.regime = regime
        self.alias_quality = alias_quality
        self.alias_type = alias_type
        self.group_type = group_type
        self.additional_info = additional_info
        self.address = address
        self.position = position
        self.id_details = id_details
        self.nationality = nationality
        self.place_of_birth = place_of_birth
        self.date_of_birth = date_of_birth
        self.name_non_latin_script = name_non_latin_script
        self.title = title
        self.name = name
        self.search_fields = [self.name, self.name_non_latin_script]

    def webify(self):
        main_name = self.name
        names = self.alias_type + ' ' + self.alias_quality + '\n' + self.title + '\n' + self.name_non_latin_script
        designation_date = ''
        if isinstance(self.designation_date, datetime.date):
            designation_date = self.designation_date.strftime("%d/%m/%Y")
        else:
            designation_date = self.designation_date
        last_update = ''
        if isinstance(self.last_update, datetime.date):
            last_update = self.last_update.strftime("%d/%m/%Y")
        else:
            last_update = self.last_update
        program = self.regime + ' GroupID: ' + self.group_id + '\n' + 'Start: ' + designation_date + '; \n' + \
                  'Last updated: ' + last_update
        nationality = self.nationality
        address = self.address
        date_of_birth = ''
        if isinstance(self.date_of_birth, datetime.date):
            date_of_birth = self.date_of_birth.strftime("%d/%m/%Y")
        else:
            date_of_birth = self.date_of_birth
        personal_details = 'Position: ' + self.position + '; \n' + 'Date of Birth: ' + date_of_birth + '\n' + \
                           'Place of Birth: ' + self.place_of_birth + '\n' + 'Identification: ' + self.id_details
        additional_info = self.additional_info + '; \n' + self.group_type

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='gb',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=additional_info,
                                            id=self.id)
        return sanction
