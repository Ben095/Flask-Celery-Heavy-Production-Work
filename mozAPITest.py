import requests

response = requests.get('https://moz.com/researchtools/ose/api/urlmetrics?site=google.com')
print response.text