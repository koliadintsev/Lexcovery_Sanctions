# XML class: day-month-year
class SanctionCHDate:

    def __init__(self, ssid=0, day=0, month=0, year=0, calendar='', quality=''):
        self.quality = quality
        self.calendar = calendar
        self.year = year
        self.month = month
        self.day = day
        self.ssid = ssid