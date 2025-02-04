class Residency():
    def __init__(self, resident, non_resident, outfitter):
        self._resident = resident
        self._non_resident = non_resident
        self._outfitter = outfitter

    @property
    def resident(self):
        return self._resident

    @resident.setter
    def resident(self, value):
        self._resident = value
    
    @property
    def non_resident(self):
        return self._non_resident

    @non_resident.setter
    def non_resident(self, value):
        self._non_resident = value
    
    @property
    def outfitter(self):
        return self._outfitter

    @outfitter.setter
    def outfitter(self, value):
        self._outfitter = value