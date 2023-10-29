# filename: fetch_webpage.py

import requests
from bs4 import BeautifulSoup

url = "https://cybernatics.io/"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())