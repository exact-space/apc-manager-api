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
time.sleep(sleepTime)

body.update(res)
apiName = "/apcmanager/systemapc"
# print(body)
wholeUrl = baseUrl + apiName
res = requests.post(wholeUrl,json=body).json()
print(res)
if type(res) == list:
    res = res[0]

time.sleep(sleepTime)

body.update(res)
apiName = "/apcmanager/equipmentapc"
# print(body)
wholeUrl = baseUrl + apiName
res = requests.post(wholeUrl,json=body).json()
print(res)
if type(res) == list:
    res = res[0]
time.sleep(sleepTime)

body.update(res)
exit()

body = {"tagmeta":[{"equipmentName":"Blr-6 Pafan-B","measureUnit":"-/MW","description":"Pa Fan Apc Tph","dataTagId":"HRD_30MKA10CE001.PV_HRD_B6_STM_FT_128AB.DACA.PV_ratio_HRD_B6_STM_FT_128AB.DACA.PV_HRD_f924_Cfbc-6_PaFan_Total_Power_Power_ratio_product","system":"Cfbc","systemName":"Cfbc-6","unitsId":"635b6f9fef6a59000703f924","equipment":"Pa Fan"}],"timeType":"daily"}
body = {"tagmeta":[{"equipmentName":"Unit-3 Cccwp-3","measureUnit":"-/MW","description":"Ccw Pump Apc Tph","dataTagId":"HRD_30MKA10CE001.PV_HRD_f924_CoolingWaterSystem_CcwPump_Total_Power_Power_ratio","system":"Cooling Water System","systemName":"Cooling Water System","unitsId":"635b6f9fef6a59000703f924","equipment":"Ccw Pump"}],"timeType":"daily"}
apiName = "/apcmanager/individualapc"
# print(body)
wholeUrl = baseUrl + apiName
res = requests.post(wholeUrl,json=body).json()
print(res)
if type(res) == list:
    res = res[0]
time.sleep(sleepTime)
