import requests
import json
from bs4 import BeautifulSoup

def get_access_token():
	response = requests.get('https://graph.facebook.com/oauth/access_token?client_id=1803730779944565&client_secret=266970737eaf5570d2e789beeeb6af9c&grant_type=fb_exchange_token&fb_exchange_token=EAAZAoe8xotnUBAJ8MnAjytCg3z9B2LUXsb9G83nZAb5hSZCFibGffZCgVg3OB9uF1jihzlE56uGOu9GWw7Dwm0A4iQwGYwCmZA2ocHVPsEKdZCJbuZCfNbw2WyqakzraSGcTNd8nsZB56bKkM1TWFXEX85mjgZBiF2ZAi549ZAAYyPhQRLrnZBTJ6vmKEgiDalpL5e4ZD').text
	new_access_token = response.split('access_token=')[-1].split('&expires=')[0]
	return new_access_token

token = get_access_token()
str = 'https://www.facebook.com/mymakeupbrushset/'
split_first = str.split('.com/')
facebook_group_name = split_first[-1].replace('/','')
response = requests.get('https://graph.facebook.com/v2.8/search?q='+facebook_group_name+'&type=page&access_token='+token).text
jsonLoads = json.loads(response)
arr = jsonLoads['data']
first_item_in_query = arr[0]['id']
response = requests.get('https://graph.facebook.com/v2.8/mymakeupbrushset/?fields=fan_count&access_token='+token).json()
print response['fan_count']
