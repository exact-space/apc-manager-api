import requests
import json
import time
sleepTime = 2
baseUrl = "http://10.36.141.34:8082"
baseUrl = "http://10.36.44.48:8082"
apiName = "/apcmanager/unitapc"

wholeUrl = baseUrl + apiName

body = {"unitsIdList":["635b6f9fef6a59000703f924"],"timeType":"daily"}
body = {"unitsIdList":["63349b9c749f3c3081c6a472","635bb88abbf1fe000756dbfb"],"timeType":"daily"}#lpg5
res = requests.post(wholeUrl,json=body).json()
print(res)
if type(res) == list:
    res = res[0]
print("*"*100)
time.sleep(sleepTime)

body.update(res)
apiName = "/apcmanager/systemapc"
# print(body)
wholeUrl = baseUrl + apiName
res = requests.post(wholeUrl,json=body).json()
print(res)
if type(res) == list:
    res = res[0]
print("*"*100)
time.sleep(sleepTime)

body.update(res)
apiName = "/apcmanager/equipmentapc"
# print(body)
wholeUrl = baseUrl + apiName
res = requests.post(wholeUrl,json=body).json()
print(res)
if type(res) == list:
    res = res[0]
print("*"*100)
time.sleep(sleepTime)

body.update(res)

apiName = "/apcmanager/individualapc"
body = {"tagmeta":[{"equipmentName":"Performance Kpi","measureUnit":"%","description":"BfpSystem Total System Apc","dataTagId":"LPG_a472_BfpSystem_1_Total_Power_Ratio","system":"Bfp System","systemName":"Bfp System","unitsId":"63349b9c749f3c3081c6a472","equipment":"Performance Kpi"}],"timeType":"daily"}
# print(body)
wholeUrl = baseUrl + apiName
res = requests.post(wholeUrl,json=body).json()
print(res)
if type(res) == list:
    res = res[0]
time.sleep(sleepTime)
