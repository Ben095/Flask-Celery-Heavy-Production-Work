

#str1 = '1.2k'
#print str1.replace('k','000')
bingDictionary = {}
bingDictionary['facebook_shares'] = '12k'
bingDictionary['google_plus_shares'] = '14000'
bingDictionary['linkedin_shares'] = '1.5k'
bingDictionary
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
	total_shares = int(facebook_total.replace('.','') + int(google_plus_shares_total.replace('.','') + int(linkedin_shares_total.replace('.',''))))
	print total_shares

# try:

#     total_shares = int(facebook_total) + int(google_plus_shares_total) + int(linkedin_shares_total)
#     print total_shares
# except:
#     pass




# integer = "1K"
# if "K" in integer:
# 	print integer.replace('K','000')
#url = "https://www.usa.gov//contact-by-topic"
# url = 'https://www.bestpricenutrition.com//contacts/'
# if "//" in url:
# 	first_replace = url.replace('//','/')
# 	second_replace = first_replace.replace('https:/', 'https://').replace('http:/','http://')
# 	print second_replace


#url = 'https://www.bestpricenutrition.com//contacts/'
# url = 'http://www.tdbank.com//investments/private-client-group/investments-insti-trust-contactus.html'
# if "//" in url:
#     split_url = url.split('http')
#     actual_url = split_url[-1].replace('://','').replace('swww','www')
#     first_replace = actual_url.replace('//','/')
#     second_replace = first_replace.replace('https:/', 'https://').replace('http:/','http://')
#     print second_replace
   #	print second_replace

   # worksheet.write_string(row, col+26, str(second_replace))
# split_url = url.split('http')
# print split_url[-1].replace('://','').replace('swww','www')
# URL = '170'
# print URL.replace('K','000')