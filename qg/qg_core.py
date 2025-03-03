import qg_json
import qg_httputils
import qg_dbcore
import time

def buildQuotationData(goodId,goodName,content):
    time.sleep(5)
    list = content["list"]
    if len(list)>0:
        for item in list:
            marketId = item["marketId"]
            marketCode = item["marketCode"]
            marketName = item["marketName"]
            varietyName = item["varietyName"]
            minimumPrice= item["minimumPrice"]
            middlePrice = item["middlePrice"]
            highestPrice = item["highestPrice"]
            if minimumPrice is None:
                minimumPrice = 0
            if middlePrice is None:
                middlePrice = 0
            if highestPrice is None:
                highestPrice = 0
            print(f"market:{marketName} name:{varietyName} min:{minimumPrice} middle:{middlePrice} max:{highestPrice}")
            # 获取当前年月日
            q_time = time.strftime("%Y-%m-%d", time.localtime())
            # 创建 Quotation 对象
            qData = qg_dbcore.QGQuotation(
                0, goodId, goodName, marketId, marketName, highestPrice, minimumPrice, middlePrice, q_time
            )
            qg_dbcore.saveQuotationData2DB(qData)

if __name__ == '__main__':
    aes = qg_json.getFoodAE()
    print(f"length::::   {len(aes)}")
    for cc in aes:
        goodId = int(cc['id'])
        goodName = cc['varietyName']
        print(f"id:{goodId} name:{goodName}")
        content = qg_httputils.priceQuotationController("","",1,str(goodId))
        pages = content["pages"]
        buildQuotationData(goodId,goodName,content)
        if pages>1:
            for page in range(2,pages+1):
                content = qg_httputils.priceQuotationController("","",page,str(goodId))
                buildQuotationData(goodId,goodName,content)