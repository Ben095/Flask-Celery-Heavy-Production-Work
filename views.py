import requests,json
from bs4 import BeautifulSoup
from urlparse import urlparse
from mozscape import Mozscape, MozscapeError
from time import sleep
from itertools import cycle
import dryscrape
from flask import*
from time import sleep
from forms import QueryGoogle
from models import*

app = Flask(__name__)
app.secret_key = '1234'
db.create_all()
headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:27.0) Gecko/20100101 Firefox/27.0',
	'Cookie':'NID=89=Xx6qVlFq5MyhJC5y4-duwh50KFDhMFDVNUHpAX63aQs1J77jswVAUv1nrxu8ekuZjs9SGvA31VnN5O3wS1b4HQrBDDRKyMgERDrGbr2oWaBps46rBvepRIX5rKTqJJq1BN4ARj2ErQ2jAA; DV=wkE1gHCYxTAcLEWZLaMIXfRxgbYxsAI',
	'X-Firefox-Spdy':'3.1',
	'Host':'www.google.com',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

@app.route('/', methods=['GET','POST'])
def querygoogle():
	form = QueryGoogle(request.form)
	index = 0
	biggestArr = []
	if form.validate_on_submit():
		arr = GoogleQuery(form.QueryGoogle.data)
		print "Getting Moz Data!"
		MozscapeData(form.QueryGoogle.data)
		print "Collecting facebook data!"
		FacebookScraper(form.QueryGoogle.data)
		print "Collecting google plus data!"
		scrapeGooglePlus(form.QueryGoogle.data)
		return render_template('google.html', form=form, arr=arr)
	return render_template('google.html',form=form)


def MozscapeData(query):
	urls = Google.query.filter_by(googleQuery=query).all()
	A = []
	Mozarr = []
	for items in urls:
		mozMiniDict = {}
		mozMiniDict['full_url'] = items.googleFullURL
		mozMiniDict['root_domain'] = items.googleRootDomain
		A.append(mozMiniDict)
	listO = open('credentials.json')
	B = json.load(listO)
	for zipList in zip(A, cycle(B)):
		try:
			client = Mozscape(zipList[-1]['key'], zipList[-1]['value'])
			authorities = client.urlMetrics(str(zipList[0]['root_domain']), Mozscape.UMCols.domainAuthority)
			Links = client.urlMetrics(str(zipList[0]['full_url']),Mozscape.UMCols.pageAuthority | Mozscape.UMCols.mozRank | Mozscape.UMCols.links)
			internal_dictionary = {}
			internal_dictionary['root_domain'] = zipList[0]['root_domain']
			internal_dictionary['backURL'] = zipList[0]['full_url']
			internal_dictionary['PA'] = Links['upa']
			internal_dictionary['DA'] = authorities['pda']
			internal_dictionary['MozRank'] = Links['umrp']
			internal_dictionary['links'] = Links['uid']
			Mozarr.append(internal_dictionary)
		except MozscapeError:
			print "Moz threw error!"
			sleep(11)
			continue

	for updateMoz in Mozarr:
		update = Google.query.filter_by(googleRootDomain=updateMoz['root_domain']).first()
		update.Links = updateMoz['links']
		update.PA = updateMoz['PA']
		update.DA = updateMoz['DA']
		update.moz_rank = updateMoz['MozRank']
		db.session.commit()

def GoogleQuery(query):
    #################-------QUERIES GOOGLE FIRST STEP-------------######### Gets 10 results.
    ### ON QUERY NO TIMER NEEDED##########
    ### GoogleQuery() function returns an array of dictionary with crucial information
    ### Save google data in database (FIRST STEP!!!!!) #######

	arr = []
	index = 0
	response = requests.get('https://www.google.com/search?num=3&q='+str(query)+'&oq='+str(query)+'&&start=10',headers=headers).text
	soup = BeautifulSoup(response)
	print soup
	title = soup.findAll('div',attrs={'class':'g'})
	for titles in title:
		try:
			dictionary = {}
			index +=1
			dictionary['index#'] = str(index) 
			dictionary['meta_title'] = titles.find('h3').text
			dictionary['full_url'] = titles.find('a')['href']
			rootDomain = dictionary['full_url'].replace('/url?q=','')
			parsed_uri = urlparse(rootDomain)
			dictionary['rootDomain'] = rootDomain
			domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
			dictionary['root_domain'] = domain
			dictionary['description'] = titles.find('span',attrs={'class':'st'}).text
			arr.append(dictionary)
		except AttributeError:
			continue

	for items in arr:
		addItem = Google(googleQuery = query, googleMetaTitle = items['meta_title'], googleFullURL=items['full_url'],googleRootDomain=items['root_domain'])
		db.session.add(addItem)
		db.session.commit()
	return arr

def FacebookData(query):
	arr = Google.query.filter_by(googleQuery=query).all()
	facebookURLAdditionalData = []
	for items in arr:
		updateTable = Google.query.filter_by(googleRootDomain=items.googleRootDomain).first()
		sleep(5)
		URLS = items.googleRootDomain
		facebookCount = requests.get('http://graph.facebook.com/?id='+URLS).text
		jsonObj = json.loads(facebookCount)
		count = jsonObj['share']
		updateTable.facebook_shares = count['share_count']
		db.session.commit()
		print 'https://www.google.com/search?num=1&q=site:facebook.com '+URLS+'&&start=10'
		response = requests.get('https://www.google.com/search?num=1&q=site:facebook.com '+URLS,headers=headers).text
		soup = BeautifulSoup(response)
		title = soup.findAll('div',attrs={'class':'g'})
		for titles in title:
			dictionary = {}
			dictionary['meta_title'] = titles.find('h3').text
			dictionary['full_url'] = titles.find('a')['href']
			rootDomain = dictionary['full_url'].replace('/url?q=','')
			parsed_uri = urlparse(rootDomain)
			dictionary['rootDomain'] = rootDomain
			dictionary['actualrootDomain'] = items.googleRootDomain
			print "ROOT DOMAIN!", items.googleRootDomain
			parseGroupURL = dictionary['rootDomain'].split('&sa')[0]
			groupURL = parseGroupURL.replace('%3F','?').replace('%3D','=')
			dictionary['groupURL'] = groupURL
			facebookURLAdditionalData.append(dictionary)
	return facebookURLAdditionalData

def FacebookScraper(query):  
	arr = []
	DataList = FacebookData(query)
	for items in DataList:
			dictionary = {}
			response = requests.get(items['groupURL']).text
			soup = BeautifulSoup(response)
			try:
				likes = soup.find('div',attrs={'class':'_4-u2 _5tsm _4-u8'}).text
			except AttributeError:
				continue
			dictionary['facebook_profile_url'] = items['groupURL']
			dictionary['facebook_profile_likes'] = likes.encode('ascii','ignore').strip()
			dictionary['rootDomain'] = items['actualrootDomain']
			print dictionary
			arr.append(dictionary)
			with open(query+'.json','wb') as outfile:
				json.dump(arr,outfile,indent=4)

	for updateFacebookData in arr:
		updateTable = Google.query.filter_by(googleRootDomain=updateFacebookData['rootDomain']).first()
		updateTable.facebook_c_url = updateFacebookData['facebook_profile_url']
		updateTable.facebook_c_likes = updateFacebookData['facebook_profile_likes']
		db.session.commit()
		print "Added facebook profile/likes!"
	
def GooglePlusData(query):
	arr = Google.query.filter_by(googleQuery=query).all()
	googleAdditionalData = []
	for items in arr:
		updateTable = Google.query.filter_by(googleRootDomain=items.googleRootDomain).first()
		URLS = items.googleRootDomain
		TwitterCount = requests.get('https://plusone.google.com/_/+1/fastbutton?url='+items.googleRootDomain,headers=headers).text
		soup = BeautifulSoup(TwitterCount)
		try:
			print "Added google shares!"
			googleCount = soup.find('div',attrs={'id':'aggregateCount'}).text
			updateTable.google_shares = googleCount
			db.session.commit()
		except AttributeError:
			pass
		sleep(5)
		response = requests.get('https://www.google.com/search?num=1&q=site:plus.google.com+'+str(URLS),headers=headers).text
		soup = BeautifulSoup(response)
		title = soup.findAll('div',attrs={'class':'g'})
		for titles in title:
			dictionary = {}
			dictionary['actual_root_domain'] = items.googleRootDomain
			dictionary['meta_title'] = titles.find('h3').text
			dictionary['full_url'] = titles.find('a')['href']
			rootDomain = dictionary['full_url'].replace('/url?q=','')
			parsed_uri = urlparse(rootDomain)
			dictionary['rootDomain'] = rootDomain
			dictionary['googleURLpage'] = dictionary['rootDomain'].split('&')[0]
			googleAdditionalData.append(dictionary)
	return googleAdditionalData

def scrapeGooglePlus(query):
	googlePlusArr = []
	arr = GooglePlusData(query)
	for visitFacebookPage in arr:
		dictionary = {}
		response = requests.get(visitFacebookPage['googleURLpage']).text
		soup = BeautifulSoup(response)
		dictionary['updaterootDomain'] = visitFacebookPage['actualrootDomain']
		try:
			dictionary['googleplus_followers'] = soup.find('span',attrs={'class':'BOfSxb'}).text
		except AttributeError:
			continue
		dictionary['googleplus_uRL'] = visitFacebookPage
		googlePlusArr.append(dictionary)

	for updategplusData in googlePlusArr:
		updateTable = Google.query.filter_by(googleRootDomain=updategplusData['updaterootDomain']).first()
		updateTable.facebook_c_url = updategplusData['googleplus_uRL']
		updateTable.facebook_c_likes = updategplusData['googleplus_followers']
		db.session.commit()
		print "Added google plus! profile/likes!"
	

if __name__ == "__main__":
	db.create_all()
	app.run(debug=True, port=9000)


