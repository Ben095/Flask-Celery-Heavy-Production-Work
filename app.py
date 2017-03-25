import requests
from bs4 import BeautifulSoup
import json
#from py_bing_search import PyBingWebSearch
from urlparse import urlparse
import sys
import urllib2
import re
 
import os
from flask import Flask, render_template, request, redirect, url_for
import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
 
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
import requests
import stripe
from firebase import firebase
#from pyfcm import FCMNotification
import json
import time
from youtubescraper import*
app = Flask(__name__)
 
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
api = Api(app)





# outputDict = {
# 	'prospect_url':fields.String,
# 	'meta_title':fields.String,
# 	'root_domain':fields.String
# }

class OutReachDesk(Resource):
	#@marshal_with(outputDict)
	def get(self, query):
		headers = {
			'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1 like Mac OS X)AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0'

		}
		arr = ['0','23','37','51','65','79']
		appendArr = []
		biggerArr = []
		for i in arr:
			response = requests.get('https://c.bingapis.com/api/custom/opal/otherpage/search?q='+str(query)+'&first='+str(i)+'&rnoreward=1',headers=headers).text
			LoadAsJson = json.loads(response)
			actualItem = LoadAsJson['answers'][0]['webResults']
			appendArr.append(actualItem)

		biggerArr.append(appendArr[0]+appendArr[1]+appendArr[2]+appendArr[3]+appendArr[4]+appendArr[5])
	#	print biggerArr
		rearr = []
		for items in biggerArr:
			eachQuery = items
			for eachQueryString in eachQuery:
				try:
					bingDictionary = {}
					bingDictionary['prospect_url'] = eachQueryString['displayUrl']
					bingDictionary['meta_title'] = eachQueryString['shortTitle'].encode('ascii','ignore')
					url = urlparse(eachQueryString['url'])
					domain = '{uri.scheme}://{uri.netloc}/'.format(uri=url)
					bingDictionary['root_domain'] = domain
					#print domain
					#website = urllib2.urlopen(domain)
					#html = website.read()
					#addys = re.findall('''[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?''', html, flags=re.IGNORECASE)
					#numbers = re.findall('[@\s][69]\d{3}[-\s]?\d{4}[\s\.]',str(html))
					# bingDictionary['emails'] = addys
					# bingDictionary['phonenumbers'] = numbers
				#	sourcecode = requests.get(domain)
			#		plain_text = sourcecode.text
			#		soup = BeautifulSoup(plain_text)
			#		rssArr = []
					formatDomain = str(domain).replace('http://','').replace('https://','')
					fixedDomain = formatDomain.split('/')[0]
					whoisAPI = requests.get('http://api.whoxy.com/?key=f5bd9ed47568013u5c00d35155ec3884&whois='+str(fixedDomain)).text
					#print whoisAPI
				#	check = 'http://104.131.43.184/whois/'+str(domain)
					loadAsJson = json.loads(whoisAPI)
					#print "GOT HERE"
				#	print "Sleeping.."
					try:
						bingDictionary['whois_full_name'] = loadAsJson['registrant_contact']['full_name']
						#print bingDictionary['whois_registrant_city']
					except:
						bingDictionary['whois_full_name'] = "None"
					try:
						bingDictionary['whois_company_name'] = loadAsJson['registrant_contact']['company_name']
					except:
						bingDictionary['whois_company_name'] = "None"
					try:
						bingDictionary['whois_city_name'] =loadAsJson['registrant_contact']['city_name']
						
					except:
						bingDictionary['whois_city_name'] = "None"
					try:
						bingDictionary['whois_country_name'] = loadAsJson['registrant_contact']['country_name']
					except:
						bingDictionary['whois_country_name'] = "None"
					try:
						bingDictionary['whois_email_address'] = loadAsJson['registrant_contact']['email_address']
					
					except:
						bingDictionary['whois_email_address'] = "None"
					try:
						bingDictionary['whois_phone_number'] = loadAsJson['registrant_contact']['phone_number']
					
					except:
						bingDictionary['whois_phone_number'] = "None"
					#for link in soup.find_all("link", {"type" : "application/rss+xml"}):
					#	href = link.get('href')
					#	rssArr.append(href)
					#bingDictionary['RSS_URLS'] = rssArr
					rearr.append(bingDictionary)
				except:
					pass
		return jsonify(results = rearr)


# eachItem = {
# 	'has_link':fields.String,
# 	'video_name':fields.String,
# 	'video_link':fields.String,
# 	'views_count':fields.String,
# 	'channel_name':fields.String,
# 	'channel_link':fields.String,
# 	'business_emails':fields.String,
# 	'links':fields.String
# }
# youtubeoutputdict = {
# 	'results':fields.String
# }
class YoutubeScraper(Resource):
#	@marshal_with(youtubeoutputdict)
	def get(self, keyword):
		includeWithLinks = True
		solveCaptcha = False
		scraper = solve(keyword, solveCaptcha, includeWithLinks, 100, 500)
		finalArr = []
		for finalOutput in scraper:
			internalDictionary = {}
			internalDictionary['has_link'] = finalOutput['video'][0]
			internalDictionary['video_name'] = finalOutput['video'][1]
			internalDictionary['video_link'] = finalOutput['video'][2]
			internalDictionary['views_count'] = finalOutput['video'][3]
			internalDictionary['channel_name'] = finalOutput['channel'][0]
			internalDictionary['channel_link'] = finalOutput['channel'][1]
			internalDictionary['business_emails'] = finalOutput['links'][0]
			internalDictionary['links'] = finalOutput['links'][1:-1]
			finalArr.append(internalDictionary)

		return jsonify(results=finalArr)

api.add_resource(YoutubeScraper,'/api/youtube/<keyword>')
api.add_resource(OutReachDesk,'/api/<query>')

if __name__ == "__main__":
	
	app.run(port=5000)

# with open('bingsearchs.json','wb') as outfile:
# 	json.dump(rearr,outfile,indent=4)
# print len(rearr)