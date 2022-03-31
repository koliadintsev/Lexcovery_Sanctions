class SanctionUSAAka:

    def __init__(self, uid=0, type='', category='', lastName='', firstName=''):
        self.firstName = firstName
        self.lastName = lastName
        self.category = category
        self.type = type
        self.uid = uid
        name = ''
        if not firstName:
            name = lastName
        else:
            name = firstName + ' ' + lastName
        self.wholeName = name

