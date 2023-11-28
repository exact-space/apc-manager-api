from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from apcmanagerlmpl import apcManagerApi,json,traceback


app = Flask(__name__)
CORS(app)

quries = {
    "pafan": [
        {
            "measureProperty": "Primary Air",
            "measureType": "Flow",
            "equipment": "Pa Fan"
        },
        {
            "measureProperty": "Bed",
            "measureType": "Level",
            "equipment": "Furnace"
        },
        {
            "measureProperty": "Feed Water",
            "measureType": "Differential Pressure",
            "equipment": "Economizer"
        },
        {
            "measureProperty": "Flue Gas",
            "measureType": "O2",
            "equipment": "Air Preheater"
        }
    ],
    "fdfan": [
        {
            "measureProperty": "Feed Water",
            "measureType": "Differential Pressure",
            "equipment": "Economizer"
        },
        {
            "measureProperty": "Secondary Air",
            "measureType": "Flow",
            "equipment": "Fd Fan"
        },
        {
            "measureProperty": "Secondary Air",
            "measureType": "Pressure",
            "equipment": "Fd Fan"
        },
        {
            "measureProperty": "Flue Gas",
            "measureType": "O2",
            "equipment": "Air Preheater"
        }
    ],
    "safan": [
        {
            "measureProperty": "Feed Water",
            "measureType": "Differential Pressure",
            "equipment": "Economizer"
        },
        {
            "measureProperty": "Secondary Air",
            "measureType": "Flow",
            "equipment": "Sa Fan"
        },
        {
            "measureProperty": "Secondary Air",
            "measureType": "Pressure",
            "equipment": "Sa Fan"
        },
        {
            "measureProperty": "Flue Gas",
            "measureType": "O2",
            "equipment": "Air Preheater"
        }
    ],
    "idfan": [
        {
            "measureProperty": "Flue Gas",
            "measureType": "O2",
            "equipment": "Air Preheater"
        },
        {
            "measureProperty": "Furnace",
            "measureType": "Pressure",
            "equipment": "Furnace"
        },
        {
            "measureProperty": "Air",
            "measureType": "Ingress Constant",
            "equipment": "Performance Kpi"
        },
        {
            "measureType": "Temperature",
            "equipment": "Id Fan",
            "measureLocation": "Inlet"
        }
    ],
    "pulverizer": [
        {
            "measureProperty": "Fuel",
            "measureType": "Flow",
            "equipment": "Pulverizer"
        },
        {
            "measureProperty": "Primary Air",
            "measureType": "Flow",
            "equipment": "Pulverizer"
        }
    ],
    "generator": [
        {
            "measureProperty": "Power",
            "measureType": "Current",
            "equipment": "Generator"
        }
    ]
}



@app.route("/apcmanager/unitapc",methods= ["POST"])
def unitapc():
    try:
        global perc
        if not request.json:
                abort(400)
        
        resObj = request.json
        unitsIdList = resObj["unitsIdList"]
        timeType = resObj["timeType"].lower()
        
        apcApi = apcManagerApi(unitsIdList)
        timeType = apcApi.getValidTimeType(timeType)
        level = "Unit"
        
        for unitsId in unitsIdList:
            msfQuery = {
                    "unitsId" : unitsId,
                    "measureInstance" : 1,
                    "equipment" : "Final Superheater",
                    "measureType" : "Flow",
                    "measureProperty" : "Main Steam"
                }
                        
            msf = apcApi.getTagMeta(msfQuery)
            if len(msf) > 1:
                 perc = False
                 break
            perc = True
        if perc:
            print("using percentages...")
            postBody = apcApi.ApcDataPerc(timeType,level,"Sum")

        else:
            print("Not using percentages...")
            
            postBody = apcApi.ApcData(timeType,level,"Sum")

        # print(json.dumps(postBody,indent=4))

        return json.dumps(postBody),200
    except:
         print(traceback.format_exc())
         abort(400)


@app.route("/apcmanager/systemapc",methods= ["POST"])
def systemapc():
    try:
        global perc
        if not request.json:
                abort(400)
        
        try:
             perc
        except:
             perc = False
             
        resObj = request.json
        unitsIdList = resObj["unitsIdList"]
        timeType = resObj["timeType"].lower()
        
        apcApi = apcManagerApi(unitsIdList)
        timeType = apcApi.getValidTimeType(timeType)
        level = "System"
        if perc:
            print("using percentages...")
            postBody = apcApi.ApcDataPerc(timeType,level,"Sum")

        else:
            print("Not using percentages...")
            
            postBody = apcApi.ApcData(timeType,level,"Sum")
        # print(json.dumps(postBody,indent=4))

        return json.dumps(postBody),200
    except:
         print(traceback.format_exc())
         abort(400)


@app.route("/apcmanager/equipmentapc",methods= ["POST"])
def equipmentapc():
    try:
        global perc
        if not request.json:
                abort(400)

        try:
             perc
        except:
             perc = False
        
        resObj = request.json
        unitsIdList = ""
        timeType = resObj["timeType"].lower()
        
        apcApi = apcManagerApi(unitsIdList)
        timeType = apcApi.getValidTimeType(timeType)
        level = "Equipment"
        if not perc:
            print("Not using perc...")
            postBody = apcApi.apcDataUsingTagmeta(timeType,resObj)
        else:
            print("using perc...")
            postBody = apcApi.apcDataUsingTagmetaPerc(timeType,resObj)
             
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
        timeType = resObj["timeType"].lower()
        
        apcApi = apcManagerApi(unitsIdList)
        timeType = apcApi.getValidTimeType(timeType)

        postBody = apcApi.apcDataUsingTagmeta(timeType,resObj)
        
        # print(json.dumps(postBody,indent=4))

        return json.dumps(postBody),200
    except:
         print(traceback.format_exc())
         abort(400)

@app.route("/apcmanager/apcrelatedtags",methods= ["POST"])
def apcrelatedtags():
     try:
        if not request.json:
            abort(400)

        resObj = request.json
        unitsIdList = ""
        timeType = resObj["timeType"].lower()

        tagmeta = resObj["tagmeta"]
        apcApi = apcManagerApi(unitsIdList)
        
        postBody = apcApi.finalApcRealtedTags(timeType,tagmeta,quries)

        print(json.dumps(postBody,indent=4))

        return json.dumps(postBody),200

     except:
          print(traceback.format_exc())
          abort(400)




if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8082)
  
