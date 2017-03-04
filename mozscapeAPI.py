import requests
from mozscape import Mozscape
from itertools import cycle
#arr = []
dictionary = {}

#links, PA, DA, MozRank

dictionary['member-79ea116cb0'] = '43053334ef958fa5668a8afd8018195b'
dictionary['member-89df24f83c'] = '0d08685d31a8f724047decff5e445861'
dictionary['member-aad6e04a94'] = '8a08a4f2477b3eda0a7b3afa8eb6faaf'
dictionary['member-1e51eae111'] = '4f1deaa49d0f4ec8f36778b80a58dba5'
dictionary['member-c1d37816b1'] = '47501159d505413721caac9687818f68'
dictionary['member-700eebf334'] = '0e7136b3468cd832f6dda555aa917661'
dictionary['member-774cfbde7e'] = '481981b24f4a4f08d7c7dc9d5038428f'
dictionary['member-34c9052fba'] = '999d2d727bfc11256421c42c529331de'
dictionary['member-587eb1767c'] = '8c36e3b36b7d6d352fd943429d97837e'
dictionary['member-5fa34d7383'] = '3986edd244ae54e1aa96c71404914578'

## I have more prospect than mozscape

B = ['roc7o.1homevideos.us/dY','egqsz.1homevideo.us/fFf','idioms.thefreedictionary.com/jack','https://mobile.twitter.com/jack','https://www.jack.org','m.youtube.com/watch?v=m0EiujcV3Tg','https://en.wikipedia.org/wiki/TRS_connector','www.jackdaniels.com/en-us/visit-us','www.janieandjack.com','www.magicjack.com','www.urbandictionary.com/define.php?term=Jack','www.harborfreight.com/automotive-motorcycle/floor-jacks.html','https://en.m.wikipedia.org/wiki/Jack_(connector)','m.imdb.com/title/tt3469918']
# client = Mozscape('member-34c9052fba','999d2d727bfc11256421c42c529331de')

# metrics = client.urlMetrics('roc7o.1homevideos.us/dY')
# print metrics
# print metrics
# #print metrics
# # metrics = client.urlMetrics(str(items))
# # #zip_list = zip(B, cycle(dictionary.iteritems()))
d = cycle(dictionary.iteritems())
#print d.next()
for items in B:
	defined = d.next()
	try:
		#print defined[0] + ' ' + defined[1]
# 		#print type(d.next()[1])
		client = Mozscape(defined[0],defined[1])
		metrics = client.urlMetrics(str(items))
		print metrics
# 		print metrics
	except:
		print defined[0] + ' '+ defined[1] + ' ' + items
		# print metrics
# 	#print metrics
# 	except:
# 		pass
	#print d.next()[0]#items, d.next()
	
#	print d
# for items in zip_list:
# 	try:
# 		mozscape_dictionary = {}
# 		client = Mozscape(items[1][0],items[1][1])
# 		metrics = client.urlMetrics(str(items[0]))
# 		mozscape_dictionary['PA'] = metrics['upa']
# 		mozscape_dictionary['DA'] = metrics['pda']
# 		mozscape_dictionary['']
# 	except:
# 		pass
#print zip_list

