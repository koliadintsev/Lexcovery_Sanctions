# XML class: place
class SanctionCHPlace:

    def __init__(self, ssid=0, location='', location_variant=None, area='', area_variant=None, country=''):
        if area_variant is None:
            area_variant = []
        if location_variant is None:
            location_variant = []
        self.country = country
        self.area_variant = area_variant
        self.area = area
        self.location_variant = location_variant
        self.location = location
        self.ssid = ssid
