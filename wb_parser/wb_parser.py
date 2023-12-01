import requests as req
import json

def parser():
    name = 'рубашка мужская'
    r = req.get(f'https://catalog.wb.ru/catalog/tops_tshirts1/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat=8142&curr=rub&dest=-1257786&page=10')
    #return json.loads(r.text)['data']['products'][0]
    return r.status_code
print(parser())
# with open ('test.json', 'w') as file:
#     json.dump(parser(), file, ensure_ascii=False, indent=4)

def main():
    pass

