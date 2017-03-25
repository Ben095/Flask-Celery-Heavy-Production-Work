import urllib
import requests
import shutil
import os
import deathbycaptcha

s = 0
headers = 0

def solveCaptcha(challenge):
	# Put your DBC account username and password here.
    # Use deathbycaptcha.HttpClient for HTTP API.

	username = "onlinemarketingjuice"
	password = "R6ZeMYxZgY3O"
	captcha_file_name = challenge + ".png"
	timeout = 99

	client = deathbycaptcha.SocketClient(username, password)
	try:
		balance = client.get_balance()

		# Put your CAPTCHA file name or file-like object, and optional
		# solving timeout (in seconds) here:
		captcha = client.decode(captcha_file_name, timeout)
		if captcha:
			return captcha["text"]
	except deathbycaptcha.AccessDeniedException:
	    # Access to DBC API denied, check your credentials and/or balance
	    #print "error with death by captcha"
	    return "failed"

def getCaptcha(challenge):

	response = solveCaptcha(challenge)
	os.remove(challenge + ".png")

	return response