# Install the necessary packages
# pip install selenium
# pip install chromedriver-autoinstaller
# pip install pandas

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
import time

# Auto install chromedriver
chromedriver_autoinstaller.install()

# Specify the path to the Chrome executable for Flatpak installation
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Adjust the path as needed

# Specify the path to the user profile directory
user_profile = "C:\\Users\\Umair\\AppData\\Local\\Google\\Chrome\\User Data\\Guest Profile"  # Adjust the path as needed

# Set Chrome options
options = webdriver.ChromeOptions()
options.binary_location = chrome_path
options.add_argument(f"user-data-dir={user_profile}")

# Define and launch the driver
service = Service()
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# Read links from the text file
with open('input_links.txt', 'r') as file:
    urls = file.readlines()

# List to store extracted data
extracted_data = []

try:
    # Iterate through each URL
    for url in urls:
        url = url.strip()
        print(f"Processing URL: {url}")

        driver.get(url)

        # Allow time for the page to load
        time.sleep(5)

        # Scroll down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Allow time for the page to load after scrolling
        time.sleep(2)

        # Try to find the price element
        try:
            price_element = driver.find_element(By.XPATH, '//span[@data-testid="price-wrap"]//span[@itemprop="price"]')
            price = price_element.text.strip()
            print(f"Price found: {price}")

            # Append the extracted data to the list
            extracted_data.append({'Link': url, 'Price': price})
        except Exception as e:
            print("Price not found on the page.")
            print(f"Error: {e}")

finally:
    # Close the browser
    driver.quit()

# Create a DataFrame from the extracted data
output_df = pd.DataFrame(extracted_data)

# Save the DataFrame to a CSV file
output_df.to_csv('output_prices.csv', index=False)
