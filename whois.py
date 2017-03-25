import requests,json
whoisAPI = requests.get('http://104.131.43.184/whois/wholelifeinsurancerates.net').text
loadAsJson = json.loads(whoisAPI)
try:
	registrant_city = loadAsJson['registrant_city']
	registrant_email = loadAsJson['registrant_email']
	registrant_country = loadAsJson['registrant_country']
	registrant_name = loadAsJson['registrant_name']
	registrant_phone_number = loadAsJson['registrant_phone_number']
except:
	pass
print loadAsJson['registrant_city']