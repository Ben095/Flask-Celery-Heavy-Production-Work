import re
import requests
from bs4 import BeautifulSoup

response = requests.get('http://www.nakedbeauty.net.au/bookings.html').text
#soup = BeautifulSoup(response)

soup = '041-709-3500'
#000 000 0000

# phoneregex = re.compile(r'''
# (\+\d)?
# (-)?
# (\d{3}|\(\d{3}\))?
# (\.|-|\s)?
# (\d{3})
# (\.|-|\s)
# (\d{4})
# ''', re.VERBOSE)

phonemo = re.findall('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',str(soup))
print phonemo