class SuccessPercentages():
    def __init__(self, resident_percentages, non_resident_percentages, outfitter_percentages):
        self._resident_percentages = resident_percentages
        self._non_resident_percentages = non_resident_percentages
        self._outfitter_percentages = outfitter_percentages

    @property
    def resident_percentages(self):
        return self._resident_percentages

    @resident_percentages.setter
    def resident_percentages(self, value):
        self._resident_percentages = value
    
    @property
    def non_resident_percentages(self):
        return self._non_resident_percentages

    @non_resident_percentages.setter
    def non_resident_percentages(self, value):
        self._non_resident_percentages = value
    
    @property
    def outfitter_percentages(self):
        return self._outfitter_percentages

    @outfitter_percentages.setter
    def outfitter_percentages(self, value):
        self._outfitter_percentages = value