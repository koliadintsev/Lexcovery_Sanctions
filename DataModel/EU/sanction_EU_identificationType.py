from DataModel.EU.sanction_EU_generic import SanctionEUGeneric
from DataModel.EU.sanction_EU_regulationSummary import SanctionEURegulationSummary


class SanctionEUIdentificationType(SanctionEUGeneric):

    def __init__(self, diplomatic=False, knownExpired=False, knownFalse=False, reportedLost=False, revokedByIssuer=False,
                 issueDate='', issuedBy ='', latinNumber = '', nameOnDocument = '', number = '', validFrom = '', validTo = '',
                 countryIso2Code='', region = '', identificationTypeCode = '', identificationTypeDescription = '',
                 countryDescription='', regulationLanguage='', regulationSummary=SanctionEURegulationSummary()):
        super().__init__()
        self.regulationSummary = regulationSummary
        self.regulationLanguage = regulationLanguage
        self.countryDescription = countryDescription
        self.identificationTypeDescription = identificationTypeDescription
        self.identificationTypeCode = identificationTypeCode
        self.region = region
        self.countryIso2Code = countryIso2Code
        self.validTo = validTo
        self.validFrom = validFrom
        self.number = number
        self.nameOnDocument = nameOnDocument
        self.latinNumber = latinNumber
        self.issuedBy = issuedBy
        self.issueDate = issueDate
        self.revokedByIssuer = revokedByIssuer
        self.reportedLost = reportedLost
        self.knownFalse = knownFalse
        self.knownExpired = knownExpired
        self.diplomatic = diplomatic
