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
from flask import Flask, abort, request, jsonify, g, url_for, current_app
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from flask import make_response
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
import requests
from mozscape import Mozscape
from itertools import cycle
import stripe
from firebase import firebase
# from pyfcm import FCMNotification
import json
import time
# from youtubescraper import*
import grequests
from grequests import*
from functools import partial

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

print "GOT STARTED!"





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
query = 'loans'
for i in arr:
    response = requests.get('https://c.bingapis.com/api/custom/opal/otherpage/search?q=' + str(
        query) + '&first=' + str(i) + '&rnoreward=1', headers=headers).text
    LoadAsJson = json.loads(response)
    print LoadAsJson
    with open('check_thisoutput.json','wb') as outfile:
        json.dump(LoadAsJson,outfile,indent=4)
    actualItem = LoadAsJson['answers'][0]['webResults']
    appendArr.append(actualItem)
try:
    biggerArr.append(appendArr[0]+appendArr[1])
except:
    pass
rearr = []
print len(biggerArr)
d = cycle(m_dictionary.iteritems())
for items in biggerArr[:2]:
    eachQuery = items
    domainArray = []
    eachPageWhoisResult = []
    async_list = []
    url_list = []
    for eachQueryString in eachQuery:
    	bingDictionary = {}

        bingDictionary['prospect_url'] = eachQueryString[
            'displayUrl']
        try:
            defined = d.next()
            client = Mozscape(str(defined[0]),str(defined[1]))

            mozscape_dictionary = {}
            metrics = client.urlMetrics(str(bingDictionary['prospect_url']))
            bingDictionary['PA'] = metrics['upa']
            bingDictionary['DA'] = metrics['pda']
            bingDictionary['MozRank'] = metrics['ut']
        except: 
            bingDictionary['PA'] = 0
            bingDictionary['DA'] = 0
            bingDictionary['MozRank'] = 0
            pass
        try:
            if "https://" in str(bingDictionary['prospect_url']):
                response = requests.get('http://graph.facebook.com/?id='+str(eachQueryString['displayUrl']))
                print 'Facebookgraph takes time'
                loadAsJson = json.loads(response.text)
               # print loadAsJson
                bingDictionary['facebook_shares'] = loadAsJson['share']['share_count']
            else:
                print 'http://graph.facebook.com/?id=https://'+str(eachQueryString['displayUrl'])
                response = requests.get('http://graph.facebook.com/?id=https://'+str(eachQueryString['displayUrl']))
                print 'Facebookgraph takes time'
                loadAsJson = json.loads(response.text)
                bingDictionary['facebook_shares'] = loadAsJson['share']['share_count']

        except:
            bingDictionary['facebook_shares'] = 0
        try:
            if "https://" in str(bingDictionary['prospect_url']):
                response = requests.get('https://plusone.google.com/_/+1/fastbutton?url='+str(bingDictionary['prospect_url'])).text
                soup = BeautifulSoup(response)
           
                follow_count = soup.find('div',attrs={'id':'aggregateCount'}).text
                bingDictionary['google_plus_shares'] = follow_count
            else:
                response = requests.get('https://plusone.google.com/_/+1/fastbutton?url=https://'+str(bingDictionary['prospect_url'])).text
                soup = BeautifulSoup(response)
                follow_count = soup.find('div',attrs={'id':'aggregateCount'}).text
                bingDictionary['google_plus_shares'] = follow_count
        except:
            bingDictionary['google_plus_shares'] = 0

        try:
           response = requests.get('https://www.linkedin.com/countserv/count/share?url=https://'+str(bingDictionary['prospect_url'])).text
           #print response
           convert_to_dict = response.replace('IN.Tags.Share.handleCount(','').replace(");",'')
           loadAsJson = json.loads(convert_to_dict)
           bingDictionary['linkedin_shares'] = loadAsJson['count']
        except:
           # raise
           bingDictionary['linkedin_shares'] = 0

        facebook_total = bingDictionary['facebook_shares']
        google_plus_shares_total = bingDictionary['google_plus_shares']
        linkedin_shares_total = bingDictionary['linkedin_shares']
        total_shares = int(facebook_total) + int(google_plus_shares_total) + int(linkedin_shares_total)
        bingDictionary['total_shares'] = total_shares
       	bingDictionary['meta_title'] = eachQueryString[
                            'shortTitle'].encode('ascii', 'ignore')
        url = urlparse(eachQueryString['url'])
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=url)
        bingDictionary['root_domain'] = domain
        response = requests.get(bingDictionary['root_domain']).text
        soup = BeautifulSoup(response)
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
        RSS_ARR = []
        extractedPhone = phoneRegex.findall(str(soup))
        all_phone_numbers_array = []
        for phone_numbers in extractedPhone:
            all_phone_numbers_array.append(phone_numbers[0])
        bingDictionary['phone_numbers'] = all_phone_numbers_array
        for link in soup.find_all("link", {"type" : "application/rss+xml"}):
            href = link.get('href')
            RSS_ARR.append(href)
        bingDictionary['RSS_URL'] = RSS_ARR
        a = soup.findAll('a')

        all_hrefs_arr = []
        for items in a:
            try:
                all_hrefs_arr.append(items['href'])

            except:
                pass
        bingDictionary['facebook_page_url'] = "No url found!"
        bingDictionary['facebook_page_likes'] = 0
        bingDictionary['twitter_page_url'] = "No url found!"
        bingDictionary['twitter_followers'] = 0
        bingDictionary['google_plus_followers'] = 0
        bingDictionary['google_plus_url'] = "No url found!"
        bingDictionary['contact_url'] = "No url found!"
        email_arr = []
        emails = re.search(r"^[a-zA-Z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",str(soup))
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
        try:
            for contact_urls in all_hrefs_arr:
                if "contact" in contact_urls:
                    bingDictionary['contact_url'] = bingDictionary['root_domain'] + contact_urls
        except:
            pass
        try:
            for first_items in all_hrefs_arr:
                if "facebook.com" in first_items:
                    response = requests.get(first_items).text
                    soup = BeautifulSoup(response)
                    likes = soup.find('span',attrs={'class':'_52id _50f5 _50f7'}).text.replace('likes','')
                    bingDictionary['facebook_page_likes'] = likes
                    bingDictionary['facebook_page_url'] = first_items
        except:
            pass

        try:
            for second_items in all_hrefs_arr:
                if "twitter.com" in second_items:
                    
                    response = requests.get(second_items).text
                    soup = BeautifulSoup(response)
                    twitter_followers = soup.find('span',attrs={'class':'ProfileNav-value'}).text

                    bingDictionary['twitter_followers'] = twitter_followers
                    bingDictionary['twitter_page_url'] = second_items
        except:
            pass

        try:
            for third_items in all_hrefs_arr:
                if "plus.google.com" in third_items:
                    response = requests.get(third_items).text
                    soup = BeautifulSoup(response)
                    googleplus_followers = soup.find('div',attrs={'class':"C98T8d GseqId b12n5"}).text.split('-')[0].replace('followers','')
                    bingDictionary['google_plus_followers'] = googleplus_followers
                    bingDictionary['google_plus_url'] = third_items
        except:
            pass

        formatDomain = str(domain).replace(
                            'http://', '').replace('https://', '')
        fixedDomain = formatDomain.split('/')[0].replace('https://www.','').replace('http://www.','').replace('www.','')
        response = requests.get('http://104.131.43.184/whois/'+str(fixedDomain)).text
        try:
            loadAsJson = json.loads(response)
        except:
            pass
        miniArray = []
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
        miniArray.append(whoisDictionary)
        bingDictionary['whoisData'] = miniArray
        rearr.append(bingDictionary)

with open('final_version_data.json','wb') as outfile:
    json.dump(rearr,outfile,indent=4)
        
        # bingDictionary['whoisData'] = "None"
        # miniArz = []
        # try:
        #     response = requests.get('http://104.131.43.184/whois/'+str(fixedDomain)).text
        #     print response
        #    # print "WHOIS TIMER..."
        #     #min_text = 'http://104.131.43.184/whois/'+str(fixedDomain)
        #     #url_list.append(str(min_text))
        #     #loadAsJson = json.loads(response)
        # except:
        #     pass
        #a_link = soup.findAll('a')
        # try:
        #     for each_url_in_webpage in a_link:
        #         if "facebook.com" in each_url_in_webpage['href']:
        #             bingDictionary['facebook_page_url'] = each_url_in_webpage['href']
        #         else:
        #             bingDictionary['facebook_page_url'] = "bleh"
        # except:
        #     pass

        # print bingDictionary