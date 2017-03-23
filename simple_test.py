import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.mymakeupbrushset.com/').text
soup = BeautifulSoup(response)
a_link = soup.findAll('a')
print a_link
# for href in a_link:
# 	print href['href']