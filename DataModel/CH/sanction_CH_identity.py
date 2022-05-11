# XML class: identity
class SanctionCHIdentity:

    def __init__(self, ssid=0, main=False, name=None, nationality=None, day_month_year=None, place_of_birth=None,
                 address=None, identification_document=None):
        self.main = main
        self.ssid = ssid
        if address is None:
            address = []
        if identification_document is None:
            identification_document = []
        if place_of_birth is None:
            place_of_birth = []
        if day_month_year is None:
            day_month_year = []
        if nationality is None:
            nationality = []
        if name is None:
            name = []
        self.identification_document = identification_document
        self.address = address
        self.place_of_birth = place_of_birth
        self.day_month_year = day_month_year
        self.nationality = nationality
        self.name = name
