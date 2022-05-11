import datetime

import xlrd

from DataModel import sanction_web


class SanctionAU:

    def __init__(self, number='', name='', entity='', name_type='', date_of_birth='', place_of_birth='', citizenship='',
                 address='', additional_information='', listing_information='', committees = '', control_date='', id=0):

        self.id = id
        self.control_date = control_date
        self.committees = committees
        self.listing_information = listing_information
        self.additional_information = additional_information
        self.citizenship = citizenship
        self.place_of_birth = place_of_birth
        self.date_of_birth = date_of_birth
        self.name_type = name_type
        self.entity = entity
        self.name = name
        self.number = number
        self.address = address
        self.search_fields = [self.name]


    def webify(self):
        main_name = self.name
        names = self.entity + '\n' + self.name_type
        control_date = ''
        if isinstance(self.control_date, datetime.date):
            control_date = self.control_date.strftime("%d/%m/%Y")
        else:
            control_date = self.control_date

        listing_information = ''
        if self.listing_information:
            if isinstance(self.listing_information, datetime.date):
                listing_information = self.listing_information.strftime("%d/%m/%Y")
            elif isinstance(self.listing_information, float):
                try:
                    listing_information = xlrd.xldate_as_datetime(self.listing_information, 0).date().strftime("%d/%m/%Y")
                except Exception:
                    listing_information = str(self.listing_information)
            else:
                listing_information = str(self.listing_information)
        program = listing_information + ';\n' + 'Committee: ' + self.committees + ';\n' + 'Start: ' + control_date
        nationality = self.citizenship
        address = self.address
        date_of_birth = ''
        if isinstance(self.date_of_birth, datetime.date):
            date_of_birth = self.date_of_birth.strftime("%d/%m/%Y")
        else:
            date_of_birth = self.date_of_birth
        personal_details = 'Date of Birth: ' + date_of_birth + '\n' + 'Place of Birth: ' + self.place_of_birth
        additional_info = self.additional_information

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='au',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=additional_info,
                                            id=self.id)
        return sanction
