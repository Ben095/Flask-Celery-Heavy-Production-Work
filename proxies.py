import random

random_port = random.randint(6000,6249)
proxies = {
		"https" : "socks5://jackfitzdomains:jackfitz@37.58.52.8:" + str(random_port),
	}


def random_proxy():
	return proxies