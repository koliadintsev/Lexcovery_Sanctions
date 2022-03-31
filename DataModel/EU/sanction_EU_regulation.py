from DataModel.EU.sanction_EU_generic import SanctionEUGeneric
from DataModel.EU.sanction_EU_regulationSummary import SanctionEURegulationSummary

class SanctionEURegulation(SanctionEUGeneric):

    def __init__(self, publicationUrl='', corrigendum=SanctionEURegulationSummary(), regulationType='',
                 organisationType='', publicationDate='', entryIntoForceDate='', numberTitle='', programme=''):
        super().__init__()
        self.programme = programme
        self.numberTitle = numberTitle
        self.entryIntoForceDate = entryIntoForceDate
        self.publicationDate = publicationDate
        self.organisationType = organisationType
        self.regulationType = regulationType
        self.corrigendum = corrigendum
        self.publicationUrl = publicationUrl