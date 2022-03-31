from DataModel.EU.sanction_EU_generic import SanctionEUGeneric
from DataModel.EU.sanction_EU_regulationSummary import SanctionEURegulationSummary


class SanctionEUAddress(SanctionEUGeneric):

    def __init__(self, city='', street='', poBox='', zipCode='', region='', place='', countryIso2Code='', asAtListingTime = False,
                 countryDescription='', contactInfo=None, regulationLanguage='', regulationSummary=SanctionEURegulationSummary()):
        super().__init__()
        if contactInfo is None:
            contactInfo = [] #list of contact info
        self.contactInfo = contactInfo
        self.asAtListingTime = asAtListingTime
        self.zipCode = zipCode
        self.poBox = poBox
        self.city = city
        self.street = street
        self.regulationSummary = regulationSummary
        self.regulationLanguage = regulationLanguage
        self.countryDescription = countryDescription
        self.countryIso2Code = countryIso2Code
        self.place = place
        self.region = region

