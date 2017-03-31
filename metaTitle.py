import requests
from bs4 import BeautifulSoup


#response = requests.get('https://twitter.com/sproutinnovate').text
bingDictionary = {}
try:
    response = requests.get('https://twitter.com/sproutinnovate').text
    soup = BeautifulSoup(response)
    twitter_followers = soup.findAll('span',attrs={'class':'ProfileNav-value'})[2].text
   # print twitter_followers[2]
   # print twitter_followers
    bingDictionary['twitter_followers'] = twitter_followers
except:
    bingDictionary['twitter_followers'] = 0


print bingDictionary