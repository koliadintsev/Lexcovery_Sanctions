from DataModel import sanction_web


class SanctionUSA:

    def __init__(self, uid=0, firstName='', lastName='', title='', sdnType='', remarks='', programList=None,
                 idList=None, akaList=None, addressList=None, nationalityList=None, citizenshipList=None,
                 dateOfBirthList=None, placeOfBirthList=None, vesselInfo=None, id=0):
        self.id = id
        if vesselInfo is None:
            vesselInfo = []
        self.vesselInfo = vesselInfo  # list of SanctionUSAVessel
        if placeOfBirthList is None:
            placeOfBirthList = []
        self.placeOfBirthList = placeOfBirthList  # list of SanctionUSAPlaceOfBirth
        if dateOfBirthList is None:
            dateOfBirthList = []
        self.dateOfBirthList = dateOfBirthList  # list of SanctionUSADateOfBirth
        if citizenshipList is None:
            citizenshipList = []
        self.citizenshipList = citizenshipList  # list of SanctionUSANationality
        if nationalityList is None:
            nationalityList = []
        self.nationalityList = nationalityList  # list of SanctionUSANationality
        if addressList is None:
            addressList = []
        self.addressList = addressList  # list of SanctionUSAAddress
        if akaList is None:
            akaList = []
        self.akaList = akaList  # list of SanctionUSAAka
        if idList is None:
            idList = []
        if programList is None:
            programList = []
        self.idList = idList  # list of SanctionUSADocument
        self.programList = programList  # list of strings
        self.remarks = remarks
        self.sdnType = sdnType
        self.title = title
        self.lastName = lastName
        self.firstName = firstName
        self.uid = uid
        name = ''
        if not firstName:
            name = lastName
        else:
            name = firstName + ' ' + lastName
        self.wholeName = name
        self.search_fields = [self.wholeName]
        for n in self.akaList:
            self.search_fields.append(n.wholeName)

    def webify(self):

        main_name = self.firstName + ' ' + self.lastName
        if self.title:
            main_name = main_name + ', ' + self.title

        names = ''
        for n in self.akaList:
            if names:
                names = names + ';\n' + n.wholeName
            else:
                names = n.wholeName

        program = ''
        for p in self.programList:
            if program:
                program = program + ';\n' + p
            else:
                program = p

        address = ''
        for a in self.addressList:
            if a.address1:
                address = address + a.address1 + ', '
            if a.address2:
                address = address + a.address2 + ', '
            if a.address3:
                address = address + a.address3 + ', '
            if a.city:
                address = address + a.city + ', '
            if a.stateOrProvince:
                address = address + a.stateOrProvince + ', '
            if a.postalCode:
                address = address + a.postalCode + ', '
            if a.country:
                address = address + a.country + ';\n'

        nationality = ''
        if len(self.nationalityList) > 1:
            for n in self.nationalityList:
                if n.mainEntry:
                    nationality = n.country + ' - main nationality.\nAdditional nationalities:\n'
            for n in self.nationalityList:
                if not n.mainEntry:
                    nationality = nationality + n.country + ';\n'
        else:
            for n in self.nationalityList:
                nationality = n.country + ';\n'
        if len(self.citizenshipList) > 1 or nationality:
            for n in self.citizenshipList:
                if n.mainEntry:
                    nationality = nationality + n.country + ' - main nationality.\n'
            for n in self.citizenshipList:
                if not n.mainEntry:
                    nationality = nationality + n.country + ';\n'
        else:
            for n in self.citizenshipList:
                nationality = nationality + n.country + ';\n'
        if len(self.idList) > 0:
            for doc in self.idList:
                doc_text = ''
                if doc.idType:
                    doc_text = doc_text + doc.idType + ', '
                if doc.idNumber:
                    doc_text = doc_text + doc.idNumber + ', '
                if doc.idCountry:
                    doc_text = doc_text + doc.idCountry + ', '
                if doc.issueDate:
                    doc_text = doc_text + 'issued: ' + doc.issueDate + ', '
                if doc.expirationDate:
                    doc_text = doc_text + 'expired: ' + doc.expirationDate + ';'
                nationality = nationality + doc_text + '\n'

        personal_details = ''
        if len(self.dateOfBirthList) > 1:
            personal_details = 'Date of birth:\n'
            for date in self.dateOfBirthList:
                if date.mainEntry:
                    personal_details = personal_details + date.dateOfBirth + ' - most possible.\nAdditional dates:\n'
            for date in self.dateOfBirthList:
                if not date.mainEntry:
                    personal_details = personal_details + date.dateOfBirth + ';\n'
        else:
            for date in self.dateOfBirthList:
                personal_details = 'Date of birth:\n' + date.dateOfBirth + ';\n'
        if len(self.placeOfBirthList) > 1:
            personal_details = personal_details + 'Place of birth:\n'
            for place in self.placeOfBirthList:
                if place.mainEntry:
                    personal_details = personal_details + place.placeOfBirth + ' - most possible.\nAdditional places:\n'
            for place in self.placeOfBirthList:
                if not place.mainEntry:
                    personal_details = personal_details + place.placeOfBirth + ';'
        else:
            for place in self.placeOfBirthList:
                personal_details = personal_details + 'Place of birth:\n' + place.placeOfBirth + ';'

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='us',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=self.remarks,
                                            id=self.id)
        return sanction
