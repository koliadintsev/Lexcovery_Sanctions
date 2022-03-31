from DataModel.EU.sanction_EU_generic import SanctionEUGeneric
from DataModel.EU.sanction_EU_regulationSummary import SanctionEURegulationSummary


class SanctionEUBirthdate(SanctionEUGeneric):

    def __init__(self, circa=False, calendarType='', city='', zipCode='', birthdate='', dayOfMonth='', monthOfYear='',
                 year='', yearRangeFrom='', yearRangeTo='', region='', place='', countryIso2Code='',
                 countryDescription='', regulationLanguage='', regulationSummary=SanctionEURegulationSummary()):
        super().__init__()
        self.regulationSummary = regulationSummary
        self.regulationLanguage = regulationLanguage
        self.countryDescription = countryDescription
        self.countryIso2Code = countryIso2Code
        self.place = place
        self.region = region
        self.yearRangeTo = yearRangeTo
        self.yearRangeFrom = yearRangeFrom
        self.year = year
        self.monthOfYear = monthOfYear
        self.dayOfMonth = dayOfMonth
        self.birthdate = birthdate
        self.zipCode = zipCode
        self.city = city
        self.calendarType = calendarType
        self.circa = circa





