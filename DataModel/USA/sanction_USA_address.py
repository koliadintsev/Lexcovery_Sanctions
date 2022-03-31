class SanctionUSAAddress:

    def __init__(self, uid=0, address1='', address2='', address3='', city='', stateOrProvince='', postalCode='', country=''):
        self.country = country
        self.postalCode = postalCode
        self.stateOrProvince = stateOrProvince
        self.city = city
        self.address3 = address3
        self.address2 = address2
        self.address1 = address1
        self.uid = uid