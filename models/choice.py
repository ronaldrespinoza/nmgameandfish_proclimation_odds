from dataclasses import dataclass

@dataclass
class Choice:
    first_choice: bool
    second_choice: bool
    third_choice: bool
    fourth_choice: bool
    total_chosen: bool