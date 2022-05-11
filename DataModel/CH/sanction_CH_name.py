# XML class: name

class SanctionCHName:

    def __init__(self, ssid=0, name_type=0, quality='', lang='', name_part=None):
        if name_part is None:
            name_part = []
        self.name_part = name_part
        self.lang = lang
        self.quality = quality
        self.name_type = name_type
        self.ssid = ssid