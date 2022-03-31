class SanctionUSADocument:

    def __init__(self, uid=0, idType='', idNumber='', idCountry='', issueDate='', expirationDate=''):
        self.expirationDate = expirationDate
        self.issueDate = issueDate
        self.idCountry = idCountry
        self.idNumber = idNumber
        self.idType = idType
        self.uid = uid