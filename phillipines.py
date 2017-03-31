import requests
from bs4 import BeautifulSoup
import random
import json
from mozscape import Mozscape

arr = []
m_dictionary = {}
m_dictionary['member-79ea116cb0'] = '43053334ef958fa5668a8afd8018195b'
m_dictionary['member-89df24f83c'] = '0d08685d31a8f724047decff5e445861'
m_dictionary['member-aad6e04a94'] = '8a08a4f2477b3eda0a7b3afa8eb6faaf'
m_dictionary['member-1e51eae111'] = '4f1deaa49d0f4ec8f36778b80a58dba5'
m_dictionary['member-c1d37816b1'] = '47501159d505413721caac9687818f68'
m_dictionary['member-700eebf334'] = '0e7136b3468cd832f6dda555aa917661'
m_dictionary['member-774cfbde7e'] = '481981b24f4a4f08d7c7dc9d5038428f'
m_dictionary['member-34c9052fba'] = '999d2d727bfc11256421c42c529331de'
m_dictionary['member-587eb1767c'] = '8c36e3b36b7d6d352fd943429d97837e'
m_dictionary['member-5fa34d7383'] = '3986edd244ae54e1aa96c71404914578'
bingDictionary = {}
email_arrz = []
bingDictionary['contact_url'] = 'www.depmakeup.com/pages/contact-us'
try:
	if "http:" in bingDictionary['contact_url']:
	    response = requests.get(bingDictionary['contact_url']).text
	    soup = BeautifulSoup(response)
	    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(soup), re.I)
	    for each_emails in emails:
	        print "EACH EMAILS HERE", each_emails

	        email_arrz.append(each_emails)
	else:
		#print "GOT HERE??"

	    response = requests.get('http://'+bingDictionary['contact_url']).text
	    soup = BeautifulSoup(response)
	    print 'http://'+bingDictionary['contact_url']
	    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(soup))
	    print emails
	    for each_emails in emails:
	        print "EACH EMAILS HERE", each_emails

	        email_arrz.append(each_emails)

except:
    pass
bingDictionary['emails'] = email_arrz
print bingDictionary
# #oz_url = site.replace('www.','')
# moz_url = 'true-company.com'

# each_url = 'https://facebook.com/flattummytea'
# if 3 == each_url.count('/') or 4 == each_url.count('/'):
#     bingDictionary['facebook_page_url'] = each_url
#     print "EACH URL", each_url
# else:
#     print "NO 3"
#     bingDictionary['facebook_page_url'] = None

# #while True:
	#try:
#str_fb = 'https://www.facebook.com/mymakeupbrushset/'
#print str_fb.count('/')
# for key, value in m_dictionary.iteritems():
# 	print key, value
# 	try:
# 		client = Mozscape(key, value)
# 		metrics = client.urlMetrics(moz_url)
# 		bingDictionary['PA'] = metrics['upa']
# 		bingDictionary['DA'] = metrics['pda']
# 		bingDictionary['Links'] = metrics['uid']
# 		print bingDictionary
# 	except:
# 		continue
		
# for key, value in m_dictionary.iteritems():
# 	print key, value
# 	try:
# 		client = Mozscape(str(key),str(value))
#     	metrics = client.urlMetrics(str(moz_url))
#     	bingDictionary['PA'] = metrics['upa']
#     	bingDictionary['DA'] = metrics['pda']
#     	bingDictionary['Links'] = metrics['uid']
#     	print bingDictionary
#     except:
#     	continue

# site = 'true-company.com'
# try:
#     key, value = random.choice(list(m_dictionary.items()))
#     client = Mozscape(str(key),str(value))
#     mozscape_dictionary = {}
#     metrics = client.urlMetrics(str(site))
#     bingDictionary['PA'] = metrics['upa']
#     bingDictionary['DA'] = metrics['pda']
#    # bingDictionary['MozRank'] = metrics['ut']
#     bingDictionary['Links'] = metrics['uid']
#     print bingDictionary
# except:

#   	raise
# if 3 == social_email.count('/'):
# 	print "YES"
# if social_email.startswith('//'):
# 	print social_email.replace('//','https://www.')

# response = requests.get('http://loansolutions.ph/').text
# if "remarketing" in response:
# 	print "yrue"

# token = 'EAAZAoe8xotnUBADck4NSbeci4WtDEF8oIaMNzpOTBlMdyvFcdseEuOOqSPlAogiqObbMNXOmKdYllNOxaqOhwlew2OMbbIaQQYuBps SIgcC938zsplGMPAZCWtGu2y8UJnMMYMZBudnO3RGQj3tlVYmS9HY1noZD'
# #token = 'EAAZAoe8xotnUBACKEcMajDZBRTHOdxZBKAXDiBMGCfSaUaCK3HoCMQMwUt a15GEBzcZCCZC8p1MqzFGWjmozGyfZANKWzmiZCB3C576s7WLMjIBLtTtzXh9ZAtodXRfwYlpCneZBFgAJreQQGJf30Td9S4CZCVD2C xOx8ZD'
# #token = 'EAAZAoe8xotnUBAD0h1csxNeglioJUCglIZB0WByze5cx7XtcuOAZA3wtI7xYlI5YESrFeHqzwUZCwKUScHIhb6WZB2FzPKFvdCYhZCBTiAV94E1IzZC2wee7uQBAmO6fwN3FHZBSqjykb1XiFJt5pDrV4myA11NXiwkZD'
# first_items  = 'https://www.facebook.com/sproutsolutionsph/'
# #token = 'EAAZAoe8xotnUBA KZAfR2UT7SFKzME4UmPh66aBNjAJCktmlHKpXAzzm2fn79QsNuHHOlUwJqO9dfWVJiWNLbuM2JZC v0WaGbOIsXOMQQIhFjywZB72mwpUDKRAISV24WHmN0gEFo0ZBLhwfyijvkU2hGqDyiupbkZD'
# #token ='EAAZAoe8xotnUBANtmHgyfiD2aMBIYbOsiQbgzZAFZ CK5gMdMgXOyAZBZAWLSIq1EPyoILZANxRRqz4vvB8QnhvuJlaRSTiSpuSU31wuBygOaWZAAA5d0OFTm1ZC1UIwuTYv9dZCJj5VMZAjN dyANwLiB1j9vIXZBGSD3CYZD'
# bingDictionary = {}
# response = requests.get('https://graph.facebook.com/oauth/access_token?client_id=1803730779944565&client_secret=266970737eaf5570d2e789beeeb6af9c&grant_type=fb_exchange_token&fb_exchange_token='+token).json()
# print response['access_token']
# new_access_token = response.split('access_token=')[-1].split('&expires=')[0]
# convert_to_str = dict(new_access_token)
# print convert_to_str
#tore_token = Token(fb_token=new_access_token)
# print "HI"
# try:
#     split_first = first_items.split('.com/')
#     facebook_group_name = split_first[-1].replace('/','')
#     print facebook_group_name
#     response = requests.get('https://graph.facebook.com/v2.8/search?q='+facebook_group_name+'&type=page&access_token='+token).text
#     jsonLoads = json.loads(response)
#     print jsonLoads
#     arr = jsonLoads['data']
#     first_item_in_query = arr[0]['id']
#     response = requests.get('https://graph.facebook.com/v2.8/'+first_item_in_query+'/?fields=fan_count&access_token='+token).json()
#     #print response
#     bingDictionary['facebook_page_likes'] = response['fan_count']
#     print bingDictionary
# except:
# 	#print "error"
#     pass
# facebook_group_name = 'sproutsolutionsph'
# response = requests.get('https://graph.facebook.com/v2.8/search?q='+facebook_group_name+'&type=page&access_token='+token).text
# jsonLoads = json.loads(response)
# arr = jsonLoads['data']
# first_item_in_query = arr[0]['id']
# response = requests.get('https://graph.facebook.com/v2.8/'+first_item_in_query+'/?fields=fan_count&access_token='+token).json()
# print response
# print response['fan_count']
#print bingDictionary

# m_dictionary = {}
# arr_list = []
# m_dictionary['member-79ea116cb0'] = '43053334ef958fa5668a8afd8018195b'
# m_dictionary['member-89df24f83c'] = '0d08685d31a8f724047decff5e445861'
# m_dictionary['member-aad6e04a94'] = '8a08a4f2477b3eda0a7b3afa8eb6faaf'
# m_dictionary['member-1e51eae111'] = '4f1deaa49d0f4ec8f36778b80a58dba5'
# m_dictionary['member-c1d37816b1'] = '47501159d505413721caac9687818f68'
# m_dictionary['member-700eebf334'] = '0e7136b3468cd832f6dda555aa917661'
# m_dictionary['member-774cfbde7e'] = '481981b24f4a4f08d7c7dc9d5038428f'
# m_dictionary['member-34c9052fba'] = '999d2d727bfc11256421c42c529331de'
# m_dictionary['member-587eb1767c'] = '8c36e3b36b7d6d352fd943429d97837e'
# m_dictionary['member-5fa34d7383'] = '3986edd244ae54e1aa96c71404914578'
# key, value = random.choice(list(m_dictionary.items()))
# print key, value
# bingDictionary = {}
# response = requests.get('http://sprout.ph/').text
# soup = BeautifulSoup(response)
# all_hrefs_arr = soup.findAll('a')

# try:
#     for first_items in all_hrefs_arr:
#         if "facebook.com" in str(first_items):
#             bingDictionary['facebook_page_url'] = first_items['href']
# except:
#     pass
# print bingDictionary