import requests
from bs4 import BeautifulSoup


response = requests.get('http://sprout.ph/').text
soup = BeautifulSoup(response)
title = soup.find('title').text
print title