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
    # parse_page_arr = []
    # soup = BeautifulSoup(page)
    # a_link = soup.findAll('a')
    # for items in a_link:
    #     for first_items in all_hrefs_arr:
                    
    #     print items['href']
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


def get_all_emails(page_contents):

    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", page_contents, re.I)
    return emails

def crawl_site(seed, domain, max_pages=10):
    to_crawl = deque([seed])
   # crawled = []
    crawled = set()
    #emails_found = set()
    emails_found = []
    all_hrefs_arr = []
    bingDictionary = {}
    while len(to_crawl) and (len(crawled) < max_pages):
        url = to_crawl.popleft()
        crawled.add(url)
        

        content = get_page(url)
        jacker = get_page(url)
        soup = BeautifulSoup(jacker)
        try:
            a_link = soup.findAll('a')
            for hrefs in a_link:
                all_hrefs_arr.append(hrefs['href'])
          #  print all_hrefs_arr
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
                   # emails_found.append(bingDictionary)
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
                   # emails_found.append(bingDictionary)
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
                  #  emails.append(bingDictionary)
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
        return item


domain = 'www.mymakeupbrushset.com'
seed_url = "http://{}/".format(domain)
maxpages = 1       

crawled, emails_found = crawl_site(seed_url, domain, maxpages)
for items in emails_found:
    print items
# email = emails_found[-1]
# #print email
# for items in email:
#     print items