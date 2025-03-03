import json


def getCitys():
    with open('city.json', 'r', encoding='utf-8') as f:
        citys = json.load(f)
    return citys

if __name__ == '__main__':
    citys = getCitys()
    for city in citys:
        print(city)