import requests
from bs4 import BeautifulSoup
import json


response = requests.get('https://www.instagram.com/biplovdahal/?__a=1').text
json_loader = json.loads(response)
print json_loader