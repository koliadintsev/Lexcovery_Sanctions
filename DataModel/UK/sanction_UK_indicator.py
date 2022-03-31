class SanctionUKIndicator:

    def __init__(self, AssetFreeze=False, ArmsEmbargo=False, TargetedArmsEmbargo = False, CharteringOfShips=False,
                 ClosureOfRepresentativeOffices=False, CrewServicingOfShipsAndAircraft=False, Deflag=False,
                 PreventionOfBusinessArrangements=False, ProhibitionOfPortEntry=False, TravelBan=False,
                 PreventionOfCharteringOfShips=False, PreventionOfCharteringOfShipsAndAircraft=False,
                 TechnicalAssistanceRelatedToAircraft=False):
        self.TechnicalAssistanceRelatedToAircraft = TechnicalAssistanceRelatedToAircraft
        self.PreventionOfCharteringOfShipsAndAircraft = PreventionOfCharteringOfShipsAndAircraft
        self.PreventionOfCharteringOfShips = PreventionOfCharteringOfShips
        self.TravelBan = TravelBan
        self.ProhibitionOfPortEntry = ProhibitionOfPortEntry
        self.PreventionOfBusinessArrangements = PreventionOfBusinessArrangements
        self.Deflag = Deflag
        self.CrewServicingOfShipsAndAircraft = CrewServicingOfShipsAndAircraft
        self.ClosureOfRepresentativeOffices = ClosureOfRepresentativeOffices
        self.CharteringOfShips = CharteringOfShips
        self.TargetedArmsEmbargo = TargetedArmsEmbargo
        self.ArmsEmbargo = ArmsEmbargo
        self.AssetFreeze = AssetFreeze



