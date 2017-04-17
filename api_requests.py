import requests
import json

data = {
	#'username':'biplov',
	'username':'biplovzzzz',
	'password':'123123123vbz'
}
response = requests.post('http://127.0.0.1:6000/api/user/register', data=json.dumps(data)).text
print response