from DataModel import sanction_web


class SanctionUKCons:

    def __init__(self, name='', shortname='', code=0, address='', kved='', boss='', stan=''):
        self.stan = stan
        self.boss = boss
        self.kved = kved
        self.address = address
        self.code = code
        self.shortname = shortname
        self.name = name
        self.beneficiaries = []
        self.founders = []

    def webify(self):
        return
