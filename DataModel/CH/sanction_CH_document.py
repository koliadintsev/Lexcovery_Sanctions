# XML class: identification-document
from DataModel.CH.sanction_CH_place import SanctionCHPlace


class SanctionCHDocument:

    def __init__(self, ssid=0, document_type='', number='', issuer='', date_of_issue='', place_of_issue: SanctionCHPlace = None,
                 place_id=0, expiry_date='', remark=''):
        self.remark = remark
        self.expiry_date = expiry_date
        self.place_id = place_id
        self.place_of_issue = place_of_issue
        self.date_of_issue = date_of_issue
        self.issuer = issuer
        self.number = number
        self.document_type = document_type
        self.ssid = ssid