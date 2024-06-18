import requests
import json
import time
sleepTime = 4
baseUrl = "http://10.36.141.34:8082"
# baseUrl = "http://10.36.44.48:8082"
baseUrl = "http://10.0.0.14:8082"
baseUrl = "http://127.0.0.1:8082"
apiName = "/apcmanager/unitapc"

wholeUrl = baseUrl + apiName

# body = {"unitsIdList":["63349b9c749f3c3081c6a472","635bb88abbf1fe000756dbfb"],"timeType":"daily"}#lpg5
body = {"unitsIdList":["635b6f9fef6a59000703f924"],"timeType":"daily"}#hrd3
body = {"unitsIdList":["6375e28c32ebf700068ac0aa"],"timeType":"daily"}#hrd3
body = {"unitsIdList":["635219343e4a8c0006f29888","60eb2fab454596520b33e6db","60eb2fb6454596520b33e6dd","60eb2fb2454596520b33e6dc","60eb2fbb454596520b33e6de","5df8f5a57e961b7f0bccc7ed","5ef5104439e8a82281df30bd","63349b9c749f3c3081c6a472","635bb88abbf1fe000756dbfb","5f0ff2f892affe3a28ebb1c2","635b6f9fef6a59000703f924","62d1526a96a4266ef62cc954","628dd242c78e4c5d0f3b90cf","6375e28c32ebf700068ac0aa","6581818964ee3f0007e6c471","60ae9143e284d016d3559dfb","65817c16dcd5de0007bbbf5d"],"timeType":"daily"}

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
# body = {"tagmeta":[{"equipmentName":"Performance Kpi","measureUnit":"%","description":"BfpSystem Total System Apc","dataTagId":"LPG_a472_BfpSystem_1_Total_Power_Ratio","system":"Bfp System","systemName":"Bfp System","unitsId":"63349b9c749f3c3081c6a472","equipment":"Performance Kpi"}],"timeType":"daily"}
# print(body)
wholeUrl = baseUrl + apiName
res = requests.post(wholeUrl,json=body).json()
print(res)
if type(res) == list:
    res = res[0]
time.sleep(sleepTime)
