import requests
from bs4 import BeautifulSoup
import random
import json

first_items  = 'https://www.facebook.com/sproutsolutionsph/'
token = 'EAAZAoe8xotnUBA KZAfR2UT7SFKzME4UmPh66aBNjAJCktmlHKpXAzzm2fn79QsNuHHOlUwJqO9dfWVJiWNLbuM2JZC v0WaGbOIsXOMQQIhFjywZB72mwpUDKRAISV24WHmN0gEFo0ZBLhwfyijvkU2hGqDyiupbkZD'
bingDictionary = {}
print "HI"
try:
    split_first = first_items.split('.com/')
    facebook_group_name = split_first[-1].replace('/','')
    print facebook_group_name
    response = requests.get('https://graph.facebook.com/v2.8/search?q='+facebook_group_name+'&type=page&access_token='+token).text
    jsonLoads = json.loads(response)
    print jsonLoads
    arr = jsonLoads['data']
    first_item_in_query = arr[0]['id']
    response = requests.get('https://graph.facebook.com/v2.8/'+first_item_in_query+'/?fields=fan_count&access_token='+token).json()
    #print response
    bingDictionary['facebook_page_likes'] = response['fan_count']
    print bingDictionary
except:
	#print "error"
    pass
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