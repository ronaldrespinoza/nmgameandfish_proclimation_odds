from dataclasses import dataclass

@dataclass
class Residency:
    resident: bool
    nonresident: bool
    outfitter: bool
