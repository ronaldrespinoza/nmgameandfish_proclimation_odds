class SuccessTotals():
    def __init__(self, resident_total, non_resident_total, outfitter_total):
        self._resident_total = resident_total
        self._non_resident_total = non_resident_total
        self._outfitter_total = outfitter_total

    @property
    def resident_total(self):
        return self._resident_total

    @resident_total.setter
    def resident_total(self, value):
        self._resident_total = value
    
    @property
    def non_resident_total(self):
        return self._non_resident_total

    @non_resident_total.setter
    def non_resident_total(self, value):
        self._non_resident_total = value
    
    @property
    def outfitter_total(self):
        return self._outfitter_total

    @outfitter_total.setter
    def outfitter_total(self, value):
        self._outfitter_total = value
