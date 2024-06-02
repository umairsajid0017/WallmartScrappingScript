import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
import time

# Auto install chromedriver
chromedriver_autoinstaller.install()

# Specify the path to the Chrome executable for Flatpak installation (adjust the path as needed)
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# Set Chrome options
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
# Avoiding detection
options.add_argument('--disable-blink-features=AutomationControlled')
options.binary_location = chrome_path

# Read links from the text file
with open('input_links.txt', 'r') as file:
    urls = [url.strip() for url in file.readlines()]

# List to store extracted data
extracted_data = []

def extract_price(url, wait_secs_for_page_load):
    # Define and launch the driver
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.delete_all_cookies()
    driver.maximize_window()

    print(f"Processing URL: {url}")
    driver.get(url)

    time.sleep(wait_secs_for_page_load)  # Wait for the page to load completely

    # Try to find the price element
    try:
        price_element = driver.find_element(By.XPATH, '//span[@data-testid="price-wrap"]//span[@itemprop="price"]')
        price = price_element.text.strip()
        print(f"Price found: {price}")

        # Return the extracted data
        return {'Link': url, 'Price': price}
    except Exception as e:
        print("Price not found on the page.")
        return {'Link': url, 'Price': 'Not found'}
    finally:
        driver.quit()

# Calculate the total time required to process all URLs
url_length = len(urls)
wait_secs_for_new_link = 30
wait_secs_for_page_load = 5
total_secs = wait_secs_for_new_link * url_length + wait_secs_for_page_load * url_length
total_mins = total_secs / 60
print(f"Total URLs: {url_length} will take approximately {total_mins:.2f} minutes to process.")

start_time = time.time()

# Iterate through each URL and call the function
for index, url in enumerate(urls):
    data = extract_price(url, wait_secs_for_page_load)
    extracted_data.append(data)

    elapsed_time = (time.time() - start_time) / 60  # elapsed time in minutes
    remaining_time = (total_mins - elapsed_time) if index < url_length - 1 else 0
    print(f"Price {data['Price']} | Link {index + 1} of {url_length} - Time Left {remaining_time:.2f} mins - Time Elapsed {elapsed_time:.2f} mins")

    time.sleep(wait_secs_for_new_link)  # Wait before processing the next URL

# Create a DataFrame from the extracted data
output_df = pd.DataFrame(extracted_data)

# Save the DataFrame to a CSV file without the curly braces
output_df.to_csv('output_prices.csv', index=False, columns=['Link', 'Price'])
print("Data saved to output_prices.csv")
