UA_RISK_WORDING = "THIS PERSON OR COMPANY IS NOT SANCTIONED\nHowever, this person or company " \
                         "is in close connection with sanctioned one\n and may be  " \
                         "sanctioned at any time\n"

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

