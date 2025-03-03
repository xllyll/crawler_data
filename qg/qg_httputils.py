import http.client
import ssl
import json
import time

import qg_json
from urllib.parse import urlencode

def getCompany(code):
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection("pfsc.agri.cn", context=context)
    payload = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Host': 'pfsc.agri.cn',
        'Connection': 'keep-alive'
    }
    url_path = f"/api/priceQuotationController/getMarketByProvinceCode?code={code}"
    conn.request("POST", url_path, payload, headers)
    res = conn.getresponse()
    data = res.read()
    jsonStr = data.decode("utf-8")
    json_data = json.loads(jsonStr)

    contents = json_data["content"]
    for content in contents:
        print(content["enterpriseName"])


def get7DayDatas(code,marketId,names):
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection("pfsc.agri.cn", context=context)
    payload = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Host': 'pfsc.agri.cn',
        'Connection': 'keep-alive'
    }
    p = {
        "name":names,
        "cycle":"近7日",
        "order":"ASC",
        "provinceCode":code,
        "marketId":marketId
    }
    url_path = f"/api/marketQuotationController/getSingleMarketManyVarieties?"
    #urlencode
    url_path = url_path + urlencode(p)
    print(url_path)
    conn.request("POST", url_path, payload, headers)
    res = conn.getresponse()
    data = res.read()
    jsonStr = data.decode("utf-8")
    json_data = json.loads(jsonStr)

    contents = json_data["content"]
    for content in contents:
        print(content["enterpriseName"])

def priceQuotationController(marketId,provinceCode,pageNum,varietyId):
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection("pfsc.agri.cn", context=context)
    p = {
        "marketId": marketId,
        "provinceCode": provinceCode,
        "pageNum": pageNum,
        "pageSize": 10,
        "pid": "AE",
        "varietyId": varietyId
    }
    payload = json.dumps(p)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'pfsc.agri.cn',
        'Connection': 'keep-alive'
    }
    conn.request("POST", "/api/priceQuotationController/pageList?key=&order=", payload, headers)
    res = conn.getresponse()
    data = res.read()
    jsonStr = data.decode("utf-8")
    json_data = json.loads(jsonStr)
    content = {}
    try:
        content = json_data["content"]
    except:
        print(jsonStr)
    return content

def buildQuotationData(content):
    time.sleep(5)
    list = content["list"]
    if len(list)>0:
        for item in list:
            varietyName = item["varietyName"]
            minimumPrice= item["minimumPrice"]
            middlePrice = item["middlePrice"]
            highestPrice = item["highestPrice"]
            print(f"name:{varietyName} min:{minimumPrice} middle:{middlePrice} max:{highestPrice}")

if __name__ == '__main__':
    # 北京
    # getCompany("110000")
    # get7DayDatas("110000","76E4F160BFCF936CE040A8C020017257","大白菜")

    content = priceQuotationController("","",1,"135")
    pages = content["pages"]
    buildQuotationData(content)
    if pages>1:
        for page in range(2,pages+1):
            content = priceQuotationController("","",page,"135")
            buildQuotationData(content)

    # citys = qg_json.getCitys()
    # for city in citys:
    #     code = city['id']
    #     print(f"city:{city['name']} id:{code}")
    #     getCompany(code)