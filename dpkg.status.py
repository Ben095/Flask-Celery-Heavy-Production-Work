import requests
from bs4 import BeautifulSoup


headers = {
	'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1 like Mac OS X)AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0'
}
response = requests.get('https://c.bingapis.com/api/custom/opal/search?unixTime=1479841193&form=OPSBTW&rnoreward=1&q=ben&color=05847C',headers=headers).text
print response