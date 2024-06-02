import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = 'https://www.walmart.com/ip/Scrubbing-Bubbles-Toilet-Gel-Rainshower-2-Dispensers-30-Gel-Discs/310719024'

# Fetch the HTML content from the URL
response = requests.get(url)
html_content = response.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

print(soup.prettify())

# Find the span with itemprop="price"
price_span = soup.find('span', itemprop='price')

# Extract the price amount
if price_span:
    price = price_span.text.strip()
    print(f'The price is: {price}')
else:
    print('Price not found')