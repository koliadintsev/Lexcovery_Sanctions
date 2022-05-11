# XML class: sanctions-program
class SanctionCHProgram:

    def __init__(self, ssid=0, version_date='', predecessor_version_date='', program_key='', program_name='',
                 sanctions_set='', sanction_set_ssid=0, origin=''):
        self.origin = origin
        self.sanction_set_ssid = sanction_set_ssid
        self.sanctions_set = sanctions_set
        self.program_name = program_name
        self.program_key = program_key
        self.predecessor_version_date = predecessor_version_date
        self.version_date = version_date
        self.ssid = ssid
