from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Path to your ChromeDriver (update path if necessary)
CHROMEDRIVER_PATH = "/path/to/chromedriver"

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no browser window)
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

URL = "https://exam.sanand.workers.dev/tds-2025-01-ga1#hq-css-selectors"
driver.get(URL)

# Wait for JavaScript to load (adjust sleep time if needed)
time.sleep(3)

# Get the fully loaded page source
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Find divs with class 'foo'
foo_divs = soup.select("div.foo")

if foo_divs:
    print(f"Found {len(foo_divs)} divs with class 'foo'!")
    data_values = [int(div["data-value"]) for div in foo_divs if "data-value" in div.attrs]
    total_sum = sum(data_values)
    print(f"Sum of data-value attributes: {total_sum}")
else:
    print("Error: 'foo' not found in HTML structure.")
