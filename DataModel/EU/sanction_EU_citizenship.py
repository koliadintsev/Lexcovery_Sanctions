from DataModel.EU.sanction_EU_generic import SanctionEUGeneric
from DataModel.EU.sanction_EU_regulationSummary import SanctionEURegulationSummary


class SanctionEUCitizenship(SanctionEUGeneric):

    def __init__(self, acquisitionDate='', disenfranchisementDate='', region='', countryIso2Code='',
                 countryDescription='', regulationLanguage='', regulationSummary = SanctionEURegulationSummary()):
        super().__init__()
        self.regulationSummary = regulationSummary
        self.regulationLanguage = regulationLanguage
        self.countryDescription = countryDescription
        self.countryIso2Code = countryIso2Code
        self.region = region
        self.disenfranchisementDate = disenfranchisementDate
        self.acquisitionDate = acquisitionDate
