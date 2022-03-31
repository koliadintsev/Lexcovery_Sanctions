class SanctionEUGeneric:

    def __init__(self, remark='', additionalInformation=None):
        if additionalInformation is None:
            additionalInformation = [] #list of sanction_additional_info
        self.additionalInformation = additionalInformation
        self.remark = remark
