from DataModel.EU.sanction_EU_generic import SanctionEUGeneric


class SanctionEURegulationSummary(SanctionEUGeneric):

    def __init__(self, regulationType='', publicationDate='', numberTitle='', publicationUrl=''):
        super().__init__()
        self.publicationUrl = publicationUrl
        self.numberTitle = numberTitle
        self.publicationDate = publicationDate
        self.regulationType = regulationType