import re
import pandas as pd

# Regex pattern to match the hunting data
pattern = re.compile(r"(\b(?:Bow|Muzzle|Any Legal(?:\s?–\s?Youth Only)?)\b)\s+([A-Za-z]{3})\s?\.\s?(\d{1,2})(?:-(\d{1,2}))?(?:\s?-\s?([A-Za-z]{3})\s?\.\s?(\d{1,2})(?:-(\d{1,2}))?)?(?:,\s?‘?(\d{2,4}))?\s+([A-Za-z\-]+-\d{1,2}-\d{3})\s+([A-Za-z\/]+)\s+(\d+)\s+([A-Za-z]+)")
# pattern = re.compile(
#     # Hunt Type (Bow, Muzzle, Any Legal, etc.)
#     r"(\b(?:Bow|Muzzle|Any Legal(?:\s?–\s?Youth Only)?)\b)\s+"  # Hunt type (e.g., "Bow", "Muzzle", "Any Legal")
    
#     # Month for the Hunt (e.g., "Sep", "Jan")
#     r"([A-Za-z]{3})\s?\.\s?"  # Month (e.g., "Sep", "Jan")

#     # Day Range (Start day)
#     r"(\d{1,2})"  # Start day of the hunt (e.g., "1", "15", "25")
    
#     # Optional End Day for the first range (e.g., "24" in "1-24")
#     r"(?:-(\d{1,2}))?"  # End day of the range (optional, e.g., "24" in "1-24")
    
#     # Optional Second Date Range (Month 2)
#     r"(?:\s?-\s?([A-Za-z]{3})\s?\.\s?)?"  # Optional second month (e.g., "Oct")
    
#     # Optional Second Start Day and End Day (for the second range)
#     r"(?:\d{1,2})"  # Second Start day of the hunt (e.g., "1")
#     r"(?:-(\d{1,2}))?"  # Second End day of the hunt (optional)
    
#     # Optional Year (e.g., ‘26)
#     r"(?:,\s?‘?(\d{2,4}))?"  # Optional year (e.g., "‘26")
    
#     # Hunt Code (e.g., "DER-2-104")
#     r"([A-Za-z]+-\d{1,2}-\d{3})\s+"  # Hunt code (e.g., "DER-2-104")
    
#     # Fee Type (e.g., "S", "HD")
#     r"([A-Za-z\/]+)\s+"  # Fee type (e.g., "S", "HD")
    
#     # Number of Licenses
#     r"(\d+)\s+"  # Number of licenses (e.g., "40", "100")
    
#     # Bag Limit (e.g., "FAD", "A", "ES")
#     r"([A-Za-z]+)"  # Bag limit (e.g., "FAD", "A", "ES")
# )

# Text to match
text = """Bow Sep . 1-24 DER-2-104 S 40 FAD
 Bow Jan . 1-15, ‘26 DER-2-106 HD 80 FAD
 Muzzle Sep . 27-Oct .3 DER-3-108 S 50 FAD
 Any Legal – Youth Only Oct . 25-29 DER-1-100 S 25 FAD
 Any Legal Nov . 1-5 DER-1-101 S 150 FAD
 Any Legal – Youth Only Nov . 22-30 DER-1-103 S 15 FAD"""

# Prepare a list to hold the rows of the DataFrame
data = []

# Test each line
for line in text.splitlines():
    line = line.strip()
    match = pattern.match(line)
    if match:
        # Extract matched groups
        hunt_type = match.group(1)
        month1 = match.group(2)
        day1_start = match.group(3)
        day1_end = match.group(4)
        month2 = match.group(5)
        day2_start = match.group(6)
        day2_end = match.group(7)
        year = match.group(8)
        hunt_code = match.group(9)
        fee_type = match.group(10)
        licenses = match.group(11)
        bag_limit = match.group(12)
        
        # Format the hunt dates properly
        if month2:
            hunt_dates = f"{month1} {day1_start}-{day1_end} - {month2} {day2_start}-{day2_end}"
        else:
            hunt_dates = f"{month1} {day1_start}-{day1_end}"
        if year:
            hunt_dates += f", '{year}"
        
        # Append the row as a dictionary
        data.append({
            "Hunt Type": hunt_type,
            "Hunt Dates": hunt_dates,
            "Hunt Code": hunt_code,
            "Fee Type": fee_type,
            "Licenses": licenses,
            "Bag Limit": bag_limit
        })
    else:
        print(f"No match for line: {line}")

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Display the DataFrame
print(df)
