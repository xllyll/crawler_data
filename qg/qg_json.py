import json


def getCitys():
    with open('city.json', 'r', encoding='utf-8') as f:
        citys = json.load(f)
    return citys

def getFoodAE():
    with open('good_ae.json', 'r', encoding='utf-8') as f:
        aes = json.load(f)
    datas = []
    for ae in aes:
        for cc in ae:
            datas.append(cc)
    return datas

if __name__ == '__main__':
    # citys = getCitys()
    # for city in citys:
    #     print(city)
    aes = getFoodAE()
    for cc in aes:
        print(f"id:{cc['id']} name:{cc['varietyName']}")