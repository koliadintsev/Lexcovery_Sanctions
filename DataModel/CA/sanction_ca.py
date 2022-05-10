from DataModel import sanction_web


class SanctionCA:

    def __init__(self, country='', entity='', last_name='', given_name='', date_of_birth='', schedule='', item='',
                 aliases ='', title = '', id=0):
        self.title = title
        self.id = id
        self.aliases = aliases
        self.item = item
        self.schedule = schedule
        self.date_of_birth = date_of_birth
        self.given_name = given_name
        self.last_name = last_name
        self.entity = entity
        self.country = country
        name = ''
        if self.entity:
            name = self.entity
        else:
            if self.given_name:
                name = self.given_name + ' ' + self.last_name
            else:
                name = self.last_name
        self.search_fields = [name, aliases]


    def webify(self):

        name = ''
        if self.entity:
            name = self.entity
        else:
            if self.given_name:
                name = self.given_name + ' ' + self.last_name
            else:
                name = self.last_name
        main_name = name
        names = self.aliases + '\n' + self.title
        program = 'Country: ' + self.country + '\n' + 'Schedule: ' + self.schedule + ';\n' + 'Item: ' + self.item
        nationality = ''
        address = ''
        personal_details = 'Date of Birth: ' + self.date_of_birth
        additional_info = ''

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='ca',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=additional_info,
                                            id=self.id)
        return sanction

