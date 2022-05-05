import datetime

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


    def webify(self):
        main_name = self.name
        names = self.entity + '\n' + self.name_type
        program = self.listing_information + ';\n' + 'Committee: ' + self.committees + ';\n' + 'Start: ' + self.control_date
        nationality = self.citizenship
        address = self.address
        personal_details = 'Date of Birth: ' + self.date_of_birth + '\n' + 'Place of Birth: ' + self.place_of_birth
        additional_info = self.additional_information

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='au',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=additional_info,
                                            id=self.id)
        return sanction
