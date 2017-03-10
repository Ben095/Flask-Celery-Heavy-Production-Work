bingDictionary = {}
bingDictionary['root_domain'] = 'http://www.dillards.com/'
domain = bingDictionary['root_domain'].replace('https://','').replace('http://','')
print domain.replace('/','')