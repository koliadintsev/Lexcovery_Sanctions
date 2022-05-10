from DataModel.EU.sanction_EU_generic import SanctionEUGeneric
from DataModel.EU.sanction_EU_regulation import SanctionEURegulation
from DataModel import sanction_web

class SanctionEU(SanctionEUGeneric):

    def __init__(self, code='', classificationCode='P', nameAlias=None, citizenship=None, birthdate=None,
                 address=None, regulation = SanctionEURegulation(),
                 identification=None, delistingDate='', designationDate='', unitedNationId='', euReferenceNumber='', id = 0):
        super().__init__()
        self.regulation = regulation
        self.id = id
        if identification is None:
            identification = [] #list of sactionEUIdentificationType
        if address is None:
            address = [] #list of sanctionEUAddress
        if birthdate is None:
            birthdate = [] #list of sanctionEUBirthdate
        if citizenship is None:
            citizenship = [] #list of sanctionEUCitizenship
        if nameAlias is None:
            nameAlias = [] #list of sanctionEUName
        self.euReferenceNumber = euReferenceNumber
        self.unitedNationId = unitedNationId
        self.designationDate = designationDate
        self.delistingDate = delistingDate
        self.identification = identification
        self.address = address
        self.birthdate = birthdate
        self.citizenship = citizenship
        self.nameAlias = nameAlias
        self.classificationCode = classificationCode
        self.code = code
        self.search_fields = []
        for name in self.nameAlias:
            self.search_fields.append(name.wholeName)

    def webify(self):

        main_name = ''
        names = ''
        for name in self.nameAlias:
            if not main_name and (name.nameLanguage == '' or name.nameLanguage == 'EN'):
                main_name = name.wholeName
            else:
                if names:
                    names = names + ';\n' + name.wholeName
                else:
                    names = name.wholeName
                if name.remark:
                    names = names + ', ' + name.remark
        if not main_name:
            main_name = self.nameAlias[0].wholeName

        program = ''
        regulation = self.regulation
        if regulation.programme:
            program = program + regulation.programme + '; '
        if regulation.numberTitle:
            program = program + regulation.numberTitle + '; '
        if regulation.publicationUrl:
            program = program + '<a href="' + regulation.publicationUrl + '">Regulation Details</a>'

        address = ''
        if len(self.address) > 0:
            for a in self.address:
                if a.poBox:
                    address = address + a.poBox+ ', '
                if a.street:
                    address = address + a.street+ ', '
                if a.city:
                    address = address + a.city+ ', '
                if a.region:
                    address = address + a.region+ ', '
                if a.place:
                    address = address + a.place+ ', '
                if a.zipCode:
                    address = address + a.zipCode+ ', '
                if a.countryDescription:
                    address = address + a.countryDescription + ';\n'
                if len(a.contactInfo) > 0:
                    address = address + 'Contact information:\n'
                    for contact in a.contactInfo:
                        address = address + contact.key + ': ' + contact.value + ';\n'

        nationality = ''
        if len(self.citizenship)>0:
            for n in self.citizenship:
                if nationality:
                    nationality = nationality + ';\n' + n.countryDescription
                else:
                    nationality = n.countryDescription
        if len(self.identification)>0:
            if nationality:
                nationality = nationality + ';\n' + 'Documents:\n'
            else:
                nationality = 'Documents:\n'
            for doc in self.identification:
                if doc.identificationTypeDescription:
                    nationality = nationality + ', ' + doc.identificationTypeDescription
                if doc.nameOnDocument:
                    nationality = nationality + ', ' + doc.nameOnDocument
                if doc.number:
                    nationality = nationality + ', ' + doc.number
                if doc.issuedBy:
                    nationality = nationality + ', ' + doc.issuedBy
                if doc.issueDate:
                    nationality = nationality  + ', '+ doc.issueDate
                if doc.countryDescription:
                    nationality = nationality  + ', '+ doc.countryDescription
                nationality = nationality + ';\n'

        personal_details = ''
        functions = ''
        title = ''
        gender = ''
        gender_found = False
        for name in self.nameAlias:
            if name.gender:
                if not gender_found:
                    gender = name.gender
                    gender_found = True
            if name.function:
                functions = functions + name.function + ';\n'
            if name.title:
                title = title + name.title + ';\n'
        if gender:
            personal_details = personal_details + 'Gender: ' + gender + '\n'
        if title:
            personal_details = personal_details + 'Titles: ' + title
        if functions:
            personal_details = personal_details + 'Functions: ' + functions

        if len(self.birthdate) > 0:
            personal_details = personal_details + 'Date of birth:\n'
            for date in self.birthdate:
                if date.birthdate:
                    personal_details = personal_details + date.birthdate + ', '
                if date.city:
                    personal_details = personal_details + date.city + ', '
                if date.region:
                    personal_details = personal_details + date.region + ', '
                if date.countryDescription:
                    personal_details = personal_details + date.countryDescription
                personal_details = personal_details + '\n'

        additional_info = ''
        if self.remark:
            additional_info = self.remark
        additional_info = additional_info + self.add_additional_info(self)

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='eu',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=additional_info,
                                            id=self.id)
        return sanction

    def add_additional_info(self, doc):
        text = ''
        if doc.remark:
            text = doc.remark
        if len(doc.additionalInformation)>0:
            for info in doc.additionalInformation:
                text = text + '\n' + info.key + ': ' + info.value + '\n'
        return text