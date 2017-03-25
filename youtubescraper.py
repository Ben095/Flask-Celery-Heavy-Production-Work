import json
from captcha import *
import csv
import os
from requests.auth import HTTPProxyAuth
import threading
from webclient import *
import threading

YOUTUBE_BASEURL = "https://www.youtube.com"

min_delay = 1000
max_delay = 2500

MAX_TRIES = 20
UNSOLVED_CAPTCHAS = 0

biggestArr = []
class Scrapper:
	def __init__(self, to_scrape, solveCaptcha, includeWithLinks):
		self.to_do = to_scrape

		self.results = []
		self.solveCaptcha = solveCaptcha
		self.includeWithLinks = includeWithLinks

		self.client = WebClient(min_delay, max_delay)


	def work(self):
		
		for searchPage in self.to_do:
			data = self.loadPage(searchPage)
			self.scrapeContent(data, self.solveCaptcha, self.includeWithLinks)


	def foundLinks(self, url):

		data = self.client.getContent(url)

		soup = BeautifulSoup(data)

		description = soup.findAll('p', { "id" : "eow-description"} )

		if len(description) > 0:
			links = description[0].findAll('a')

			if len(links) > 0:
				return True
		return False


	def getChannelLinks(self, url, solveCaptcha):

		result = []
		
		for i in range(MAX_TRIES):
			try:
				data = self.client.getContent(url)
				soup = BeautifulSoup(data)

				channel_id = soup.findAll('meta', {"itemprop": "channelId"})[0]["content"]

				links = soup.findAll('li', {"class": "channel-links-item"} )

				result = []

				# SOLVE CAPTCHA
				str1 = "'XSRF_TOKEN': "
				pos = data.find(str1) + len(str1) + 1

				session_token = data[pos:]

				str1 = ','
				pos = session_token.find(str1)

				session_token = session_token[:pos-1]


				needle = "business-email-button"

				pos = data.find(needle)

				if pos > -1 and solveCaptcha == True:
					#print "WE ARE GOING TO SOLVE A CAPTCHA"
					email = self.getBusinessEmail(channel_id, session_token) 

					if len(email) < 3:
						continue

					result.append( email )
				else:
					
					email_span = soup.findAll('span', {"class": "business-email-inline"})

					if len(email_span) > 0:
						result.append( email_span[0].text )
					else:
						result.append( "" )


				# GET LINKS
				for link in links:
					actual_link = link.findNext('a')
					result.append( actual_link["href"] )

				break

			except Exception, e:
				print "GETTING CHANNEL LINKS " +str(e)
				continue
		return result

	def getBusinessEmail(self, channel_id, session_token):

		data = self.client.getContent("https://www.youtube.com/channels_profile_ajax?action_get_business_email_captcha=1")

		dictionary = json.loads(data)
		
		data = dictionary["html_content"]

		soup = BeautifulSoup(data)


		challenge = soup.findAll('input', {"name" : "challenge"})[0]["value"]

		self.client.downloadImage(challenge)
		response = getCaptcha(challenge)

		data={"response": response, "challenge": challenge, "channel_id": channel_id, "session_token": session_token}


		print "TRYING TO SOLVE ONE CAPTCHA"
		for i in range(MAX_TRIES):
			try:

				data = self.client.postContent("https://www.youtube.com/channels_profile_ajax?action_verify_business_email_captcha=1", data)


				print "DATA = " + data


				# check if captcha failed
				failed = "match the word verification"
				if data.find(failed) > -1:
					continue

				# get the email if it's correct
				dictionary = json.loads(data)
				data = dictionary["html_content"]
				soup = BeautifulSoup(data)
				link = soup.findAll('a')
				if len(link) > 0:
					return link[0].text
				
				return ""

			except Exception,e :
				print "ERROR POSTING CAPTCHA"
				print str(e)
				continue

		return ""

	def loadPage(self, url):


		for i in range(MAX_TRIES):
			try:
				

				data = self.client.getContent(url)
				soup = BeautifulSoup(data,from_encoding="utf-8")
				videos = soup.findAll('div', { "class": "yt-lockup-content"})

				if len(videos) > 0:
					return data

				continue

			except Exception, e:
				print str(e)
				continue
		return ""

	def scrapeContent(self, data, solveCaptcha, includeWithLinks):

		# SCRAPE THE CONTENT FROM A GIVEN PAGE
		soup = BeautifulSoup(data,from_encoding="utf-8")

		for video in soup.findAll('div', { "class": "yt-lockup-content"}):

			video_link = video.findNext('a')

			channel_link = video_link.findNext('a')

			video_info = video.findNext('ul', { "class": "yt-lockup-meta-info"} )

			views_count = 0
			if video_info is not None:
				options = video_info.findChildren()

				if len(options) > 1:
					views_count = options[1].text

			video_title = video_link.text
			video_link = YOUTUBE_BASEURL + video_link["href"]

			bad = "googleads"
			bad2 = "playlist"
			bad3 = "user"
			
			pos = video_link.find(bad)
			pos2 = video_link.find(bad2)
			pos3 = video_link.find(bad3)

			if pos > -1 or pos2 > -1 or pos3 > -1:
				# THIS IS NOT ACTUALLY A VIDEO
				continue


			channel_name = channel_link.text
			channel_link = YOUTUBE_BASEURL + channel_link["href"]

			bad = "watch"
			pos = channel_link.find(bad)

			print "HERE"

			if pos > -1:
				# THIS IS NOT A CORRECT CHANNEL
				continue

			has_link = False

			if self.foundLinks(video_link) == True:
				has_link = True


			if has_link == False or includeWithLinks == True:
				
				if has_link == True:
					link_label = "YES"
				else:
					link_label = "NO"

				try:
					video = [link_label, video_title, video_link, views_count]
					#video = [ str(x) for x in video]
					video = [ x.encode('utf-8') for x in video ]

					channel = [channel_name, channel_link]
					#channel = [ str(x) for x in channel]
					channel = [ x.encode('utf-8') for x in channel ]
					
					links = self.getChannelLinks(channel_link + "/about", solveCaptcha)
					#links = [ str(x) for x in links]
					links = [ x.encode('utf-8') for x in links ]
					

					row = []
					row.extend(video)
					row.extend(channel)
					row.extend(links)
					dictionary = {}
					dictionary['video'] = video
					dictionary['channel'] = channel
					dictionary['links'] = links


					self.results.append(dictionary)

					with open('outputresultssc.json','wb') as outfile:
						json.dump(self.results,outfile,indent=4)
				except:
					print "FOUND INVALID VIDEO"
			



def value_is_int(value):
    try:
        tempVal = int(value)
        return True
    except:
        return False



def solve( keyword, solveCaptcha, includeWithLinks, mint, maxt):

	global min_delay, max_delay

	min_delay = mint
	max_delay = maxt


	# load first page
	url = "https://www.youtube.com/results?"
	keyword = urllib.urlencode( { "search_query" : keyword, "sp" : "CAM%3D" } )


	#wr  = csv.writer(response)

	row = ["has link", "video name", "video link", "views count", "channel name", "channel link", "business email", "links"]
	#wr.writerow(row)

	client = WebClient(min_delay, max_delay)

	data = client.getContent(url + keyword)
	soup = BeautifulSoup(data)

	to_scrape = [ [], [], []]


	for link in soup.findAll('a'):
		needle = "/results?"

		inner_text = link.text

		if value_is_int(inner_text):
			if link["href"].find(needle) > -1:
				if link.text > 0:

					url = YOUTUBE_BASEURL + link["href"]

					pageNumber = int(link.text)

					if pageNumber < 3:
						to_scrape[0].append(url)
					else:
						if pageNumber < 5:
							to_scrape[1].append(url)
						else:
							to_scrape[2].append(url)

					print url


	scrappers = [Scrapper( to_scrape[0], solveCaptcha, includeWithLinks),
		Scrapper( to_scrape[1], solveCaptcha, includeWithLinks),
		Scrapper( to_scrape[2], solveCaptcha, includeWithLinks)]

	
	threads = []

	for scrapper in scrappers:
		current_thread = threading.Thread(target=scrapper.work)
		current_thread.start()
		threads.append(current_thread)

	for t in threads:
		t.join()

	biggestArrz = []
	for scrapper in scrappers:
		for row in scrapper.results:
			biggestArrz.append(row)
	return biggestArrz



