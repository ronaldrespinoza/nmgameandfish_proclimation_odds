import pdfplumber
import pandas as pd
import re

# Function to parse and extract data from the PDF
def extract_data_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    
    return text


def get_deer_regex():
    return re.compile(
            r"([A-Za-z\s\-\–]+(?:Youth Only|Mobility|Impaired Only|NM Resident|Only|Restricted|Youth)?)\s*"  # Hunt type
            r"([A-Za-z]{3}\s?\.\s?\d{1,2}(?:[-,]?\d{1,2})?\s?(?:-\s?[A-Za-z]{3}\s?\.\s?\d{1,2})?(?:,\s?‘\d{2,4})?)\s*"  # Hunt dates (with two months or year)
            r"([A-Za-z]+-\d{1,2}-\d{3})\s*"  # Hunt code (e.g., DER-2-104)
            r"([A-Za-z\/]+)\s*"  # Fee type (e.g., 'S', 'Q/HD')
            r"(\d+)\s*"  # Number of licenses
            r"([A-Za-z]+)"  # Bag limit (e.g., 'FAD')
            )


def get_elk_regex():
    return re.compile(
            r"([A-Za-z\s\-\–]+(?:Youth Only|Mobility|Impaired Only|NM Resident|Only|Restricted|Youth)?)\s*"  # Hunt type
            r"([A-Za-z]{3}\s?\.\s?\d{1,2}(?:-\d{1,2})?(?:\s?-\s?[A-Za-z]{3}\s?\.\s?\d{1,2})?(?:,\s?'?\d{2,4})?)\s*"
            r"([A-Za-z]+-\d{1,2}-\d{3})\s*"  # Hunt code (e.g., DER-2-104)
            r"([A-Za-z\/]+)\s*"  # Fee type (e.g., 'S', 'Q/HD')
            r"(\d+)\s*"  # Number of licenses
            r"([A-Za-z\/(\d|A-Za-z)]+)"  # Bag limit (e.g., 'FAD')
            )


def parse_hunting_data(text, animal_choice):
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    data = []
    unit = None

    for line in lines:

        if line.startswith("Unit"):
            unit = line.strip()
            continue
        elif line.startswith("Premium Statewide"):
            unit = line.strip()
            continue

        if animal_choice == "elk":
            pattern = get_elk_regex()
        elif animal_choice == "deer":
            pattern = get_deer_regex()

        match = pattern.match(line)
        if match:
            hunt_type = match.group(1).strip()
            hunt_dates = match.group(2).strip()
            hunt_code = match.group(3).strip()
            fee_type = match.group(4).strip()
            licenses = int(match.group(5).strip())
            bag_limit = match.group(6).strip()

            data.append([unit, hunt_type, hunt_dates, hunt_code, fee_type, licenses, bag_limit])
        else:
            continue
        
    return pd.DataFrame(data, columns=["Unit", "Hunt Type", "Hunt Dates", "Hunt Code", "Fee Type", "Licenses", "Bag"])

def scrape_pdf_page_range(pdf_path, start_page, end_page):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        if start_page < 1 or end_page > len(pdf.pages):
            raise ValueError("Page range is out of bounds. The PDF has {} pages.".format(len(pdf.pages)))
        
        for page_num in range(start_page - 1, end_page):
            page = pdf.pages[page_num]
            full_text += page.extract_text()

    return full_text

def scrape_for_deer():
    pdf_path = "input/HNT RIB 2025-26_ENGLISH_Online.pdf"
    animal_choice = 'deer'
    deer_start_page = 55
    deer_end_page = 68
    scraped_text = scrape_pdf_page_range(pdf_path, deer_start_page, deer_end_page)
    return parse_hunting_data(scraped_text, animal_choice)

def scrape_for_elk():
    pdf_path = "input/HNT RIB 2025-26_ENGLISH_Online.pdf"
    animal_choice = 'elk'
    elk_start_page = 75
    elk_end_page = 95
    scraped_text = scrape_pdf_page_range(pdf_path, elk_start_page, elk_end_page)
    return parse_hunting_data(scraped_text, animal_choice)

