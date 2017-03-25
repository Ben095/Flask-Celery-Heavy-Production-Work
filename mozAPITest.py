import requests

response = requests.get('https://moz.com/researchtools/ose/api/urlmetrics?site=mymakeupbrushset.com')
print response.text