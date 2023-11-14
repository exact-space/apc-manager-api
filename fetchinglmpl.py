import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import json
import requests
import grequests
import os
import datetime
import time
import statistics
import math
import sys
import itertools
import traceback


import platform
version = platform.python_version().split(".")[0]
if version == "3":
    import app_config.app_config as cfg
elif version == "2":
    import app_config as cfg
config = cfg.getconfig()

config["api"]["meta"] = config["api"]["meta"].replace("10.0.0.14","10.36.44.48")
config["api"]["query"] = config["api"]["query"].replace("10.0.0.14","10.36.44.48")


class fetching():
    def __init__(self,unitsIdList):
        self.unitsIdList = unitsIdList


    # --------------------------- apc meta related start -------------------- #
    def getResponseBody(self,response,word="",printa=False):
        try:
            if(response.status_code==200):
                if printa:
                    print(f"Got {word} successfully.....")

                body = json.loads(response.content)
                if type(body) != list:
                    body = [body]
                
            else:
                body =[]
                print(f"Did not get{word} successfully.....")
                print(response.status_code)
                print(response.url)

                # print(response.content)
            return body
        except:
            print(traceback.format_exc())


    def getTagMeta(self,query,retrunAsList = False):
        try:
            urlQuery = config["api"]["meta"] + '/tagmeta?filter={"where":' + json.dumps(query) + '}'
            # print(urlQuery)
            response = requests.get(urlQuery)
            word = "tagmeta"
            body = self.getResponseBody(response,word,1)
            if retrunAsList:
                returnLst = []
                for i in body:
                    returnLst.append(i["dataTagId"])
                return returnLst
            else:
                return body
        except:
            print(traceback.format_exc())


    def getUnitName(self,unitsId):
        try:
            query = {
                "id":unitsId
            }

            urlQuery = config["api"]["meta"] + '/units?filter={"where":' + json.dumps(query) + '}'  
            response = requests.get(urlQuery)
            if(response.status_code==200):
                # print(response.status_code)
                # print("Got Calculations  successfully.....")
                body = json.loads(response.content)[0]
                return body["name"]
                
            else:
                body =[]
                print("Did not get unit name successfully.....")
                print(response.status_code)
                print(response.url)

                # print(response.content)
            return body
        except:
            print(traceback.format_exc())


    def getCalculationsFromDataTagId(self,dataTagId):
        try:
            query = {
                "dataTagId":dataTagId
            }

            urlQuery = config["api"]["meta"] + '/calculations?filter={"where":' + json.dumps(query) + '}'  
            response = requests.get(urlQuery)
            if(response.status_code==200):
                # print(response.status_code)
                # print("Got Calculations  successfully.....")
                body = json.loads(response.content)
                
            else:
                body =[]
                print("Did not get calculations successfully.....")
                print(response.status_code)
                print(response.url)

                # print(response.content)
            return body
        except:
            print(traceback.format_exc())
    

    def getTagmetaFromDataTagId(self,dataTagId):
        try:
            query = {
                "dataTagId":dataTagId
            }

            urlQuery = config["api"]["meta"] + '/tagmeta?filter={"where":' + json.dumps(query) + '}'  
            response = requests.get(urlQuery)
            if(response.status_code==200):
                # print(response.status_code)
                # print("Got tagmeta successfully.....")
                body = json.loads(response.content)
                
            else:
                body =[]
                print("Did not get tagmeta successfully.....")
                print(response.status_code)
                print(response.url)

                # print(response.content)
            return body
        except:
            print(traceback.format_exc())

    
    def getTagmetaFromUnitsId(self,unitsIdList,field = False):
        try:
            urls = []
            for unitsId in unitsIdList:
                
                query ={
                    "unitsId":unitsId,
                    "measureProperty":"Power",
                    "or":[
                    {"measureType":"Load"},
                    {"measureType":"Apc"},
                    ]
                }
                if not field:
                    urlQuery = config["api"]["meta"] + '/tagmeta?filter={"where":' + json.dumps(query) + '}'  
                else:
                    fields = ["dataTagId","description","unitsId","system","systemName","equipment","equipmentName"]
                    urlQuery = config["api"]["meta"] + '/tagmeta?filter={"where":' + json.dumps(query) + ',"fields":'+ json.dumps(fields) +'}'  
 

                urls.append(urlQuery)
                # print(urlQuery)
            

            rs = (grequests.get(u) for u in urls)
            requests = grequests.map(rs)
            
            tagmeta = {}
            for idx,response in enumerate(requests):
                if response.status_code==200:
                    # print("got tagmeta successfully...")
                    tagmeta[unitsIdList[idx]] = json.loads(response.content)
                else:
                    print("Not getting tagmeta SL Level successfully...")
                    print(response.status_code)
                    print(response.url)
                    # print(response.content)
            # print(tagmeta)
            return tagmeta
    
        except Exception as e:
            print(traceback.format_exc())


    def getTagmetaForSL(self,unitsIdList):
        try:
            urls=[]
            for unitsId in unitsIdList:
                query =  {
                    "unitsId":unitsId,
                    "measureType":"Equipment Apc"
                }
                urlQuery = config["api"]["meta"] + '/tagmeta?filter={"where":' + json.dumps(query) + '}'  
                urls.append(urlQuery)
                # print(urlQuery)
            

            rs = (grequests.get(u) for u in urls)
            requests = grequests.map(rs)
            
            tagmeta = {}
            for idx,response in enumerate(requests):
                if response.status_code==200:
                    # print("got tagmeta successfully...")
                    tagmeta[unitsIdList[idx]] = json.loads(response.content)
                else:
                    print("Not getting tagmeta successfully...")
                    print(response.status_code)
                    print(response.url)

                    # print(response.content)
            # print(tagmeta)
            return tagmeta
        except:
            print(traceback.format_exc())


    def getTagmetaForUL(self,unitsIdList):
        try:
            urls=[]
            for unitsId in unitsIdList:
                query =  {
                    "unitsId":unitsId,
                    "measureType":"System Apc",
                    "equipment":"Performance Kpi",
                    "equipmentName":"Performance Kpi",
                }
                urlQuery = config["api"]["meta"] + '/tagmeta?filter={"where":' + json.dumps(query) + '}'  
                urls.append(urlQuery)
                # print(urlQuery)
            

            rs = (grequests.get(u) for u in urls)
            requests = grequests.map(rs)
            
            tagmeta = {}
            for idx,response in enumerate(requests):
                if response.status_code==200:
                    # print("got tagmeta successfully...")
                    tagmeta[unitsIdList[idx]] = json.loads(response.content)
                else:
                    print("Not getting tagmeta successfully...")
                    print(response.status_code)
                    print(response.url)

                    # print(response.content)
            # print(tagmeta)
            return tagmeta
        except:
            print(traceback.format_exc())


    def getTagmetaForDel(self):
        try:
            urls = []
            for unitsId in self.unitsIdList:
                
                query ={
                    "unitsId":unitsId,
                    "measureProperty":"Power",
                    "or":[
                    {"measureType":"Equipment Apc"},
                    {"measureType":"System Apc"},
                    {"measureType":"Unit Apc"},
                    ]
                }

                urlQuery = config["api"]["meta"] + '/tagmeta?filter={"where":' + json.dumps(query) + '}'  
                urls.append(urlQuery)
                # print(urlQuery)
            

            rs = (grequests.get(u) for u in urls)
            requests = grequests.map(rs)
            
            tagmeta = []
            for idx,response in enumerate(requests):
                if response.status_code==200:
                    # print("got tagmeta successfully...")
                    tagmeta += json.loads(response.content)
                else:
                    print("Not getting tagmeta SL Level successfully...")
                    print(response.status_code)
                    print(response.url)
                    # print(response.content)
            # print(tagmeta)
            return tagmeta
        
        except:
            print(traceback.format_exc())


    def getCalForDel(self,dataTagIdLst):
        try:
            urls = []
            for dataTagId in dataTagIdLst:
                
                query ={
                    "dataTagId":dataTagId
                }

                urlQuery = config["api"]["meta"] + '/calculations?filter={"where":' + json.dumps(query) + '}'  
                urls.append(urlQuery)
                # print(urlQuery)
            

            rs = (grequests.get(u) for u in urls)
            requests = grequests.map(rs)
            
            tagmeta = []
            for idx,response in enumerate(requests):
                if response.status_code==200:
                    # print("got tagmeta successfully...")
                    try:
                        tagmeta.append(json.loads(response.content)[0])
                    except:
                        pass
                else:
                    print("Not getting tagmeta SL Level successfully...")
                    print(response.status_code)
                    print(response.url)

                    # print(response.content)
            # print(tagmeta)
            return tagmeta
        
        except:
            print(traceback.format_exc())


    # --------------------------- apc meta related end -------------------- #


    # ----------------------------- apc api related start ----------------- #
    def getValuesV2(self,tagList,startTime, endTime,unit):
        try:
            # print(unit)
            tagList = list(set(tagList))
            url = config["api"]["query"]
            print(url)
            metrics = []
            for tag in tagList:
                tagDict = {
                    "tags":{},
                    "name":tag,
                    "aggregators": [
                                    {
                                    "name": "avg",
                                    "sampling": {
                                        "value": "1",
                                        "unit": unit
                                    },
                                        "align_start_time": True
                                    },
                                        {
                            "name": "gaps",
                            "sampling": {
                                "value": "1",
                                "unit": unit
                            },
                            "align_start_time": True
                            }
                                ]
                }
                metrics.append(tagDict)

            query ={
                "metrics":metrics,
                "plugins": [],
                "cache_time": 0,
                "start_absolute": startTime,
                "end_absolute": endTime

            }
        #     print(json.dumps(query,indent=4))
            res=requests.post(url=url, json=query)
            values=json.loads(res.content)
            finalDF = pd.DataFrame()
            for i in values["queries"]:
                df = pd.DataFrame(i["results"][0]["values"],columns=["time",i["results"][0]["name"]])

                try:
                    finalDF = pd.concat([finalDF,df.set_index("time")],axis=1)
                except Exception as e:
                    print(e)
                    finalDF = pd.concat([finalDF,df],axis=1)

            finalDF.reset_index(inplace=True)
            finalDF.fillna(0,inplace=True)
            
            # if unit.lower() != "days":
            # finalDF['time'] = finalDF['time'] + 1*1000*60*60*24
                
            # print(finalDF['time'])
            dates = pd.to_datetime(finalDF['time'],unit='ms')
            datesMonth = dates.dt.month_name()
            datesYear = dates.dt.year
            datesDate = dates.dt.day
            
            if unit.lower() == "days" or unit.lower() == "weeks":
                dates = [str(datesDate[idx])+"-"+x[:3]+"-"+str(datesYear[idx]) for idx,x in enumerate(datesMonth)]
            else:
                dates = [x[:3]+"-"+str(datesYear[idx]) for idx,x in enumerate(datesMonth)]
                
            finalDF['time'] = dates
            # print(dates)
            # print(finalDF)
            return finalDF
        
        except Exception as e:
            print(traceback.format_exc())
            return pd.DataFrame()


    def getTagmetaForApi(self,apcName,measureType):
        try:
            st = time.time()
            urls=[]
            fields = ["dataTagId","description","unitsId","system","systemName","equipment","equipmentName","measureUnit"]

            for unitsId in self.unitsIdList:
                query =  {
                    "unitsId":unitsId,
                    "measureProperty": apcName + " Apc",
                    "measureType" : measureType
                }
                urlQuery = config["api"]["meta"] + '/tagmeta?filter={"where":' + json.dumps(query) + ',"fields":'+ json.dumps(fields) +'}'  
                urls.append(urlQuery)
                print(urlQuery)
            

            rs = (grequests.get(u) for u in urls)
            requests = grequests.map(rs)
            
            tagmeta = {}
            for idx,response in enumerate(requests):
                if response.status_code==200:
                    # print("got tagmeta successfully...")
                    tagmeta[self.unitsIdList[idx]] = json.loads(response.content)
                else:
                    print("Not getting tagmeta successfully...")
                    print(response.status_code)
                    print(response.url)
                    # print(response.content)
            # print(tagmeta)
            # print(time.time() - st)
            return tagmeta
        except:
            print(traceback.format_exc())

    
    def getTagmetaForApiFromDataTagId(self,dataTagIdList):
        try:
            st = time.time()
            urls=[]
            fields = ["dataTagId","description","unitsId","system","systemName","equipment","equipmentName","measureUnit"]

            for dataTagId in dataTagIdList:
                query =  {
                        "dataTagId" : dataTagId
                }
                urlQuery = config["api"]["meta"] + '/tagmeta?filter={"where":' + json.dumps(query) + ',"fields":'+ json.dumps(fields) +'}'  
                urls.append(urlQuery)
                # print(urlQuery)
            

            rs = (grequests.get(u) for u in urls)
            requests = grequests.map(rs)
            
            tagmeta = []
            for idx,response in enumerate(requests):
                if response.status_code==200:
                    # print("got tagmeta successfully...")
                    # print(response.url)
                    # print(response.content)
                    tagmeta.append(json.loads(response.content)[0])
                else:
                    print("Not getting tagmeta successfully...")
                    print(response.status_code)
                    print(response.url)

                    # print(response.content)
            # print(tagmeta)
            # print(time.time() - st)
            return tagmeta
        except:
            print(traceback.format_exc())


    def getTagmetaForApiFromQuries(self,quries):
        try:
            st = time.time()
            urls=[]
            fields = ["dataTagId","description","unitsId","system","systemName","equipment","equipmentName","measureUnit"]

            for query in quries:
                
                urlQuery = config["api"]["meta"] + '/tagmeta?filter={"where":' + json.dumps(query) + ',"fields":'+ json.dumps(fields) +'}'  
                urls.append(urlQuery)
                # print(urlQuery)
            

            rs = (grequests.get(u) for u in urls)
            requests = grequests.map(rs)
            
            tagmeta = []
            for idx,response in enumerate(requests):
                if response.status_code==200:
                    # print("got tagmeta successfully...")
                    meta = json.loads(response.content)
                    if len(meta) > 0:
                        tagmeta.append(meta)
                        
                else:
                    print("Not getting tagmeta successfully...")
                    print(response.status_code)
                    print(response.url)

                    # print(response.content)
            # print(tagmeta)
            # print(time.time() - st)
            return tagmeta
        except:
            print(traceback.format_exc())


    # ----------------------------- apc api related end ----------------- #
