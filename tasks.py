import requests
from bs4 import BeautifulSoup
import json
#namechange
#ASDASDASDASDASD
# ASDASDASDASDS
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
from youtubescraper import*
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
import urllib
import socket
from bs4 import BeautifulSoup
import re
from urlparse import urljoin, urlparse
from collections import deque
import argparse


socket.setdefaulttimeout(10)
def get_page(url):
    try:
        #print "Requesting url [%s]" % url
        f = urllib.urlopen(url)
        page = f.read()
        f.close()
        return page
    except:
        return ""
    return ""

def parse_page(page):
    #print BeautifulSoup(page)
    return BeautifulSoup(page)


def get_all_valid_links(parsed_page, base_url, domain): 
    links = set()

    # Find all links
    for anchor in parsed_page.find_all('a'):
        anchor_link = anchor.get('href')

        # Only proceed if href was found in anchor tag
        if anchor_link:
            # Uses urljoin to take care of turning
            # relative URLs into absolute ones
            absolute_link = urljoin(base_url, anchor_link)

            parsed_uri = urlparse(absolute_link)
            anchor_netloc = parsed_uri.netloc

            # Only add to list links from same domain
            if anchor_netloc == domain:
                links.add(absolute_link)

    return links

def get_all_emails(page_contents):
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", page_contents, re.I)
    print "EMAILS HERE",emails
    return emails



def crawl_site(seed, domain, max_pages=60):
    to_crawl = deque([seed])
   # crawled = []
    crawled = set()
    #emails_found = set()
    emails_found = []
    all_hrefs_arr = []
    RSS_ARR = []
    bingDictionary = {}
    bingDictionary['facebook_page_url'] = None
    bingDictionary['facebook_page_likes'] = None
    bingDictionary['contact_url'] = None
    bingDictionary['twitter_followers'] = None
    bingDictionary['twitter_page_url'] = None
    bingDictionary['googleplus_followers'] = None
    bingDictionary['google_plus_url'] = None
    bingDictionary['RSS_URL'] = None
    all_phone_numbers_array = []
    while len(to_crawl) and (len(crawled) < max_pages):
        url = to_crawl.popleft()
        crawled.add(url)
        print max_pages
        content = get_page(url)
        #print content
        jacker = get_page(url)
        print jacker
        soup = BeautifulSoup(jacker)
        for link in soup.find_all("link", {"type" : "application/rss+xml"}):
            href = link.get('href')
            RSS_ARR.append(href)
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
        bingDictionary['RSS_URL'] = RSS_ARR
        extractedPhone = phoneRegex.findall(str(soup))
        all_phone_numbers_array = []
        for phone_numbers in extractedPhone:
            all_phone_numbers_array.append(phone_numbers[0])
        bingDictionary['phone_numbers'] = all_phone_numbers_array  
        try:
            a_link = soup.findAll('a')
            for hrefs in a_link:
                all_hrefs_arr.append(hrefs['href'])
          #  print all_hrefs_arr
        except:
            pass
        #
        try:
            for first_items in all_hrefs_arr:
                if "facebook.com" in first_items:
                    bingDictionary['facebook_page_url'] = first_items
                   # emails_found.append(bingDictionary)
        except:
            pass
      
        try:
            for contact_urls in all_hrefs_arr:
                if "contact" in contact_urls:
                    bingDictionary['contact_url'] =  contact_urls
        except:
            pass

        try:
            for second_items in all_hrefs_arr:
                if "twitter.com" in second_items:
                    try:
                        bingDictionary['twitter_page_url'] = second_items
                    except:
                        pass

                    response = requests.get(second_items).text
                    soup = BeautifulSoup(response)
                    twitter_followers = soup.find('span',attrs={'class':'ProfileNav-value'}).text
                    bingDictionary['twitter_followers'] = twitter_followers
                  #  emails_found.append(bingDictionary)
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
                    #emails.append(bingDictionary)
        except:
            pass

        emails_found.append(bingDictionary)

        if content:
            # Parse page
            parsed_page = parse_page(content)
            #print parsed_page(content)
            #print parsed_page.get_text()
            # Extract all emails from page contents and add to list of emails found
            emails_found.append(get_all_emails(parsed_page.get_text()))
           # emails_found.update(get_all_emails(parsed_page.get_text()))

            # Extract valid links and append to crawling queue
            page_links = get_all_valid_links(parsed_page, url, domain)
            try:
                for link in page_links:
                    # Only add links that have not been seen yet
                    if (not link in crawled) and (not link in to_crawl):
                        to_crawl.append(link)
            except:
                pass
    
    return (crawled, emails_found)



def print_set(set_values):
    for item in set_values:
        print item



def make_celery(app):
    celery = Celery(app.import_name, backend='amqp',
                    broker='amqp://')
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='amqp://',
    CELERY_RESULT_BACKEND='amqp'
)
#rearr = []
celery = make_celery(app)
#celery = Celery('tasks', backend='amqp', broker='amqp://')
log = logging.getLogger(__name__)
#app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#from models import InstagramResult, Result, Token
from InstagramAPI import InstagramAPI
#from models import token
class RetryHTTPAdapter(HTTPAdapter):

    SECONDS_BETWEEN_RETRIES = 5

    def __init__(self, retry_time=120, *args, **kwargs):
        self.retry_time = retry_time
        super(RetryHTTPAdapter, self).__init__(*args, **kwargs)

    def send(self, *args, **kwargs):
        for _ in range(int(self.retry_time / self.SECONDS_BETWEEN_RETRIES)):
            response = super(RetryHTTPAdapter, self).send(*args, **kwargs)
            if response.status_code == httplib.OK:
                break
            time.sleep(self.SECONDS_BETWEEN_RETRIES)
        return response

s = requests.Session()
s.mount('http://', RetryHTTPAdapter(retry_time=180))
s.mount('https://', RetryHTTPAdapter(retry_time=180))
from models import*
def igFunction(name):
    try:
        excelArr = []
        dictionary = {}
        #responseID = s.get('https://www.instagram.com/'+str(name)+'/?__a=1')
        response = s.get('https://www.instagram.com/'+str(name)+'/?__a=1').text
        JSON = json.loads(response)
        URL = 'https://www.instagram.com/'+str(name)
        dictionary['url'] = URL
        Username = JSON['user']['username']
        dictionary['username'] = Username
        Name = JSON['user']['full_name']
        dictionary['name'] = Name
        UID = JSON['user']['id']
        dictionary['UID'] = UID
        Followers = JSON['user']['followed_by']['count']
        dictionary['followers'] = Followers
        Following = JSON['user']['follows']['count']
        dictionary['following'] = Following
        Verified = JSON['user']['is_verified']
        dictionary['verified'] = Verified
        Uploads = JSON['user']['media']['count']
        dictionary['uploads'] = Uploads
        Private = JSON['user']['is_private']
        dictionary['private'] = Private
        Bio = JSON['user']['biography']
        dictionary['bio'] = Bio
        URLFIELD = JSON['user']['external_url']
        dictionary['external_url'] = URLFIELD
        dictionary['snapchat'] = "None"
        dictionary['email']=""
        try:
            justTEXT = Bio.encode('ascii','ignore')
            splitJustTEXT = justTEXT.split('\n')
            emails = re.search(r'[\w\.-]+@[\w\.-]+', justTEXT)
            if emails:
                if "." in emails.group()[-1]:
                    new_emails = emails.group()[:-1]
                    email_validator = lepl.apps.rfc3696.Email()
                    if not email_validator(new_emails):
                        pass
                    else:
                        dictionary['email'] = new_emails
                else:               
                    email_string = emails.group()
                    email_validator = lepl.apps.rfc3696.Email()
                    if not email_validator(email_string):
                        pass
                    else:
                        dictionary['email'] = email_string
            for items in splitJustTEXT:
                if "Snapchat" in items:
                    dictionary['snapchat'] = items
                if "Snap" in items:
                    dictionary['snapchat'] = items

                if "SNAPCHAT" in items:
                    dictionary['snapchat'] = items
                if "snap" in items:
                    dictionary['snapchat'] = items

                if "sc" in items:
                    dictionary['snapchat'] = items
                match = re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", items)
                if match:
                        dictionary['email'] = match.group()
                # if dictionary['email'] is None:
                #     match = re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", items)
                   #  if match:
                #       try:
                #          dictionary['email']=match.group().split('')[0]
                #       except:
                #          dictionary['email']=match.group()
        except:
            pass
        
       # print dictionary
        excelArr.append(dictionary)
        return excelArr
    except:
        pass


##make a function that calls InstagramResult -> 
## 


@celery.task()
#@app.route('/instagram/<name>')
def InstagramMain(name):
    with app.app_context():
        try:
            finalData = igFunction(name)
            outputDict = {}
            response = s.get('https://www.instagram.com/'+str(name)+'/?__a=1').text
            JSON = json.loads(response)
            UID = JSON['user']['id']
            ig = InstagramAPI("outreach1998", "4108605$Biplov")
            ig.login()
            main_list = ig.getTotalFollowersID2(UID)
            finalArr = []
            finalOutput = []
            for items in main_list:
                try:
                    username = items['username']
                    print username
                    finalArr.append(igFunction(username))
                except TypeError:
                    pass
            outputDict['self_user_info'] = finalData
            outputDict['each_followers_data'] = finalArr
            finalOutput.append(outputDict)
           #print finalOutput

           #MAJOR CHANGEEE
            output = StringIO.StringIO()
            workbook = xlsxwriter.Workbook(output)
           # workbook = xlsxwriter.Workbook('output.xlsx')
            worksheet = workbook.add_worksheet()
            worksheet.set_column(1, 1, 15)
            bold = workbook.add_format({'bold': 1})
            worksheet.write('A1', 'username', bold)
            worksheet.write('B1', 'bio', bold)
            worksheet.write('C1', 'snapchat', bold)
            worksheet.write('D1', 'verified', bold)
            worksheet.write('E1', 'name', bold)
            worksheet.write('F1', 'url', bold)
            worksheet.write('G1', 'private', bold)
            worksheet.write('H1', 'followers', bold)
            worksheet.write('I1', 'uploads', bold)
            worksheet.write('J1','following',bold)
            worksheet.write('K1', 'external_url', bold)
            worksheet.write('L1', 'email', bold)
            worksheet.write('M1', 'UID', bold)
            row = 1
            col = 0
            with open(name+'.json','wb') as outfile:
                json.dump(finalOutput,outfile,indent=4)
            for items in finalOutput:
                lst1 = items['each_followers_data']
                lst2 = items['self_user_info']
                for second_items in lst2:
                    self_user_info = second_items
                    for mini_s_items in self_user_info:

                            try:
                                worksheet.write_string(row,col,str(self_user_info['username']))
                            except:
                                pass
                            try:
                                worksheet.write_string(row,col+1,str(self_user_info['bio'].encode('ascii','ignore')))
                            except:
                                pass
                            try:
                                worksheet.write_string(row,col+2,str(self_user_info['snapchat']))
                            except:
                                pass
                            try:
                                worksheet.write_string(row,col+3,str(self_user_info['verified']))
                            except:
                                pass
                            try:
                                worksheet.write_string(row+1,col+4, str(self_user_info['name'].encode('ascii','ignore')))
                            except:
                                pass
                            try:
                                worksheet.write_string(row,col+5,str(self_user_info['url']))
                            except:
                                pass
                            try:
                                worksheet.write_string(row,col+6,str(self_user_info['private']))
                            except:
                                pass
                            try:
                                worksheet.write_string(row,col+7,str(self_user_info['followers']))
                            except:
                                pass
                            try:
                                worksheet.write_string(row,col+8,str(self_user_info['uploads']))
                            except:
                                pass
                            try:
                                worksheet.write_string(row,col+9,str(self_user_info['following']))
                            except:
                                pass
                            try:
                                worksheet.write_string(row,col+10,str(self_user_info['external_url']))
                            except:
                                pass
                            try:
                                worksheet.write_string(row,col+11,str(self_user_info['email']))
                            except:
                                pass
                            try:
                                worksheet.write_string(row,col+12,str(self_user_info['UID']))
                            except:
                                pass
                for items in lst1:
                    each_items = items
                    try:
                        for mini_items in each_items:
                                try:
                                    worksheet.write_string(row+1,col,str(mini_items['username']))
                                except:
                                    pass
                                try:
                                    worksheet.write_string(row+1,col+1,str(mini_items['bio'].encode('ascii','ignore')))
                                except:
                                    pass
                                try:
                                    worksheet.write_string(row+1,col+2,str(mini_items['snapchat']))
                                except:
                                    pass
                                try:
                                    worksheet.write_string(row+1,col+3,str(mini_items['verified']))
                                except:
                                    pass
                                try:
                                    worksheet.write_string(row+1,col+4, str(mini_items['name'].encode('ascii','ignore')))
                                except:
                                    pass
                                try:
                                    worksheet.write_string(row+1,col+5,str(mini_items['url']))
                                except:
                                    pass
                                try:
                                    worksheet.write_string(row+1,col+6,str(mini_items['private']))
                                except:
                                    pass 
                                try:
                                    worksheet.write_string(row+1,col+7,str(mini_items['followers']))
                                except:
                                    pass
                                try:
                                    worksheet.write_string(row+1,col+8,str(mini_items['uploads']))
                                except:
                                    pass
                                try:
                                    worksheet.write_string(row+1,col+9,str(mini_items['following']))
                                except:
                                    pass
                                try:
                                    worksheet.write_string(row+1,col+10,str(mini_items['external_url']))
                                except:
                                    pass
                                try:
                                    bio = mini_items['bio'].encode('ascii','ignore')
                                except:
                                    pass
                                try:
                                    bio = mini_items['bio'].encode('ascii','ignore')
                                    emails = re.search(r'[\w\.-]+@[\w\.-]+',bio)
                                    #worksheet.write_string(row+1,col+11,str(mini_items['email']))
                                    if "." in emails.group()[-1]:
                                        new_emails = emails.group()[:-1]
                                        email_validator = lepl.apps.rfc3696.Email()
                                        if not email_validator(new_emails):
                                            pass
                                        else:
                                            worksheet.write_string(row+1,col+11,str(new_emails))
                                    else:               
                                        email_string = emails.group()
                                        email_validator = lepl.apps.rfc3696.Email()
                                        if not email_validator(email_string):
                                            pass
                                        else:
                                            worksheet.write_string(row+1,col+11,str(email_string))
                                except:
                                    pass
                                worksheet.write_string(row+1,col+12,str(mini_items['UID']))
                                row +=1
                    except:
                        pass
            workbook.close()
            output.seek(0)
            response = make_response(output.read())
            response.headers['Content-Disposition'] = "attachment; filename=output.csv"
            return response
        except:
            raise
            #return "TRHEW ERROR OH NO!!!!"


def get_access_token():
    result = Token.query.all()[-1].fb_token
    response = requests.get('https://graph.facebook.com/oauth/access_token?client_id=1803730779944565&client_secret=266970737eaf5570d2e789beeeb6af9c&grant_type=fb_exchange_token&fb_exchange_token='+result).text
    new_access_token = response.split('access_token=')[-1].split('&expires=')[0]
    store_token = Token(fb_token=new_access_token)
    db.session.add(store_token)
    db.session.commit()
    return str(new_access_token)



#get_access_token()

@app.route('/instagram/backend/<name>')
def igbackendWorker(name):
    instagram = InstagramMain.delay(name)
    task_id = instagram.task_id
    add_data = InstagramResult(task_id=task_id,ig_name=name)
    db.session.add(add_data)
    db.session.commit()
    return "Added to queue!"

@app.route('/instagram/<name>/result')
def GenerateResult(name):
    queryName = InstagramResult.query.filter_by(ig_name=name).first()
    task_id = queryName.task_id
  #  v = cache.get('celery-task-%s' % session.get('task_id'))
    # if v:
    #     print v
    res = AsyncResult(task_id)
    if "True" in str(res.ready()):
        return res.get()
    else:
        return "Query is still being processed! Please wait! status:" + str(res.ready())




@app.route('/outreach/results')
def FinalResults():
    with app.app_context():
        queryResults = Result.query.all()
        arr = []
        for items in queryResults:
            dictionary = {}
            dictionary['name'] = items.search_name
            dictionary['task_id'] = items.task_id
            arr.append(dictionary)


        return jsonify(results=arr)

@app.route('/celery/<task_id>/result')
def celeryTaskResult(task_id):
    res = AsyncResult(task_id)
    if "True" in str(res.ready()):
        result_arr = res.get()
        return jsonify(results=result_arr)
    else:
        return "Task is not yet ready!"

@app.route('/youtube/<task_id>/result')
def YoutubeceleryTaskResult(task_id):
    res = AsyncResult(task_id)
    if "True" in str(res.ready()):
        result_arr = res.get()
        return jsonify(results=result_arr)
    else:
        return "Task is not yet ready!"



@app.route('/outreach/<task_id>/result')
def taskResults(task_id):
    with app.app_context():
        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output)
       # workbook = xlsxwriter.Workboowk('output.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column(1, 1, 15)
        bold = workbook.add_format({'bold': 1})
        worksheet.write('A1', 'DA', bold)
        worksheet.write('B1', 'MozRank', bold)
        worksheet.write('C1', 'PA', bold)
        worksheet.write('D1', 'RSS URLS', bold)
        worksheet.write('E1', 'Contact Emails', bold)
        worksheet.write('F1', 'facebook likes', bold)
        worksheet.write('G1', 'facebook url', bold)
        worksheet.write('H1', 'google followers', bold)
        worksheet.write('I1', 'google plus url', bold)
        worksheet.write('J1','meta_title',bold)
        worksheet.write('K1', 'Contact Phone', bold)
        worksheet.write('L1', 'prospect_url', bold)
        worksheet.write('M1', 'root_domain', bold)
        worksheet.write('N1', 'social_shares', bold)
        worksheet.write('O1', 'twitter_followers', bold)
        worksheet.write('P1', 'twitter_url', bold)
        worksheet.write('Q1', 'whois_domain_name', bold)
        worksheet.write('R1', 'whois_city_name', bold)
        worksheet.write('S1', 'whois_country_code', bold)
        worksheet.write('T1', 'whois_email_address', bold)
        worksheet.write('U1', 'whois_full_name', bold)
        worksheet.write('V1', 'whois_phone_number', bold)
        worksheet.write('W1', 'facebook_shares', bold)
        worksheet.write('X1', 'google_plus_shares', bold)
        worksheet.write('Y1', 'linkedin_shares', bold)
        worksheet.write('Z1', 'total_shares', bold)
        worksheet.write('AA1', 'Contact Form', bold)
        row = 1
        col = 0
        res = AsyncResult(task_id)
        if "True" in str(res.ready()):
            result_arr = res.get()
            #get_results = str(result_arr)
            loadAsJson = result_arr
            for each_items in loadAsJson:
                try:
                    worksheet.write_string(row,col,str(each_items['DA']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+1,str(each_items['MozRank']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+2,str(each_items['PA']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+3,str(each_items['RSS_URL'][0]))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+4,str(each_items['emails']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+5,str(each_items['facebook_page_likes']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+6,str(each_items['facebook_page_url']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+7,str(each_items['google_followers']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+8,str(each_items['google_plus_url']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+9,str(each_items['meta_title']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+10,str(each_items['phone_numbers'][0]))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+11,str(each_items['prospect_url']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+12,str(each_items['root_domain']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+13,str(each_items['social_shares']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+14,str(each_items['twitter_followers']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+15,str(each_items['twitter_page_url']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+16,str(each_items['whoisData'][0]['domain_name']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+17,str(each_items['whoisData'][0]['whois_city_name']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+18,str(each_items['whoisData'][0]['whois_country_code']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+19,str(each_items['whoisData'][0]['whois_email_address']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+20,str(each_items['whoisData'][0]['whois_full_name']))
                except:
                    pass
                try:
                    worksheet.write_string(row,col+21,str(each_items['whoisData'][0]['whois_phone_number']))
                except:
                    pass
                try:
                    worksheet.write_string(row, col+22, str(each_items['facebook_shares']))
                except:
                    pass
                try:
                    worksheet.write_string(row, col+23, str(each_items['google_plus_shares']))
                except:
                    pass

                try:
                    worksheet.write_string(row, col+24, str(each_items['linkedin_shares']))
                except:
                    pass
                try:
                    #total_amount_shares = int(each_items['facebook_shares']) + int(each_items['google_plus_shares']) + int(each_items['linkedin_shares'])
                    worksheet.write_string(row, col+25, str(each_items['total_shares']))
                except:
                    pass
                try:
                    worksheet.write_string(row, col+26, str(each_items['contact_url']))
                    # url = each_items['contact_url']
                    # if "//" in url:
                    #     split_url = url.split('http')
                    #     actual_url = split_url[-1].replace('://','').replace('swww','www')
                    #     first_replace = actual_url.replace('//','/')
                    #     second_replace = first_replace.replace('https:/', 'https://').replace('http:/','http://')
                    #     worksheet.write_string(row, col+26, str(second_replace))

                    
                except:
                    pass
                row +=1



            workbook.close()
            output.seek(0)
            response = make_response(output.read())
            response.headers['Content-Disposition'] = "attachment; filename=outreach_output.csv"
            return response
        else:
            return "Query is not yet done processing please wait! status" + str(res.ready())


@celery.task()
#@app.route('/outreach/query/<site>')
def site(site):
    try:
            #domain = bingDictionary['root_domain'].replace('https://','').replace('http://','')
            meta_title_arr = []
            
            
            rearr = []
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
            bingDictionary = {}
            moz_url = site.replace('www.','')
            print moz_url

            response = requests.get('https://moz.com/researchtools/ose/api/urlmetrics?site='+moz_url)
            try:
                json_loader = json.loads(response.text)
                data_loads = json_loader['data']
                authorities = data_loads['authority']
                domain_authority = authorities['domain_authority']
                page_authority = authorities['page_authority']
                links = data_loads['page']['inbound_links']
                bingDictionary['PA'] = page_authority
                bingDictionary['DA'] = domain_authority
                bingDictionary['links'] = links
            except:
                pass
            domain = site
            seed_url = "http://{}/".format(domain)
            maxpages = 30
            email_arrz = []
            crawled, emails_found = crawl_site(seed_url, domain, maxpages)
            emails_arr = emails_found[-1]
            for emails in emails_arr:
                email_validator = lepl.apps.rfc3696.Email()
                if not email_validator(emails):
                    print 'no valid'
                    pass
                else:
                    print "EMAILS HERE", emails
                    email_arrz.append(emails)
                   # email_arr.append(emails.encode('ascii','ignore'))
            token = get_access_token()
            print token

            print "EMAIL ARRAY", email_arrz
            first_items  = emails_found[0]['facebook_page_url']
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
                print response
                bingDictionary['facebook_page_likes'] = response['fan_count']
            except:
                pass
                #pass


            bingDictionary['facebook_page_url'] = emails_found[0]['facebook_page_url']
            bingDictionary['twitter_followers'] = emails_found[0]['twitter_followers']
            bingDictionary['twitter_page_url'] = emails_found[0]['twitter_page_url']
            bingDictionary['google_plus_url'] = emails_found[0]['google_plus_url']
            bingDictionary['googleplus_followers'] = emails_found[0]['googleplus_followers']
            bingDictionary['phone_numbers'] = emails_found[0]['phone_numbers']
            url = emails_found[0]['contact_url']
            try:
                if "//" in url:
                    split_url = url.split('http')
                    actual_url = split_url[-1].replace('://','').replace('swww','www')
                    first_replace = actual_url.replace('//','/')
                    second_replace = first_replace.replace('https:/', 'https://').replace('http:/','http://')
                    bingDictionary['contact_url'] = second_replace
                else:
                    bingDictionary['contact_url'] = site + str(emails_found[0]['contact_url'])
            except:
                bingDictionary['contact_url'] = emails_found[0]['contact_url']
                pass
       
            print "YOOO"
            print bingDictionary['contact_url']
            #bingDictionary['contact_url'] = emails_found[0]['contact_url']
            try:
                if "http:" in bingDictionary['contact_url']:
                    response = requests.get(bingDictionary['contact_url']).text
                    soup = BeautifulSoup(response)
                    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(soup), re.I)
                    for each_emails in emails:
                        print "EACH EMAILS HERE", each_emails

                        email_arrz.append(each_emails)
                else:
                    response = requests.get('http://'+bingDictionary['contact_url']).text
                    soup = BeautifulSoup(response)
                    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(soup), re.I)
                    for each_emails in emails:
                        print "EACH EMAILS HERE", each_emails

                        email_arrz.append(each_emails)
            except:
                pass
            bingDictionary['emails'] = email_arrz

            try:
                if "https://" in str(site):
                    response = requests.get('http://graph.facebook.com/?id='+str(site))
                    print 'Facebookgraph takes time'
                    loadAsJson = json.loads(response.text)
                   # print loadAsJson
                    bingDictionary['facebook_shares'] = loadAsJson['share']['share_count']
                else:
                    print 'http://graph.facebook.com/?id=https://'+str(site)
                    response = requests.get('http://graph.facebook.com/?id=https://'+str(site))
                    print 'Facebookgraph takes time'
                    loadAsJson = json.loads(response.text)
                    bingDictionary['facebook_shares'] = loadAsJson['share']['share_count']

            except:
                bingDictionary['facebook_shares'] = 0
            try:
                if "https://" in str(site):
                    response = requests.get('https://plusone.google.com/_/+1/fastbutton?url='+str(site)).text
                    soup = BeautifulSoup(response)
               
                    follow_count = soup.find('div',attrs={'id':'aggregateCount'}).text
                    bingDictionary['google_plus_shares'] = follow_count
                else:
                    response = requests.get('https://plusone.google.com/_/+1/fastbutton?url=https://'+str(site)).text
                    soup = BeautifulSoup(response)
                    follow_count = soup.find('div',attrs={'id':'aggregateCount'}).text
                    bingDictionary['google_plus_shares'] = follow_count
            except:
                bingDictionary['google_plus_shares'] = 0

            try:
               response = requests.get('https://www.linkedin.com/countserv/count/share?url=https://'+str(site)).text
               #print response
               convert_to_dict = response.replace('IN.Tags.Share.handleCount(','').replace(");",'')
               loadAsJson = json.loads(convert_to_dict)
               bingDictionary['linkedin_shares'] = loadAsJson['count']
            except:
               bingDictionary['linkedin_shares'] = 0
            facebook_total = str(bingDictionary['facebook_shares']).replace('k','000')
            google_plus_shares_total = str(bingDictionary['google_plus_shares']).replace('k','000')
            linkedin_shares_total = str(bingDictionary['linkedin_shares']).replace('k','000')
            if "." in facebook_total:
                facebook_total = facebook_total.replace('000','00')
            if "." in google_plus_shares_total:
                google_plus_shares_total = facebook_total.replace('000','00')
            if "." in linkedin_shares_total:
                linkedin_shares_total = facebook_total.replace('000','00')

            try:
                total_shares = int(facebook_total) + int(google_plus_shares_total) + int(linkedin_shares_total)
              #  print total_shares
            except:
                total_amount_shares = int(facebook_total.replace('.','') + int(google_plus_shares_total.replace('.','') + int(linkedin_shares_total.replace('.',''))))
            bingDictionary['total_shares'] = total_shares
            
            try:
                response = requests.get('http://'+site).text.encode('ascii','ignore')
                #print response
            except:
                pass
                #pass
                #response = requests.get(bingDictionary['root_domain'], verify=False).text
            soup = BeautifulSoup(response)
            
           # RSS_ARR = []
            main_tags = soup.findAll('img')
            meta_title_arr = []
            for alt in main_tags:
                alt = alt.get('alt')
                if alt is None:
                    pass
                else:
                    meta_title_arr.append(alt)
            try:
                bingDictionary['meta_title'] = meta_title_arr[0]
            except:
                bingDictionary['meta_title'] = None   
            formatDomain = str(site).replace(
                                'http://', '').replace('https://', '')
            fixedDomain = formatDomain.split('/')[0].replace('https://www.','').replace('http://www.','').replace('www.','')
            print  "GETS HERE???"
            whoissite = str(site).replace('www.','')
            print "http://104.131.43.184/whois/'"+str(whoissite)
            response = requests.get('http://104.131.43.184/whois/'+str(whoissite)).text
            #print response
            try:
                loadAsJson = json.loads(response)
               # print loadAsJson
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
            return rearr
            #return jsonify(results=rearr)

    except:
        raise


@celery.task()
#@app.route('/outreach/<query>')
def OutReacherDesk(query):
    with app.app_context():
        try:

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
            arr = ['1', '23', '37', '51', '65', '79']
            appendArr = []  
            biggerArr = []
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
                for items in appendArr:
                    biggerArr.append(items)
            except:
                pass
            rearr = []
            with open('output_inspect.json','wb') as outfile:
                json.dump(biggerArr,outfile,indent=4)
            print len(biggerArr)
            d = cycle(m_dictionary.iteritems())
            for items in biggerArr:
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
                        bingDictionary['Links'] = metrics['uid']
                    except: 
                        bingDictionary['PA'] = 0
                        bingDictionary['DA'] = 0
                        bingDictionary['MozRank'] = 0
                        bingDictionary['Links'] = 0
                        
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
                    facebook_total = str(bingDictionary['facebook_shares']).replace('k','000')
                    google_plus_shares_total = str(bingDictionary['google_plus_shares']).replace('k','000')
                    linkedin_shares_total = str(bingDictionary['linkedin_shares']).replace('k','000')
                    if "." in facebook_total:
                        facebook_total = facebook_total.replace('000','00')
                    if "." in google_plus_shares_total:
                        google_plus_shares_total = facebook_total.replace('000','00')
                    if "." in linkedin_shares_total:
                        linkedin_shares_total = facebook_total.replace('000','00')

                    try:
                        total_shares = int(facebook_total) + int(google_plus_shares_total) + int(linkedin_shares_total)
                        print total_shares
                    except:
                        total_amount_shares = int(facebook_total.replace('.','') + int(google_plus_shares_total.replace('.','') + int(linkedin_shares_total.replace('.',''))))
                    bingDictionary['total_shares'] = total_shares
                    bingDictionary['meta_title'] = eachQueryString[
                                        'shortTitle'].encode('ascii', 'ignore')
                    url = urlparse(eachQueryString['url'])
                    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=url)
                    bingDictionary['root_domain'] = domain
                    try:
                        response = requests.get(bingDictionary['root_domain']).text
                    except:
                        pass
                        #response = requests.get(bingDictionary['root_domain'], verify=False).text
                    email_arrz = []
                   # domain = bingDictionary['root_domain']

                    seed_url = "http://{}/".format(domain)
                    maxpages = 30
                    domain = bingDictionary['root_domain'].replace('https://','').replace('http://','')
                    seed_url = "http://{}/".format(domain)
                    print domain, seed_url
                    crawled, emails_found = crawl_site(seed_url, domain, maxpages)

                    emails_arr = emails_found[-1]
                    for emails in emails_arr:
                        email_validator = lepl.apps.rfc3696.Email()
                        if not email_validator(emails):
                            print 'no valid'
                            pass
                        else:
                            print "EMAILS HERE", emails
                            email_arrz.append(emails)
                    bingDictionary['emails'] = email_arrz
                    token = get_access_token()
                    first_items  = emails_found[0]['facebook_page_url']
                    try:
                        split_first = first_items.split('.com/')
                        facebook_group_name = split_first[-1].replace('/','')
                        response = requests.get('https://graph.facebook.com/v2.8/search?q='+facebook_group_name+'&type=page&access_token='+token).text
                        jsonLoads = json.loads(response)
                        arr = jsonLoads['data']
                        first_item_in_query = arr[0]['id']
                        response = requests.get('https://graph.facebook.com/v2.8/'+first_item_in_query+'/?fields=fan_count&access_token='+token).json()
                        bingDictionary['facebook_page_likes'] = response['fan_count']
                        print bingDictionary['facebook_page_likes']
                    except:
                        pass
                    bingDictionary['facebook_page_url'] = emails_found[0]['facebook_page_url']
                    bingDictionary['twitter_followers'] = emails_found[0]['twitter_followers']
                    bingDictionary['twitter_page_url'] = emails_found[0]['twitter_page_url']
                    bingDictionary['google_plus_url'] = emails_found[0]['google_plus_url']
                    bingDictionary['googleplus_followers'] = emails_found[0]['googleplus_followers']
                    bingDictionary['phone_numbers'] = emails_found[0]['phone_numbers']
                    bingDictionary['contact_url'] = emails_found[0]['contact_url']
                    url = emails_found[0]['contact_url']
                    try:
                        if "//" in url:
                            split_url = url.split('http')
                            actual_url = split_url[-1].replace('://','').replace('swww','www')
                            first_replace = actual_url.replace('//','/')
                            second_replace = first_replace.replace('https:/', 'https://').replace('http:/','http://')
                            bingDictionary['contact_url'] = second_replace
                        else:
                            bingDictionary['contact_url'] = site + str(emails_found[0]['contact_url'])
                    except:
                        bingDictionary['contact_url'] = emails_found[0]['contact_url']
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

            return rearr
            

        except:
            raise
@app.route('/outreach/backend/<query>')
def backendWorker(query):
    with app.app_context():
        convert_to_str = str(query)
        outreach = OutReacherDesk.delay(convert_to_str)
        task_id = outreach.task_id
        user = Result(task_id=task_id, username='Jack', search_name=query)
        db.session.add(user)
        db.session.commit()
        return "Added to queue!"

@celery.task()
#@app.route('/outreach/youtube/<keyword>')
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

    return finalArr


@app.route('/outreach/youtube/<keyword>')
def YoutubeWorker(keyword):
    with app.app_context():
        convert_to_str = str(keyword)
        youtube_task_id = youtube.delay(convert_to_str)
        task_id = youtube_task_id.task_id
        user = Result(task_id=task_id, username='Jack', search_name=convert_to_str)
        db.session.add(user)
        db.session.commit()
        return "Youtube added to queue"



@app.route('/outreach/celery/<query>')
def individualWorker(query):
    with app.app_context():
        convert_to_str = str(query)
        outreach = site.delay(query)
        task_id = outreach.task_id
        user = Result(task_id=task_id, username='Jack', search_name=query)
        db.session.add(user)
        db.session.commit()
        return "Added to queue"
    


if __name__ == '__main__':
    app.run()