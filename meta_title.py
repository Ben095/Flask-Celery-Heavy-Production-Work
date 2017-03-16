import requests
from bs4 import BeautifulSoup
import json


file = open('domains_to_test','r')
items = file.read().split('\n')
each_url = items
output_arr = []
for each_url_text in each_url:
	output_dictionary = {}
	response = requests.get(each_url_text).text
	soup = BeautifulSoup(response)
	main_tags = soup.findAll('img')
	meta_title_arr = []
	for alt in main_tags:
		alt = alt.get('alt')
		if alt is None:
			pass
		else:
			meta_title_arr.append(alt)
	output_dictionary['meta_title'] = meta_title_arr[0]
	output_dictionary['url'] = each_url_text
	output_arr.append(output_dictionary)
	print output_dictionary
	#print output_arr
with open('urls.json','wb') as outfile:
	json.dump(output_arr,outfile,indent=4)