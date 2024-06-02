from bs4 import BeautifulSoup

# Read the HTML content from the file
with open('Wallmart_page.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the span with itemprop="price"
price_span = soup.find('span', itemprop='price')

# Extract the price amount
if price_span:
    price = price_span.text.strip()
    print(f'The price is: {price}')
else:
    print('Price not found')