import requests

from bs4 import BeautifulSoup
response = requests.get('https://moz.com/researchtools/ose/api/urlmetrics?site=growthgrind.com').text
print response