import requests
import json

baseUrl = "http://10.36.141.34:8082"
apiName = "/apcmanager/unitapc"

wholeUrl = baseUrl + apiName
body = {"unitsIdList"}