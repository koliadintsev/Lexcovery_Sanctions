from DataModel.EU.sanction_EU_generic import SanctionEUGeneric
from DataModel.EU.sanction_EU_regulationSummary import SanctionEURegulationSummary


class SanctionEUName(SanctionEUGeneric):

    def __init__(self, firstName='', middleName='', lastName='', wholeName='', function='', gender='',
                 title='', nameLanguage='', strong=False, regulationLanguage='', regulationSummary = SanctionEURegulationSummary()):
        super().__init__()
        self.regulationSummary = regulationSummary
        self.regulationLanguage = regulationLanguage
        self.title = title
        self.strong = strong
        self.nameLanguage = nameLanguage
        self.gender = gender
        self.function = function
        self.wholeName = wholeName
        self.lastName = lastName
        self.middleName = middleName
        self.firstName = firstName
