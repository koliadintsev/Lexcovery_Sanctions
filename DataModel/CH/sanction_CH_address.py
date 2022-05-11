# XML class: address
from DataModel.CH.sanction_CH_place import SanctionCHPlace


class SanctionCHAddress:

    def __init__(self, ssid=0, place_id=0, quality='', current=True, c_o='', address_details='', p_o_box='',
                 zip_code='', remark='', place: SanctionCHPlace = None):
        self.place = place
        self.remark = remark
        self.zip_code = zip_code
        self.p_o_box = p_o_box
        self.address_details = address_details
        self.c_o = c_o
        self.current = current
        self.quality = quality
        self.place_id = place_id
        self.ssid = ssid
