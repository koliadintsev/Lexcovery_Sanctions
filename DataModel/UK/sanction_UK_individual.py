class SanctionUKIndividual:

    def __init__(self, DOB=None, PassportDetails=None, Nationalities=None, BirthDetails=None,
                 Positions=None, NationalIdentifierDetails=None, Gender=''):
        if BirthDetails is None:
            BirthDetails = [] #list of strings
        if PassportDetails is None:
            PassportDetails = [] #list of strings
        self.PassportDetails = PassportDetails
        if Nationalities is None:
            Nationalities = [] #list of strings
        self.Nationalities = Nationalities
        if NationalIdentifierDetails is None:
            NationalIdentifierDetails = [] #list of strings
        self.NationalIdentifierDetails = NationalIdentifierDetails
        self.Gender = Gender
        if Positions is None:
            Positions = [] #list of strings
        self.Positions = Positions
        self.BirthDetails = BirthDetails
        if DOB is None:
            DOB = [] #list of strings
        self.DOB = DOB
