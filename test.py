import requests 
from test_db import DATABASE_TMP

BASE="http://127.0.0.1:5000/"


for i in range(len(DATABASE_TMP)):
        response = requests.put(BASE + "ip/" + str(i), DATABASE_TMP[i])
        print(response.json())

input()
response = requests.delete(BASE + "ip/0")
print(response)
input()
response = requests.get(BASE + "ip/1")
print(response.json())