from dataclasses import dataclass

@dataclass
class PercentSuccess:
    resident_percent_success: bool
    resident_percent_success_first_choice: bool
    resident_percent_success_second_choice: bool
    resident_percent_success_third_choice: bool
    nonresident_percent_success: bool
    nonresident_percent_success_first_choice: bool
    nonresident_percent_success_second_choice: bool
    nonresident_percent_success_third_choice: bool
    outfitter_percent_success: bool
    outfitter_percent_success_first_choice: bool
    outfitter_percent_success_second_choice: bool
    outfitter_percent_success_third_choice: bool