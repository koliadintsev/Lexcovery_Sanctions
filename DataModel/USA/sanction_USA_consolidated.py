from DataModel import sanction_web


class SanctionUSAConsolidated:

    def __init__(self, doc_id='', source='', entity_number='', doc_type='', programs='', name='', title='',
                 addresses='',
                 federal_register_notice='', start_date='', end_date='', standard_order='', license_requirement='',
                 license_policy='', call_sign='', vessel_type='', gross_tonnage='', gross_registered_tonnage='',
                 vessel_flag='', vessel_owner='', remarks='', source_list_url='', alt_names='', citizenships='',
                 dates_of_birth='', nationalities='', places_of_birth='', source_information_url='', ids=''):
        self.ids = ids
        self.source_information_url = source_information_url
        self.places_of_birth = places_of_birth
        self.nationalities = nationalities
        self.dates_of_birth = dates_of_birth
        self.citizenships = citizenships
        self.source_list_url = source_list_url
        self.remarks = remarks
        self.vessel_owner = vessel_owner
        self.vessel_flag = vessel_flag
        self.gross_registered_tonnage = gross_registered_tonnage
        self.gross_tonnage = gross_tonnage
        self.vessel_type = vessel_type
        self.call_sign = call_sign
        self.license_policy = license_policy
        self.license_requirement = license_requirement
        self.standard_order = standard_order
        self.end_date = end_date
        self.start_date = start_date
        self.federal_register_notice = federal_register_notice
        self.addresses = addresses
        self.title = title
        self.name = ''
        main_name = name.split(',')
        for n in main_name:
            if self.name:
                self.name = n + ' ' + self.name
            else:
                self.name = n
        self.programs = programs
        self.doc_type = doc_type
        self.entity_number = entity_number
        self.source = source
        self.doc_id = doc_id
        self.search_fields = [self.name]
        self.alt_names = ''
        if alt_names.find(';'):
            alt = alt_names.split(';')
            for alt_name in alt:
                if alt_name.find(','):
                    a = alt_name.split(',')
                    n = ''
                    for part in a:
                        if n:
                            n = part + ' ' + n
                        else:
                            n = part
                    self.alt_names = self.alt_names + n + '; '
                    self.search_fields.append(n)
                else:
                    self.alt_names = self.alt_names + alt_name + '; '
                    self.search_fields.append(alt_name)
        else:
            self.alt_names = alt_names
            self.search_fields.append(alt_names)

    def webify(self):
        main_name = self.name
        if self.title:
            main_name = main_name + ', ' + self.title

        names = self.alt_names.replace('; ', ';\n')

        program = ''
        if self.programs:
            program = self.programs + '\n'
        program = program + self.source + '  <a href="' + self.source_information_url + '">Source Information</a>' \
                  + '\n' + 'Number: ' + self.entity_number + '  <a href="' + self.source_list_url + '">Source List</a>' + '\n'
        if self.start_date:
            program = program + 'Start date: ' + self.start_date + '\n' + 'End date: ' + self.end_date + '\n'
        if self.federal_register_notice:
            program = program + 'Federal Notice: ' + self.federal_register_notice + '\n'
        if self.standard_order:
            program = program + self.standard_order + '\n'
        if self.license_policy or self.license_requirement:
            program = program + 'License policy: ' + self.license_policy + '\n' + 'License requirements: ' + self.license_requirement

        address = self.addresses.replace('; ', ';\n')

        nationality = ''
        if self.nationalities:
            nationality = "Nationalities: " + self.nationalities + '\n'
        if self.citizenships:
            nationality = nationality + "Citizenships: " + self.citizenships

        personal_details = ''
        if self.dates_of_birth:
            personal_details = personal_details + 'Dates of Birth: ' + self.dates_of_birth + '\n'
        if self.places_of_birth:
            personal_details = personal_details + 'Places of Birth: ' + self.places_of_birth + '\n'
        if self.ids:
            personal_details = personal_details + 'IDs: ' + self.ids

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='us',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=self.remarks,
                                            id=self.doc_id)
        return sanction
