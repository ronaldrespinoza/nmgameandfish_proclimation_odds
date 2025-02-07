from dataclasses import dataclass

@dataclass
class PercentSuccess:
    resident_percent_success: bool
    non_resident_percent_success: bool
    outfitter_percent_success: bool
    resident_percent_success_first_choice: bool
    resident_percent_success_second_choice: bool
    resident_percent_success_third_choice: bool