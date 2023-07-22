import requests
import json
import time
baseUrl = "http://10.36.141.34:8082"
apiName = "/apcmanager/unitapc"

wholeUrl = baseUrl + apiName
body = {"unitsIdList":["635b6f9fef6a59000703f924"],"timeType":"daily"}
res = requests.post(wholeUrl,json=body).json()
print(res)
if type(res) == list:
    res = res[0]
time.sleep(10)
body.update(res)
apiName = "/apcmanager/systemapc"
print(body)
wholeUrl = baseUrl + apiName
res = requests.post(wholeUrl,json=body).json()

if type(res) == list:
    res = res[0]
time.sleep(10)
body.update(res)
apiName = "/apcmanager/equipmentapc"
print(body)
wholeUrl = baseUrl + apiName
res = requests.post(wholeUrl,json=body).json()