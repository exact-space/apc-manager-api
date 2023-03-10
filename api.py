from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from apcmanagerlmpl import apcManagerApi,json,traceback


app = Flask(__name__)
CORS(app)


@app.route("/apcmanager/unitapc",methods= ["POST"])
def unitapc():
    try:
        if not request.json:
                abort(400)
        
        resObj = request.json
        unitsIdList = resObj["unitsIdList"]
        timeType = resObj["timeType"]
        
        apcApi = apcManagerApi(unitsIdList)
        timeType = apcApi.getValidTimeType(timeType)
        level = "Unit"
        postBody = apcApi.ApcData(timeType,level)
        # print(json.dumps(postBody,indent=4))

        return json.dumps(postBody),200
    except:
         print(traceback.format_exc())
         abort(400)


@app.route("/apcmanager/systemapc",methods= ["POST"])
def systemapc():
    try:
        if not request.json:
                abort(400)
        
        resObj = request.json
        unitsIdList = resObj["unitsIdList"]
        timeType = resObj["timeType"]
        
        apcApi = apcManagerApi(unitsIdList)
        timeType = apcApi.getValidTimeType(timeType)
        level = "System"
        postBody = apcApi.ApcData(timeType,level)
        # print(json.dumps(postBody,indent=4))

        return json.dumps(postBody),200
    except:
         print(traceback.format_exc())
         abort(400)


@app.route("/apcmanager/equipmentapc",methods= ["POST"])
def equipmentapc():
    try:
        if not request.json:
                abort(400)
        
        resObj = request.json
        unitsIdList = ""
        timeType = resObj["timeType"]
        
        apcApi = apcManagerApi(unitsIdList)
        timeType = apcApi.getValidTimeType(timeType)
        level = "Equipment"
        postBody = apcApi.apcDataUsingTagmeta(timeType,resObj)
        # print(json.dumps(postBody,indent=4))

        return json.dumps(postBody),200
    except:
         print(traceback.format_exc())
         abort(400)


@app.route("/apcmanager/individualapc",methods= ["POST"])
def individualapc():
    try:
        if not request.json:
                abort(400)
        
        resObj = request.json
        unitsIdList = ""
        timeType = resObj["timeType"]
        
        apcApi = apcManagerApi(unitsIdList)
        timeType = apcApi.getValidTimeType(timeType)

        postBody = apcApi.apcDataUsingTagmeta(timeType,resObj)
        
        # print(json.dumps(postBody,indent=4))

        return json.dumps(postBody),200
    except:
         print(traceback.format_exc())
         abort(400)



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8081)
  
