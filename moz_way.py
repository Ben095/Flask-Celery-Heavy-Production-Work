import requests
from bs4 import BeautifulSoup
import json

response = requests.get('https://moz.com/researchtools/ose/api/urlmetrics?site=www.buxomcosmetics.com')
json_loader = json.loads(response.text)
data_loads = json_loader['data']
authorities = data_loads['authority']
domain_authority = authorities['domain_authority']
page_authority = authorities['page_authority']
print domain_authority, page_authority
print data_loads['page']['inbound_links']
#soup = BeautifulSoup(response)
#print soup.findAll('section',attrs={'class':'box box-content bottom2 main-search'})