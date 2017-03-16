import requests
from bs4 import BeautifulSoup




response = requests.get('https://www.lendingclub.com/').text
#print response
soup = BeautifulSoup(response)

a_link = soup.findAll('a')
href_arr = []
for items in a_link:

	href_arr.append(items['href'])

#print href_arr
for hrefs in href_arr:
	if "facebook.com" in hrefs:
		print hrefs