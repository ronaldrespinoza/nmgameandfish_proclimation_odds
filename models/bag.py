import enum

class Bag(enum.Enum):
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"\'{self.value}\'"
    
    def get_deer_bags():
        return ['A', 'ES', 'ESWTD', 'FAD', 'FAMD', 'FAWTD']
    
    def get_deer_bag_drop_down(self):
        bag_options = []
        for item in self.get_deer_bags():
            bag_options.append({'label': '{}'.format(item), 'value': item})
        return bag_options

    def get_elk_bags():
        return ['A', 'APRE/6', 'APRE/6/A', 'ES', 'MB', 'MB/A']
    
    def get_elk_bag_drop_down(self):
        bag_options = []
        for item in self.get_elk_bags():
            bag_options.append({'label': '{}'.format(item), 'value': item})
        return bag_options

    def get_unit_dropdown_from_bag(self, animal_choice):
        with open('.//input//{}_unit_dropdown.txt'.format(animal_choice), 'r') as file:
            units = file.readlines()
    
        # Strip any unwanted whitespace characters (like newlines)
        units = [unit.strip() for unit in units]
        
        # Create the options for the dropdown menu
        return [{'label': unit, 'value': unit} for unit in units]

    FAMD = "FAMD"
    FAWD = "FAWD"
    ESWTD = "ESWTD"
    FAD = "FAD"
    A = "A"
    ES = "ES"
    MB = "MB"