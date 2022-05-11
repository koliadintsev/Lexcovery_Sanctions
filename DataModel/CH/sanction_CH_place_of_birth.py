# XML class: place-of-birth
from DataModel.CH.sanction_CH_place import SanctionCHPlace


class SanctionCHPlaceOfBirth:

    def __init__(self, ssid=0, place_id='', quality='', place: SanctionCHPlace = None):
        self.place = place
        self.place_id = place_id
        self.quality = quality
        self.ssid = ssid