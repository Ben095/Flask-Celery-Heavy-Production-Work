# import requests

# response = requests.get('https://moz.com/researchtools/ose/api/urlmetrics?site=www.makeoverforall.com')
# print response
import requests
from bs4 import BeautifulSoup
import re 
response = requests.get('www.makeoverforall.com/contact').text
soup = BeautifulSoup(response)
emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(soup), re.I)
print emails