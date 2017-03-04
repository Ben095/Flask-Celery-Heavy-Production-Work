import requests
from bs4 import BeautifulSoup
import json




response = requests.get('https://plus.google.com/+checkcity').text
soup = BeautifulSoup(response)
print soup.find('div',attrs={'class':"C98T8d GseqId b12n5"}).text.split('-')[0].replace('followers','')
# response = requests.get('https://www.facebook.com/SunTrust').text
# soup = BeautifulSoup(response)
# likes = soup.find('span', attrs={'class':'_52id _50f5 _50f7'}).text.replace('likes','')

# response = requests.get('http://www.checkcity.com/').text
# #response = requests.get('https://www.suntrust.com/').text
# soup = BeautifulSoup(response)
# a = soup.findAll('a')

# all_hrefs_arr = []
# for items in a:
# 	try:
# 		all_hrefs_arr.append(items['href'])

# 	except:
# 		pass
# for items in all_hrefs_arr:
# 	if "plus.google.com" in items:
# 		print items
	# try:
	# 	if "facebook.com" in items['href']:
	#  		facebook_page_url = items['href']
	# except:
	# 	continue
# response = requests.get('https://www.linkedin.com/countserv/count/share?url=https://asdasdasd.com').text
# count = response.split(',')[0].split('{')[-1].split(':')
# linkedInCount = count[-1]
# bingDictionary = {}
# response = requests.get('https://www.linkedin.com/countserv/count/share?url=https://www.ship2anywhere.com.au/').text
# convert_to_dict = response.replace('IN.Tags.Share.handleCount(','').replace(");",'')
# loadAsJson = json.loads(convert_to_dict)
# print loadAsJson['count']
# count = response.split(',')[0].split('{')[-1].split(':')
# linkedInCount = count[-1]
# bingDictionary['linkedin_shares'] = linkedInCount
# print bingDictionary

#try:
# response = requests.get('https://plusone.google.com/_/+1/fastbutton?url=https://studentloans.gov').text
# soup = BeautifulSoup(response)
# follow_count = soup.find('div',attrs={'id':'aggregateCount'}).text
# print follow_count
# except:
# 	pass