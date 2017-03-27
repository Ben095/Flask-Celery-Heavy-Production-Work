import requests
from bs4 import BeautifulSoup
import random
m_dictionary = {}
arr_list = []
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
key, value = random.choice(list(m_dictionary.items()))
print key, value
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