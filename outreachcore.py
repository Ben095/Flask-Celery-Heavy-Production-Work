import requests
from bs4 import BeautifulSoup
import json
# from py_bing_search import PyBingWebSearch
from urlparse import urlparse
import sys
import urllib2
import re
from multiprocessing import Pool
from tornado import ioloop, httpclient
from flask.ext.sqlalchemy import SQLAlchemy
import xlsxwriter
import os
from flask import Flask, render_template, request, redirect, url_for
import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from youtubescraper import*
from flask import make_response
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
import requests
import stripe
from firebase import firebase
# from pyfcm import FCMNotification
import json
import time
# from youtubescraper import*
import grequests
from grequests import*
from functools import partial
from mozscape import Mozscape

from urlparse import urlparse
from threading import Thread
import httplib
import sys
from Queue import Queue
import logging
import requests
from requests.adapters import HTTPAdapter 
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from celery import Celery
from flask import Response
from itertools import chain
from celery import Celery
from celery.task.control import inspect
from celery.result import AsyncResult
from time import sleep
#from models import*
from celery.result import AsyncResult
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import lepl.apps.rfc3696
from itertools import cycle

rearr = []
celery = Celery('tasks', backend='amqp', broker='amqp://')
log = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import*



@app.route('/outreach/<query>')
def OutReacherDesk(query):
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

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1 like Mac OS X)AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0'

    }
    arr = ['0', '23', '37', '51', '65', '79']
    appendArr = []  
    biggerArr = []
    for i in arr:
        response = requests.get('https://c.bingapis.com/api/custom/opal/otherpage/search?q=' + str(
            query) + '&first=' + str(i) + '&rnoreward=1', headers=headers).text
        LoadAsJson = json.loads(response)
        with open('check_thisoutput.json','wb') as outfile:
        	json.dump(LoadAsJson,outfile,indent=4)
     	actualItem = LoadAsJson['answers'][0]['webResults']
      	appendArr.append(actualItem)

 	try:      	
		biggerArr.append(appendArr[
	    0] + appendArr[1] + appendArr[2] + appendArr[3] + appendArr[4] + appendArr[5])
	except:
		pass

    with open("check_output.json",'wb') as outfile:
    	json.dump(biggerArr,outfile,indent=4)



    rearr = []
    d = cycle(m_dictionary.iteritems())
    for items in biggerArr:
        eachQuery = items
        domainArray = []
        eachPageWhoisResult = []
        async_list = []
        url_list = []
        for eachQueryString in eachQuery:
            try:
                ## moz goes here

                bingDictionary = {}

                bingDictionary['prospect_url'] = eachQueryString[
                    'displayUrl']
                try:
                    defined = d.next()
                    client = Mozscape(str(defined[0]),str(defined[1]))

                    mozscape_dictionary = {}
                    metrics = client.urlMetrics(str(eachQueryString['displayUrl']))
                    print metrics
                    bingDictionary['PA'] = metrics['upa']
                    bingDictionary['DA'] = metrics['pda']
                    bingDictionary['MozRank'] = metrics['ut']
                except: 
                    #pass
                    bingDictionary['PA'] = "none"
                    bingDictionary['DA'] = "none"
                    bingDictionary['MozRank'] = "none"
                
                response = requests.get('http://graph.facebook.com/?id='+str(eachQueryString['displayUrl']))
                loadAsJson = json.loads(response.text)
                try:
                    bingDictionary['facebook_shares'] = loadAsJson['share']['share_count']
                except:
                    bingDictionary['facebook_shares'] = "null"
                
                bingDictionary['meta_title'] = eachQueryString[
                    'shortTitle'].encode('ascii', 'ignore')
                url = urlparse(eachQueryString['url'])
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=url)
                bingDictionary['root_domain'] = domain
                likes = requests.get('https://c.bingapis.com/api/custom/opal/otherpage/search?q=site:facebook.com%20'+str(domain)).text
                loadAsJson = json.loads(likes)
                try:
                    parse_likes = loadAsJson['answers'][0]['webResults']
                    for items in parse_likes:
                        if "likes" in items['snippet']:
                            list_of_words = items['snippet'].split()
                            next_word = list_of_words[list_of_words.index("likes") - 1]
                            bingDictionary['facebook_likes'] = next_word
                            bingDictionary['facebook_url'] = items['url']
                except:
                    bingDictionary['facebook_likes'] = None
                    bingDictionary['facebook_url'] = None

                twitter = requests.get('https://c.bingapis.com/api/custom/opal/otherpage/search?q=site:twitter.com%20'+str(domain)).text
                loadAsJson = json.loads(twitter)
                try:
                    parse_likes = loadAsJson['answers'][0]['webResults']
                    bingDictionary['twitter_url'] = parse_likes[0]['url']
                    bingDictionary['twitter_followers'] = parse_likes[0]['formattedFacts'][0]['items'][0]['text']
                except:
                    bingDictionary['twitter_followers'] = None
                    bingDictionary['twitter_url'] = None

                google_plus = requests.get('https://c.bingapis.com/api/custom/opal/otherpage/search?q=site:https://plus.google.com%20http://www.jackdaniels.com/').text
                loadAsJson = json.loads(google_plus)
                try:
                    parse_likes = loadAsJson['answers'][0]['webResults']
                    dictionary = {}
                    for items in parse_likes:
                        list_of_words = items['snippet'].split()
                        for items in list_of_words:
                            if "follower" in items:
                                next_word = list_of_words[list_of_words.index(items)-1]
                                bingDictionary['google_plus_followers'] = next_word
                                bingDictionary['google_plus_url'] = items['url']
                except:
                    bingDictionary['google_plus_followers'] = None
                    bingDictionary['google_plus_url'] = None
                formatDomain = str(domain).replace(
                    'http://', '').replace('https://', '')
                fixedDomain = formatDomain.split('/')[0].replace('https://www.','').replace('http://www.','').replace('www.','')
                print fixedDomain
                whoisAPI = 'http://api.whoxy.com/?key=f5bd9ed47568013u5c00d35155ec3884&whois=' + \
                    str(fixedDomain)
                domainArray.append(whoisAPI)
                bingDictionary['whoisData'] = "None"
                bingDictionary['social_shares'] = "None"
                miniArz = []
                try:
                	response = requests.get('http://104.131.43.184/whois/'+str(fixedDomain)).text
                	min_text = 'http://104.131.43.184/whois/'+str(fixedDomain)
                	url_list.append(str(min_text))
                	loadAsJson = json.loads(response)
               	except:
               		pass
                whoisDictionary = {}
                try:
                    whoisDictionary['domain_name'] = loadAsJson['domain_name']
                except:
                    whoisDictionary['domain_name'] = "None"
                try:
                    whoisDictionary['whois_full_name'] = loadAsJson['registrant']['name']
                except:
                    whoisDictionary['whois_full_name'] = "None"
                try:
                    whoisDictionary['whois_city_name'] = loadAsJson['registrant']['city_name']
                except:
                    whoisDictionary['whois_city_name'] = "None"
                try:
                    whoisDictionary['whois_country_code'] = loadAsJson['registrant']['country_code']
                except:
                    whoisDictionary['whois_country_code'] = "None"
                try:
                    whoisDictionary['whois_email_address'] = loadAsJson['registrant']['email']
                except:
                    whoisDictionary['whois_email_address']="None"
                try:
                    whoisDictionary['whois_phone_number'] = loadAsJson['registrant']['phone_number']
                except:
                    whoisDictionary['whois_phone_number'] = "None"
                try:
                    email_response = requests.get(domain).text
                except:
                    pass
                phoneRegex = re.compile(r'''
                    # 415-555-0000, 555-9999, (415) 555-0000, 555-000 ext 12345, ext. 12345 x12345
                    (
                    ((\d\d\d) | (\(\d\d\d\)))?          #area code (optional)
                    (/s|-)                              #first seperator
                    \d\d\d                              #first 3 digits
                    -                                   #second seperator
                    \d\d\d\d                            #last 4 digits
                    (((ext(\.)?\s) |x)                  #extension word-part (optional)
                    (\d{2,5}))?                         #extension number-part (optional)
                    )                                   
                    ''', re.VERBOSE)

                soup = BeautifulSoup(email_response)
               # print soup
                extractedPhone = phoneRegex.findall(str(soup))
                RSS_ARR = []
                for link in soup.find_all("link", {"type" : "application/rss+xml"}):
                    href = link.get('href')
                    RSS_ARR.append(href)
                allPhoneNumbers = []
                for phoneNumber in extractedPhone:
                    allPhoneNumbers.append(phoneNumber[0])
                email_arr = []
                bingDictionary['phone_numbers'] = allPhoneNumbers
                bingDictionary['RSS_URL'] = RSS_ARR
                emails = re.search(r'[\w\.-]+@[\w\.-]+', str(soup))
                if emails:
                    if "." in emails.group()[-1]:
                        new_emails = emails.group()[:-1]
                        email_validator = lepl.apps.rfc3696.Email()
                        if not email_validator(new_emails):
                            pass
                        else:
                            email_arr.append(new_emails)
                    else:               
                        email_string = emails.group()
                        email_validator = lepl.apps.rfc3696.Email()
                        if not email_validator(email_string):
                            pass
                        else:
                            email_arr.append(email_string)
                bingDictionary['emails'] = email_arr
                miniArz.append(whoisDictionary)
                bingDictionary['whoisData'] = miniArz
                rearr.append(bingDictionary)
            except KeyError,RuntimeError:
                pass
    with open('url_list.json','wb') as outfile:
    	json.dump(url_list,outfile,indent=4)
    return jsonify(results=rearr)


@app.route('/api/youtube/<keyword>')
def youtube(keyword):
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

   
if __name__ == '__main__':
    app.run()

