# XML class: name-part

class SanctionCHNamePart:

    def __init__(self, value='', spelling_variant=None, order=0, name_part_type=''):
        if spelling_variant is None:
            spelling_variant = []
        self.name_part_type = name_part_type
        self.order = order
        self.spelling_variant = spelling_variant
        self.value = value