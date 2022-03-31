from DataModel import sanction_web

class SanctionUK:

    def __init__(self, LastUpdated='', DateDesignated='', UniqueID='', OFSIGroupID='', UNReferenceNumber='', RegimeName='',
                 Names=None, NonLatinNames=None, IndividualEntityShip='', DesignationSource='', SanctionsImposed='',
                 SanctionsImposedIndicators=None, OtherInformation='', UKStatementofReasons='', Addresses=None,
                 PhoneNumbers=None, EmailAddresses=None, IndividualDetails=None, EntityDetails=None, id = 0):
        self.id = id
        if EntityDetails is None:
            EntityDetails = []
        self.EntityDetails = EntityDetails
        self.SanctionsImposed = SanctionsImposed
        if IndividualDetails is None:
            IndividualDetails = [] #list of sanction_UK_individual
        self.IndividualDetails = IndividualDetails
        if EmailAddresses is None:
            EmailAddresses = [] #list of strings
        self.EmailAddresses = EmailAddresses
        if PhoneNumbers is None:
            PhoneNumbers = [] #list of strings
        self.PhoneNumbers = PhoneNumbers
        if Addresses is None:
            Addresses = [] #list of sanction_UK_address
        self.Addresses = Addresses
        self.UKStatementofReasons = UKStatementofReasons
        self.OtherInformation = OtherInformation
        if SanctionsImposedIndicators is None:
            SanctionsImposedIndicators = [] #list of sanction_UK_indicator
        self.SanctionsImposedIndicators = SanctionsImposedIndicators
        self.DesignationSource = DesignationSource
        self.IndividualEntityShip = IndividualEntityShip
        if NonLatinNames is None:
            NonLatinNames = [] #list of strings
        self.NonLatinNames = NonLatinNames
        if Names is None:
            Names = [] #list of sanction_UK_name
        self.Names = Names
        self.RegimeName = RegimeName
        self.UNReferenceNumber = UNReferenceNumber
        self.OFSIGroupID = OFSIGroupID
        self.UniqueID = UniqueID
        self.DateDesignated = DateDesignated
        self.LastUpdated = LastUpdated

    def webify(self):

        main_name = ''
        names = ''
        for name in self.Names:
            if name.NameType == 'Primary Name':
                main_name = name.Name
            else:
                if names:
                    names = names + ';\n' + name.Name
                else:
                    names = name.Name
        for name in self.NonLatinNames:
            if names:
                names = names + ';\n' + name
            else:
                names = name
        if not main_name:
            main_name = self.Names[0].Name

        program = ''
        if self.RegimeName:
            program = self.RegimeName
        if self.SanctionsImposed:
            if program:
                program = program + ';\n' + self.SanctionsImposed
            else:
                program = self.SanctionsImposed

        address = ''
        if len(self.Addresses) > 0:
            for a in self.Addresses:
                if a.Address:
                    address = address + a.Address + ', '
                if a.AddressCountry:
                    address = address + a.AddressCountry + ';\n'
        if len(self.EmailAddresses) > 0:
            address = address + 'Email addresses:\n'
            for a in self.EmailAddresses:
                address = address + a + ';\n'
        if len(self.PhoneNumbers) > 0:
            address = address + 'Phone numbers:\n'
            for a in self.PhoneNumbers:
                address = address + a + ';\n'

        nationality = ''
        personal_details = ''

        person = self.IndividualDetails
        for individual in person:
            for n in individual.Nationalities:
                if nationality:
                    nationality = nationality + ';\n' + n
                else:
                    nationality = n
            for n in individual.NationalIdentifierDetails:
                if nationality:
                    nationality = nationality + ';\n' + n
                else:
                    nationality = n
            for n in individual.PassportDetails:
                if nationality:
                    nationality = nationality + ';\n' + n
                else:
                    nationality = n
            if individual.Gender:
                personal_details = "Gender " + individual.Gender + ';\n'
            if len(individual.Positions) > 0:
                personal_details = personal_details + 'Positions:\n'
                for n in individual.Positions:
                    personal_details = personal_details + n + ';\n'
            if len(individual.DOB) > 0:
                personal_details = personal_details + 'Date of birth:\n'
                for n in individual.DOB:
                    personal_details = personal_details + n + ';\n'
            if len(individual.BirthDetails) > 0:
                personal_details = personal_details + 'Birth details:\n'
                for n in individual.BirthDetails:
                    personal_details = personal_details + n + ';\n'

        entities = self.EntityDetails
        for company in entities:
            if len(company.TypeOfEntities) > 0:
                personal_details = personal_details + 'Type of entities:\n'
                for n in company.TypeOfEntities:
                    personal_details = personal_details + n + ';\n'
            if len(company.BusinessRegistrationNumbers) > 0:
                personal_details = personal_details + 'Business registration numbers:\n'
                for n in company.BusinessRegistrationNumbers:
                    personal_details = personal_details + n + ';\n'
            if len(company.ParentCompanies) > 0:
                personal_details = personal_details + 'Parent companies:\n'
                for n in company.ParentCompanies:
                    personal_details = personal_details + n + ';\n'
            if len(company.Subsidiaries) > 0:
                personal_details = personal_details + 'Subsidiaries:\n'
                for n in company.Subsidiaries:
                    personal_details = personal_details + n + ';\n'

        additional_info = ''
        if self.OtherInformation:
            additional_info = self.OtherInformation
        if self.UKStatementofReasons:
            if additional_info:
                additional_info = additional_info + '.\n' + self.UKStatementofReasons
            else:
                additional_info = self.UKStatementofReasons

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='gb',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=additional_info,
                                            id=self.id)
        return sanction
