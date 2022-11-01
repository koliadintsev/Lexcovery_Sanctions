from DataModel import sanction_web


# "111": {"person_id"=111, "relation_name"="кум"

class RelationsPersonNAZKUA:

    def __init__(self, person_id='', relation_name='', id=0):
        self.id = id
        self.relation_name = relation_name
        self.person_id = person_id
