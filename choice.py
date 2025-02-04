class Choice():
    def __init__(self, first_choice, second_choice, third_choice, fourth_choice, total_chosen):
        self._first_choice = first_choice
        self._second_choice = second_choice
        self._third_choice = third_choice
        self._fourth_choice = fourth_choice
        self._total_chosen = total_chosen

    @property
    def first_choice(self):
        return self._first_choice

    @first_choice.setter
    def first_choice(self, value):
        self._first_choice = value
    
    @property
    def second_choice(self):
        return self._second_choice

    @second_choice.setter
    def second_choice(self, value):
        self._second_choice = value
    
    @property
    def third_choice(self):
        return self._third_choice

    @third_choice.setter
    def third_choice(self, value):
        self._third_choice = value
    
    @property
    def fourth_choice(self):
        return self._fourth_choice

    @fourth_choice.setter
    def fourth_choice(self, value):
        self._fourth_choice = value
    
    @property
    def total_chosen(self):
        return self._total_chosen

    @total_chosen.setter
    def total_chosen(self, value):
        self._total_chosen = value