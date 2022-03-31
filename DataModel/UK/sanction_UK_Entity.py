class SanctionUKEntity:

    def __init__(self, ParentCompanies=None, BusinessRegistrationNumbers=None, TypeOfEntities=None,
                 Subsidiaries=None):
        if BusinessRegistrationNumbers is None:
            BusinessRegistrationNumbers = []  # list of strings
        self.BusinessRegistrationNumbers = BusinessRegistrationNumbers
        if TypeOfEntities is None:
            TypeOfEntities = []  # list of strings
        self.TypeOfEntities = TypeOfEntities
        if Subsidiaries is None:
            Subsidiaries = []  # list of strings
        self.Subsidiaries = Subsidiaries
        if ParentCompanies is None:
            ParentCompanies = []  # list of strings
        self.ParentCompanies = ParentCompanies
