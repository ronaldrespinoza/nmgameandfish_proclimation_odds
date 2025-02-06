from dataclasses import dataclass

@dataclass
class Residency:
    resident: bool
    non_resident: bool
    outfitter: bool
