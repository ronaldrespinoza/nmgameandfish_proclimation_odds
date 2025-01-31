import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin

# New base URL where the PDFs are stored
base_url = "https://wildlife.dgf.nm.gov/wp-content/uploads/2014/06/"

# Set up Selenium WebDriver (Make sure you have ChromeDriver or use WebDriver Manager)
options = webdriver.ChromeOptions()
options.headless = True  # Run in headless mode (no UI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the webpage using Selenium
driver.get(base_url)

# Wait for the page to load completely (adjust time if needed)
time.sleep(3)

# Find all <a> tags with href attributes (i.e., the links to PDFs)
pdf_links = driver.find_elements(By.TAG_NAME, 'a')

# Filter out only the links that end with .pdf
pdf_urls = [urljoin(base_url, link.get_attribute('href')) for link in pdf_links if link.get_attribute('href') and link.get_attribute('href').endswith('.pdf')]

# Create a directory to store the PDFs if it doesn't exist
os.makedirs('downloaded_pdfs', exist_ok=True)

# Loop through each PDF URL and download it
for pdf_url in pdf_urls:
    pdf_name = pdf_url.split('/')[-1]
    pdf_path = os.path.join('downloaded_pdfs', pdf_name)
    
    # Download the PDF using requests
    pdf_response = requests.get(pdf_url)
    
    if pdf_response.status_code == 200:
        with open(pdf_path, 'wb') as file:
            file.write(pdf_response.content)
        print(f"Downloaded: {pdf_name}")
    else:
        print(f"Failed to download: {pdf_url}")

# Close the Selenium driver
driver.quit()
