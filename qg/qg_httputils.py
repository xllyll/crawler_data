import http.client
import ssl
import json
import qg_json

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

if __name__ == '__main__':
    # 北京
    # getCompany("110000")
    citys = qg_json.getCitys()
    for city in citys:
        code = city['id']
        print(f"city:{city['name']} id:{code}")
        getCompany(code)