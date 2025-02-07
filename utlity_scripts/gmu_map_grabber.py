import webbrowser

# List of units
units = [
    "Unit 2A (including Pine River WMA)",
    "Unit 2B (including Navajo WMA)",
    "Unit 2C",
    "Unit 4 Humphries/Rio Chama/Sargent WMAs Only (NM Residents Only)",
    "Unit 5A (Public Land Only)",
    "Unit 5B",
    "Unit 6A",
    "Unit 6B",
    "Unit 6C",
    "Unit 7",
    "Unit 8",
    "Unit 9 Marquez/LBar WMA Only (NM Residents Only)",
    "Unit 9 (Including Water Canyon WMA)",
    "Unit 10",
    "Unit 12",
    "Unit 13",
    "Unit 14",
    "Unit 15",
    "Unit 16A",
    "Unit 16B",
    "Unit 16C",
    "Unit 16D",
    "Unit 16E",
    "Unit 17",
    "Unit 18",
    "Unit 19 (excluding WSMR and Ft. Bliss; CWD detected in this area, see page 24)",
    "Unit 191 WSMR portion only",
    "Unit 20",
    "Unit 21",
    "Unit 21A",
    "Unit 21B",
    "Unit 22",
    "Unit 23 (excluding Burro Mountain Area)",
    "Unit 23 Burro Mountain Area Only",
    "Unit 24 (Excluding Fort Bayard Management Area, Including Double E and River Ranch WMAs)",
    "Unit 24 (Including Fort Bayard Management Area)",
    "Unit 25",
    "Unit 26",
    "Unit 27",
    "Unit 28 McGregor Range Portion of Ft. Bliss (CWD detected in this area, see p. 24)",
    "Unit 29",
    "Unit 30",
    "Unit 31 (Including Prairie Chicken WMAs)",
    "Unit 32 (Including Prairie Chicken WMAs)",
    "Unit 33 (Including Prairie Chicken WMAs)",
    "Unit 34 (CWD detected in this area. See page 24)",
    "Unit 36",
    "Unit 37",
    "Unit 38",
    "Unit 39",
    "Unit 40",
    "Unit 41",
    "Unit 42",
    "Unit 43",
    "Unit 45",
    "Unit 47",
    "Unit 48",
    "Unit 49",
    "Unit 50",
    "Unit 51A",
    "Unit 51B",
    "Unit 52",
    "Unit 53",
    "Unit 54",
    "Unit 55",
    "Unit 55A"
    "Unit 55B"
    "Unit 56",
    "Unit 57 Sugarite Canyon State Park Only",
    "Unit 57 (Excluding Sugarite Canyon State Park)",
    "Unit 58",
    "Unit 59"
]

# URL base
base_url = "https://wildlife.dgf.nm.gov/wp-content/uploads/2014/06/game-management-unit-map-boundaries-highres-"

# Function to open URLs in Firefox
def open_urls_in_firefox():
    # Path to Firefox executable (update this to your system's path to Firefox)
    firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"  # Windows example

    # Register Firefox browser
    webbrowser.register("firefox", None, webbrowser.BackgroundBrowser(firefox_path))

    for unit in units:
        # Extract the unit number
        unit_number = unit.split()[1]  # Get the number part (e.g., 'Unit 2A')
        
        # Format the URL with the unit number
        url = f"{base_url}{unit_number.lower().replace(' ', '-')}.pdf"
        
        # Open URL in Firefox
        webbrowser.get("firefox").open(url)

# Call the function
open_urls_in_firefox()
