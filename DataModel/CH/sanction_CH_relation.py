# XML class: relation
from DataModel.CH.sanction_CH import SanctionCH


class SanctionCHRelation:

    def __init__(self, ssid=0, target_id=0, relation_type='', remark='', target: SanctionCH = None):
        self.target = target
        self.remark = remark
        self.relation_type = relation_type
        self.target_id = target_id
        self.ssid = ssid