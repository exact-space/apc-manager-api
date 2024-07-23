import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import json
import grequests
import os
import datetime
import time
import statistics
import math
import sys
import itertools
import traceback
from fetchinglmpl import fetching,config,mainConfig

import requests


def tr():
    print(traceback.format_exc())
    
class posting(fetching):
    def postInTagmeta(self,postBody):
        sumTagName = postBody["dataTagId"]
        unitsId = postBody["unitsId"]

        checkBody = self.getTagmetaFromDataTagId(sumTagName)

        if len(checkBody)>1:
            print("ALEART!!!!!!!!!!!!")
            print(f"Found multiple traces of {sumTagName}")

        if len(checkBody) == 0:
            del postBody["id"]
            url = config["api"]["meta"] + f"/units/{unitsId}/tagmeta"
            response = requests.post(url,json=postBody)

            if response.status_code == 200 or response.status_code == 204:
                print(f"{sumTagName} Tagmeta posting successful..")

            else:
                print(f"{sumTagName} Tagmeta posting unsuccessful..")
                print(response.status_code,response.content)

        else:
            # print(len(checkBody))
            # print(f"{sumTagName} is already in tagmeta so updating...")
            postBody["id"] = checkBody[0]["id"]
            self.updateTagmeta(postBody,checkBody[0]["id"])


    def updateTagmeta(self,postBody,id):
        query ={
            "id":id
        }
        url = config["api"]["meta"] + '/tagmeta/update?where=' + json.dumps(query)
        response = requests.post(url,json=postBody)
        tag = postBody["dataTagId"]

        if response.status_code == 200 or response.status_code == 204:
            
            print(f"{tag} Tagmeta updating successful..")

        else:
            print(f"{tag} Tagmeta updating unsuccessful..")
            print(response.status_code,response.content)

    
    def updateCalculations(self,postBody,id):
        query ={
            "id":id
        }
        url = config["api"]["meta"] + '/calculations/update?where=' + json.dumps(query)
        response = requests.post(url,json=postBody)
        tag = postBody["dataTagId"]
        if response.status_code == 200 or response.status_code == 204:
            
            print(f"{tag} Calculations updating successful..")

        else:
            print(f"{tag} Calculations updating unsuccessful..")
            print(response.status_code,response.content)

    # -------------------- Equipment level start ------------- #
    def createSumTagNameEL(self,postdf):
        try:
            dataTagId = postdf.loc[0,"dataTagId"]
            prefix = dataTagId.split("_")[0]
            unitsId = postdf.loc[0,"unitsId"][-4:]
            epqName = postdf.loc[0,"equipment"].replace(" ","")
            mp = postdf.loc[0,"measureProperty"].replace(" ","")

            sumTagName = prefix + "_" + unitsId + "_" +epqName + "_Total_" + mp
            return sumTagName
        
        except:
            print(traceback.format_exc())


    def createPostBodyEL(self,sumTagName,postdf):
        try:
            instList = ["systemInstance","equipmentInstance","measureInstance"]

            for inst in instList:
                lim = postdf[inst].unique().min()
                postdf = postdf[postdf[inst]==lim].reset_index(drop=True)
            

            postBody = json.loads(postdf.to_json(orient="records"))[0]
            unitsId = postBody["unitsId"]
            postBody["dataTagId"] = sumTagName
            postBody["benchmarkLoad"] = {
                "status":"invalid"
            }
            postBody["measureType"] = "Equipment Apc"
            postBody["description"] = postBody["equipment"]+" Total Equipment Apc"
            postBody["standardDescription"] = ""
            postBody["component"]  = ""
            postBody["subcomponent"]  = ""
            postBody["componentName"] = ""
            
            # print(json.dumps(postBody,indent=4))
            self.postInTagmeta(postBody)
            

        except:
            print(traceback.format_exc())


    def postInTagmetaEL(self,postdf):
        try:
            sumTagName = self.createSumTagNameEL(postdf)
            postBody = self.createPostBodyEL(sumTagName,postdf)
            return sumTagName
        except:
            print(traceback.format_exc())


    def createPostBodyForCal(self,sumTagName,postdf):
        publishBodyCal = {
            "type":"sum",
            "formula":{
            "v1":list(postdf["dataTagId"]),
            },
            "dataTagId":sumTagName,
            "unitsId":postdf.loc[0,"unitsId"]
        }

        return publishBodyCal
    


    def postInCal(self,sumTagName,postdf):
        postBodyCal = self.createPostBodyForCal(sumTagName,postdf)

        checkBody = self.getCalculationsFromDataTagId(sumTagName)
        print(json.dumps(postBodyCal,indent=4))

        if len(checkBody)>1:
            print("ALEART!!!!!!!!!!!!")
            print(f"found multiple traces of {sumTagName}")

        if len(checkBody) == 0:
            unitsId = postBodyCal["unitsId"]
            url = config["api"]["meta"] + f"/units/{unitsId}/calculations"
            response = requests.post(url,postBodyCal)

            if response.status_code == 200 or response.status_code == 204:
                print(f"{sumTagName} Calcumations body posting successfull...")

            else:
                print(f"{sumTagName} calcumations body posting unsuccessfull...")
                print(response.status_code,response.content)
        else:
            # print(len(checkBody))
            # print(f"{sumTagName} is already present in calculation so updating...")
            postBodyCal["id"] = checkBody[0]["id"]
            self.updateCalculations(postBodyCal,postBodyCal["id"])
    

    # -------------------- Equipment level End ------------- #

    # ---------------------- system level Start --------------- #
    def createSumTagNameSL(self,namedf):
        try:
            dataTagId = namedf.loc[0,"dataTagId"]
            prefix = dataTagId.split("_")[0]
            unitsId = namedf.loc[0,"unitsId"][-4:]
            system = namedf.loc[0,"systemName"].replace(" ","")
            sysInst = str(namedf.loc[0,"systemInstance"])
            mp = namedf.loc[0,"measureProperty"].replace(" ","")

            sumTagName = prefix + "_" + unitsId + "_" +system + "_" + sysInst + "_Total_" + mp

            return sumTagName
        
        except:
            print(traceback.format_exc())


    def createPostBodySL(self,sumNameSL,pbdf):
        try:
            
            postBody = json.loads(pbdf.to_json(orient="records"))[0]
            unitsId = postBody["unitsId"]
            postBody["benchmarkLoad"] = {
                "status":"invalid"
            }
            postBody["dataTagId"] = sumNameSL
            postBody["measureType"] = "System Apc"
            postBody["equipment"] = "Performance Kpi"
            postBody["equipmentName"] = "Performance Kpi"
            postBody["description"] = pbdf.loc[0,"systemName"].replace(" ","") + " Total System Apc"
            postBody["standardDescription"] = ""
            
            # print(json.dumps(postBody,indent=4))

            self.postInTagmeta(postBody)

        except:
            print(traceback.format_exc())


    def postInTagmetaSL(self,postdf):
        try:

            sumNameSL = self.createSumTagNameSL(postdf)
            self.createPostBodySL(sumNameSL,postdf)
            return sumNameSL

        except:
            print(traceback.format_exc())


    # ---------------------- system level End --------------- #

    # --------------------- Unit level start ---------------- #
    def createSumTagNameUL(self,namedf):
        try:
            dataTagId = namedf.loc[0,"dataTagId"]
            prefix = dataTagId.split("_")[0]
            unitsId = namedf.loc[0,"unitsId"][-4:]
            system = namedf.loc[0,"system"].replace(" ","")
            sysInst = str(namedf.loc[0,"systemInstance"])
            mp = namedf.loc[0,"measureProperty"].replace(" ","")

            sumTagName = prefix + "_" + unitsId + "_" + "Unit_Apc"
            return sumTagName
        
        except:
            print(traceback.format_exc())


    def createPostBodyUL(self,sumTagName,pbdf):
        try:
            
            postBody = json.loads(pbdf.to_json(orient="records"))[0]
            unitsId = postBody["unitsId"]
            postBody["benchmarkLoad"] = {
                "status":"invalid"
            }
            postBody["dataTagId"] = sumTagName
            postBody["measureType"] = "Unit Apc"
            postBody["equipment"] = "Performance Kpi"
            postBody["equipmentName"] = "Performance Kpi"
            postBody["system"] = "Unit Performance"
            postBody["systemName"] = "Unit Performance"
            unitName = self.getUnitName(unitsId)
            postBody["description"] = unitName+ " Total Unit Apc"
            postBody["standardDescription"] = ""
            



            # print(json.dumps(postBody,indent=4))

            self.postInTagmeta(postBody)

        except:
            print(traceback.format_exc())


    def postinTagmetaUL(self,postdf):
        try:
            sumTagNameUL = self.createSumTagNameUL(postdf)
            self.createPostBodyUL(sumTagNameUL,postdf)
            return sumTagNameUL
        except:
            print(traceback.format_exc())


    # --------------------- Unit level End ---------------- #




class apcManager(posting):
    def __init__(self,unitsIdList):
        self.unitsIdList = unitsIdList

    # ------------------------- Creating meta level start ---------------------- #
    def mainELfunction(self):
        """
        Use: to filter data equipment wise.
        """
        try:
            print("At equipment level.....")
            tagmeta = self.getTagmetaFromUnitsId(self.unitsIdList)
            for unitsId in tagmeta:
                df = pd.DataFrame(tagmeta[unitsId])
                # print(df)
                for sysName in df["systemName"].unique():
                    sysNamedf = df[df["systemName"]==sysName]
                    for eqpName in sysNamedf["equipment"].unique():
                        
                        
                        eqpNamedf = sysNamedf[(sysNamedf["equipment"]==eqpName)].reset_index(drop=True)
                        
                        sumTagName = self.postInTagmetaEL(eqpNamedf)
                        self.postInCal(sumTagName,eqpNamedf)
                   
        except:
            print(traceback.format_exc())


    def mainSLFunction(self):
        try:
            print("At system level......")
            tagmeta = self.getTagmetaForSL(self.unitsIdList)
            for unitsId in tagmeta:
                df = pd.DataFrame(tagmeta[unitsId])
                for sysName in df["systemName"].unique():
                    sysNamedf = df[df["systemName"]==sysName]
                    lim = sysNamedf["systemInstance"].unique().min()
                    sysNamedf = sysNamedf[sysNamedf["systemInstance"]==lim].reset_index(drop=True)

                    sysNamedf = df[df["systemName"]==sysName].reset_index(drop=True)
                    # print(sysNamedf)
                    sumTagName = self.postInTagmetaSL(sysNamedf)

                    self.postInCal(sumTagName,sysNamedf)
                    
        except:
            print(traceback.format_exc())


    def mainULFucntion(self):
        try:
            print("At unit level......")
            tagmeta = self.getTagmetaForUL(self.unitsIdList)

            for unitsId in tagmeta:
                df = pd.DataFrame(tagmeta[unitsId])
                sumTagNameUL = self.postinTagmetaUL(df)
                self.postInCal(sumTagNameUL,df)

        except:
            print(traceback.format_exc())


    def createTagAndCalMeta(self):
        self.mainELfunction()
        self.mainSLFunction()
        self.mainULFucntion()

    # ------------------------- Creating meta level end ---------------------- #

    # ------------------------- Deleting meta Start --------------------------- # 
    def getDataTagIdFromMeta(self,tagmeta):
        if type(tagmeta) == list:
            dataTagIdLst= []
        
            for i in tagmeta:
                dataTagIdLst.append(i["dataTagId"])
            return dataTagIdLst

        elif type(tagmeta) == dict:
            dataTagIdLst= []
            lst = []
            for unitsId in tagmeta:
                for i in tagmeta[unitsId]:
                    dataTagIdLst.append(i["dataTagId"])
                    lst.append(i)
            return dataTagIdLst,lst


    def delDataInTagmeta(self,tagmeta,type):
        for i in tagmeta:
            dataTagId = i["dataTagId"]
            if type == "tagmeta":
                url = config["api"]["meta"] + "/tagmeta/" + i["id"]
            elif type =="cal":
                url = config["api"]["meta"] + "/calculations/" + i["id"]
                # print(url)
            else:
                print("procide valid type")
            
            response = requests.delete(url)

            if response.status_code == 200 or response.status_code == 204:
                if type == "tagmeta":
                    print(f"{dataTagId} deleting tagmeta successfull...")
                else:
                    print(f"{dataTagId} deleting calulations successfull...")


            else:
                if type == "tagmeta":
                    print(f"{dataTagId} deleting tagmeta unsuccessfull...")
                    print(response.status_code,response.content)
                else:
                    print(f"{dataTagId} deleting calulations unsuccessfull...")
                    print(response.status_code,response.content)




    def deleteTagAndCalMeta(self):
        tagmeta = self.getTagmetaForDel()
        dataTagIdLst = self.getDataTagIdFromMeta(tagmeta)
        tagmetaCal = self.getCalForDel(dataTagIdLst)

        self.delDataInTagmeta(tagmeta,"tagmeta")
        self.delDataInTagmeta(tagmetaCal,"cal")
        
    # ------------------------- Deleting meta End --------------------------- # 
    


class apcManagerApi(apcManager):
    def __init__(self,unitsIdList):
        self.unitsIdList = unitsIdList


    def getValidTimeType(self,string):
        try:
            dic = {
                "daily" : "days",
                "weekly": "weeks",
                "yearly":"months",
                "monthly":"months"
            }
            return dic[string]
        except:
            print(traceback.format_exc())

    def getValidTimeFrame(self,timeType):
        try:
            now = datetime.datetime.now() + datetime.timedelta(hours=5,minutes=30)
            day = 31 - now.day
            weekday = 7 - now.isoweekday()
            hr = 24 - now.hour - 1
            mit = 60 - now.minute - 1
            sec = 60 - now.second - 1
            msec = 999 - now.microsecond
            
            # print(now)
            if timeType.lower() == "days":
                now = now + datetime.timedelta(hours=hr,minutes=mit,seconds=sec,microseconds=msec)
                endTimeStamp = int(datetime.datetime.timestamp(now)*1000)
                day = 7
                startTimeStamp = endTimeStamp - 1*1000*60*60*24*day + 1*1000*60*60*5.5 + 1*1000
            
            elif timeType.lower() == "weeks":
                now = now + datetime.timedelta(days=weekday,hours=hr,minutes=mit,seconds=sec,microseconds=msec)
                endTimeStamp = int(datetime.datetime.timestamp(now)*1000)
                week = 4
                startTimeStamp = endTimeStamp - 1*1000*60*60*24*7*week + 1*1000*60*60*5.5 + 1*1000
                print(now)
                
            elif timeType.lower() == "months":
                now = now + datetime.timedelta(days=day,hours=hr,minutes=mit,seconds=sec,microseconds=msec)
                endTimeStamp = int(datetime.datetime.timestamp(now)*1000)
                days = 365
                startTimeStamp = endTimeStamp - 1*1000*60*60*24*days + 1*1000*60*60*5.5 + 1*1000
            # print(now)
            self.startTimeStamp = startTimeStamp
            self.endTimeStamp = endTimeStamp
        except:
            print(traceback.format_exc())
    
    
    def getDescriptionFromMeta(self,tagmeta):
        if type(tagmeta) == list:
            desc= []
        
            for i in tagmeta:
                desc.append(i["description"])
            return desc

        elif type(tagmeta) == dict:
            desc = []
            for unitsId in tagmeta:
                for i in tagmeta[unitsId]:
                    desc.append(i["description"])
            return desc
        

    def hundredRule(self,df,tagList):
        try:
            print("using hundrule")
            if mainConfig[self.unitsIdList[0]]["hundredRule"]:
                # print(df)
                for tag in tagList:
                    print("using hundred rule..",self.unitsIdList[0])
                    try:
                        idx = df[df[tag] > mainConfig[self.unitsIdList[0]]["hundValue"]].index
                        df.loc[idx,tag] = mainConfig[self.unitsIdList[0]]["hundValue"]
                    except:
                        idx = df[df[tag] > 100].index
                        df.loc[idx,tag] = 0
                    
                    print(df)
            return df
        except:
            print(traceback.format_exc())
            return df


    def ApcData(self,timeType,level,measureType):
        try:
            self.getValidTimeFrame(timeType)
            # print(startTimeStamp,endTimeStamp)
            tagmeta = self.getTagmetaForApi(level,measureType)
            # print(json.dumps(tagmeta,indent=4))
            dataTagIdList,uiTagmeta = self.getDataTagIdFromMeta(tagmeta)
            dataTagIdList = list(set(dataTagIdList))
            # descList = self.getDescriptionFromMeta(tagmeta)
            uldf = self.getValuesV2(dataTagIdList,self.startTimeStamp,self.endTimeStamp,timeType)[-7:]
            uldf = self.hundredRule(uldf,dataTagIdList)


            postBody = json.loads(uldf.to_json(orient="records"))
            postBody ={
                "tagmeta" : uiTagmeta,
                "data" : postBody
            }
            print(json.dumps(postBody,indent=4))

            return postBody
        except:
            print(traceback.format_exc())


    def ApcDataPerc(self,timeType,level,measureType):
        try:
            self.getValidTimeFrame(timeType)
            # print(startTimeStamp,endTimeStamp)
            tagmeta = self.getTagmetaForApi(level,measureType)
            # print(json.dumps(tagmeta,indent=4))
            dataTagIdList,uiTagmeta = self.getDataTagIdFromMeta(tagmeta)
            for i in uiTagmeta:
                i["measureUnit"] = "%"
            dataTagIdList = list(set(dataTagIdList))
            # descList = self.getDescriptionFromMeta(tagmeta)
            # lloadQuery = {
            #         "unitsId" : self.unitsIdList[0],
            #         "measureInstance" : 1,
            #         "equipment" : "Generator",
            #         "system" : "Generator System",
            #         "measureType" : "Load",
            #         "measureProperty" : "Power"
            #     }
            
            # loadTag = self.getTagMeta(lloadQuery,True)
            
            uldf = self.getValuesV2(dataTagIdList,self.startTimeStamp,self.endTimeStamp,timeType)[-7:]
            uldf = self.hundredRule(uldf,dataTagIdList)
            

            uldf[dataTagIdList] = uldf[dataTagIdList]/10
            # print(uldf)

            postBody = json.loads(uldf.to_json(orient="records"))
            postBody ={
                "tagmeta" : uiTagmeta,
                "data" : postBody
            }
            print(json.dumps(postBody,indent=4))
            return postBody
        except:
            print(traceback.format_exc())


    def getDataTagIdsFromResObj(self,resObj):
        dataTagId = []
        for tagmeta in resObj["tagmeta"]:
            dataTagId.append(tagmeta["dataTagId"])

        return dataTagId
    
    def getDataTagIdFromCalMeta(seld,calMeta):
        dataTagIds = []
        ExceptionList = ["HRD_30MKA10CE001.PV","HRD_30MKA10CE001.PV_HRD_B8_STM_FT_128AB.DACA.PV_ratio"]
        for cal in calMeta:
            if type(cal["formula"]["v1"]) == list:
                
                dataTagIds += cal["formula"]["v1"]
            else:
                dataTagIds += [ cal["formula"]["v1"],cal["formula"]["v2"]]
        
        dataTagIds = [x for x in dataTagIds if x not in ExceptionList]
        return dataTagIds
    

    def apcDataUsingTagmeta(self,timeType,resObj,hund = True):
        self.getValidTimeFrame(timeType)
        dataTagIds = self.getDataTagIdsFromResObj(resObj)
        # print(dataTagIds)
        calMeta = self.getCalForDel(dataTagIds)
        dataTagIds = self.getDataTagIdFromCalMeta(calMeta)
        # print(dataTagIds)

        # calMeta = self.getCalForDel(dataTagIds)
        # dataTagIds = self.getDataTagIdFromCalMeta(calMeta)
        # print(dataTagIds)
        tagmeta = self.getTagmetaForApiFromDataTagId(dataTagIds)
        uldf = self.getValuesV2(dataTagIds,self.startTimeStamp,self.endTimeStamp,timeType)[-7:]
        

        if hund:
            uldf = self.hundredRule(uldf,dataTagIds)

        postBody = json.loads(uldf.to_json(orient="records"))
        postBody ={
            "tagmeta" : tagmeta,
            "data" : postBody
        }
        # print(json.dumps(postBody,indent=4))
        return postBody
    

    def apcDataUsingTagmetaPerc(self,timeType,resObj):
        try:
            self.getValidTimeFrame(timeType)
            dataTagIds = self.getDataTagIdsFromResObj(resObj)
            calMeta = self.getCalForDel(dataTagIds)
            dataTagIds = self.getDataTagIdFromCalMeta(calMeta)
            

            tagmeta = self.getTagmetaForApiFromDataTagId(dataTagIds)
            for i in tagmeta:
                i["measureUnit"] = "%"

            uldf = self.getValuesV2(dataTagIds,self.startTimeStamp,self.endTimeStamp,timeType)[-7:]
            uldf = self.hundredRule(uldf,dataTagIds)



            uldf[dataTagIds] = uldf[dataTagIds] / 10

            postBody = json.loads(uldf.to_json(orient="records"))
            postBody ={
                "tagmeta" : tagmeta,
                "data" : postBody
            }
            # print(json.dumps(postBody,indent=4))
            return postBody
        except:
            tr()
    

    def getDataTagIdFromMetaV2(self,tagmeta):
        dataTagIdLst= []
        returnlst = []
        for lst in tagmeta:
            lst2 = []
            for tag in lst:
                dataTagIdLst.append(tag["dataTagId"])
                lst2.append(tag)
            returnlst.append(lst2)

        return dataTagIdLst,returnlst
    

    def getValidParamForQuries(self,tagmeta):
        try:
            returnDict = {}
            for tagm in  tagmeta:
                eqp = tagm["equipment"].replace(" ","").lower() + "_" + tagm["systemName"] + "_" + tagm["unitsId"]
                if eqp not in returnDict:
                    returnDict[eqp] = {
                        "unitsId":tagm["unitsId"],
                        "systemName" : tagm["systemName"]
                    }

            return returnDict
        except:
            print(traceback.format_exc())


    def getFinalQuries(self,quries,quries2):
        try:
            # print(json.dumps(quries2,indent=4))
            returnlst = []
            for query2 in quries2:
                eqpname = query2.split("_")[0].lower()
                for query in quries[eqpname]:
                    
                    # if "equipment" in query:
                    #     copyDict = quries2[query2].copy()
                    #     del copyDict["equipment"]
                    #     query3 = {**query,**copyDict}

                    # else:
                        # query3 = {**query,**quries2[query2]}

                    query3 = {**query,**quries2[query2]}
                    returnlst.append(query3)
                    
            return returnlst
        
        except:
            print(traceback.format_exc())


    def apcDataRelatedTags(self,timeType,quries):
        try:
            self.getValidTimeFrame(timeType)
            tagmeta = self.getTagmetaForApiFromQuries(quries)
            # print(tagmeta)
            dataTagIdList,uiTagmeta = self.getDataTagIdFromMetaV2(tagmeta)
            
            uldf = self.getValuesV2(list(set(dataTagIdList)),self.startTimeStamp,self.endTimeStamp,timeType)[-7:]
            postBody = json.loads(uldf.to_json(orient="records"))
            postBody ={
                "tagmeta" : uiTagmeta,
                "data" : postBody
            }
            # print(json.dumps(postBody,indent=4))
            return postBody
        except:
            print(traceback.format_exc())
        

    def finalApcRealtedTags(self,timeType,tagmeta,quries):
        quries2 = self.getValidParamForQuries(tagmeta)
        finalQuries = self.getFinalQuries(quries,quries2)
        timeType = self.getValidTimeType(timeType)
        return self.apcDataRelatedTags(timeType,finalQuries)
    

