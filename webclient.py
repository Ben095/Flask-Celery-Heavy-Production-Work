from bs4 import BeautifulSoup
import urllib
import requests
from useragent import *
from proxies import *
from time import sleep
import random
import shutil


MAX_TRIES = 20
TIMEOUT = 20

class WebClient:
	
	def __init__(self, minDelay, maxDelay):

		self.min_delay = minDelay
		self.max_delay = maxDelay

		self.s = requests.Session()
		self.proxy = {}
		
		current_user_agent = random_user_agent()
		self.get_headers = {"User-Agent": current_user_agent}
		self.post_headers = {
			"Content-Type":"application/x-www-form-urlencoded",
			"User-Agent": current_user_agent,
			"X-Client-Data":"CIu2yQEIorbJAQjEtskBCLKVygEI9JzKAQ==",
			"X-YouTube-Client-Version":"1.20160707",
			"X-Youtube-Identity-Token":"QUFFLUhqbnotX3dZQzlsWjJ4Yi1EY0FSb0JYanBtNUdSQXw=",
			"X-YouTube-Page-CL":"126879900",
			"X-YouTube-Page-Label":"youtube_20160707_RC2",
			"X-YouTube-Variants-Checksum":"fc5be725e47778ac3f1589f90856a9ec",
			"Host":"www.youtube.com",
			"Origin":"https://www.youtube.com"
		}

	def downloadImage(self, challenge):
		
		url = 'https://www.youtube.com/cimg?c=' + challenge
		response = self.s.get(url, stream=True, headers=self.get_headers)
		with open( challenge + '.png', 'wb+') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response


	def set_proxy(self):
		self.proxy = random_proxy()
		self.s.proxies = self.proxy


	def postContent(self, url, data):
		# POST A CERTAIN DATA TO A GIVEN URL
		for i in range(MAX_TRIES):	
			try:
				r = self.s.post(url, data=data, headers=self.post_headers, proxies=self.proxy, timeout=TIMEOUT)
			except:
				continue
			else:
				return r.text

	def getContent(self, url):
		# DOWNLOAD HTML RESPONSE FROM AN URL	
		data = ""

		for i in range(MAX_TRIES):
			
			try:

				to_wait = float(random.randint(self.min_delay, self.max_delay)/1000.0)
				sleep( to_wait )
				r  = self.s.get(url, headers=self.get_headers, proxies=self.proxy, timeout=TIMEOUT)

			except Exception, e:
				message = str(e)
				print "GETTING CONTENT " + message
				continue
			else:
				data = r.text
				break

		return data