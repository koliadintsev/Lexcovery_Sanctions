class SanctionUSAVessel:

    def __init__(self, callSign='', vesselType='', vesselFlag='', vesselOwner='', tonnage='', grossRegisteredTonnage=''):
        self.grossRegisteredTonnage = grossRegisteredTonnage
        self.tonnage = tonnage
        self.vesselOwner = vesselOwner
        self.vesselFlag = vesselFlag
        self.vesselType = vesselType
        self.callSign = callSign
