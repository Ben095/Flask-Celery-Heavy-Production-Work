import requests
from bs4 import BeautifulSoup
import json

# loans = requests.get('http://54.173.222.233/outreach/Skinxl/results').text
# jsoner = json.loads(loans)
# with open('output.json','wb') as outfile:
# 	json.dump(jsoner,outfile,indent=4)


response = requests.get('https://www.leaddyno.com/').text
soup = BeautifulSoup(response)
a_link = soup.findAll('a')
for items in a_link:
	if "contact" in  items['href']:
		print items['href']

def facebook():
	arr = open('root_domains.json')
	Loader = json.load(arr)
	for items in Loader:
		likes = requests.get('https://c.bingapis.com/api/custom/opal/otherpage/search?q=site:facebook.com%20'+str(items)).text
		loadAsJson = json.loads(likes)
		try:
			parse_likes = loadAsJson['answers'][0]['webResults']
			for items in parse_likes:
				if "likes" in items['snippet']:
					list_of_words = items['snippet'].split()
					next_word = list_of_words[list_of_words.index("likes") - 1]
					print next_word, items['url']
		except:
			pass
#facebook()
def twitter():
	arr = open('root_domains.json')
	Loader = json.load(arr)
	for items in Loader:
		likes = requests.get('https://c.bingapis.com/api/custom/opal/otherpage/search?q=site:twitter.com%20'+str(items)).text
		loadAsJson = json.loads(likes)
		try:
			parse_likes = loadAsJson['answers'][0]['webResults']
			twitter_url = parse_likes[0]['url']
			followers = parse_likes[0]['formattedFacts'][0]['items'][0]['text']
			print followers, twitter_url
				
		except:
			pass
#t#witter()
def googlePlus():
	arr = open('root_domains.json')
	Loader = json.load(arr)
	for items in Loader:
		google_plus = requests.get('https://c.bingapis.com/api/custom/opal/otherpage/search?q=site:plus.google.com%20'+str(items)).text
		loadAsJson = json.loads(google_plus)
		#print loadAsJson
		try:
			parse_likes = loadAsJson['answers'][0]['webResults']
			dictionary = {}
			for items in parse_likes:
				list_of_words = items['snippet'].split()
				for second_items in list_of_words:
					if "follower" in second_items:
						#print items
						next_word = list_of_words[list_of_words.index(second_items)-1]
						bingDictionary['followers'] = next_word
						bingDictionary['google_plus_url'] = items['url']
	
			print dictionary
		except:
			bingDictionary['followers'] = None
			bingDictionary['followers_url'] = None
		#print dictionary
#googlePlus()
        # for items in list_of_words:
        #     if "followers" in items:
        #         next_word = list_of_words[list_of_words.index(items)-1]
        #        	print next_word

	# try:		
	# 	parse_likes = loadAsJson['answers'][0]['webResults']
	# 	twitter_url = parse_likes[0]['url']
	# 	followers = parse_likes[0]['formattedFacts'][0]['items'][0]['text']
	# 	print followers
			
	# except:
	# 	pass
#googlePlus()

	# response = requests.get('http://graph.facebook.com/?id='+str(items))
	# loadAsJson = json.loads(response.text)
	# try:
	# 	print loadAsJson['share']['share_count']
	# except:
	# 	print "null"