class SanctionWeb:

    def __init__(self, main_name = '', names = '', sanctioned_by = '', program = '', nationality = '', address = '',
                 personal_details = '', additional_info = '', id = 0):
        self.sanctioned_by = sanctioned_by
        self.names = names
        self.id = id
        self.additional_info = additional_info
        self.personal_details = personal_details
        self.address = address
        self.nationality = nationality
        self.program = program
        self.main_name = main_name

