import requests
import json


data = {'username':'biplov','password':'123123123vb'}
response = requests.post('http://127.0.0.1:5000/api/user/register', data = json.dumps(data)).text
print response