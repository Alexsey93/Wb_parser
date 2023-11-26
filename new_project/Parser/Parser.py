import requests
from bs4 import BeautifulSoup as bs
import json
#import asyncio
#from aiohttp import ClientSession
import os
import shutil
import time
from aiohttp_retry import RetryClient, ExponentialRetry



HEADERS_WB = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://www.wildberries.ru',
    'Connection': 'keep-alive',
    'Referer': 'https://www.wildberries.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
}


pattern = (r'^/\w+')

def make_folder():
    folder = "data"
    if os.path.exists(folder) == True:
        print("Найдена папка, хотите перезаписать?")
        if input("Если да, введите Y, если нет, введите N ") == "Y":
            shutil.rmtree(folder)
            os.mkdir(folder)
    else:
        os.mkdir(folder)
        print(f'{folder}')
        
class Parser:
    
    def __init__(self, url, header):
        self.url = url
        self.header = header
    
    def get_page(self):
        return requests.get(self.url, self.header).text
    
class Json_write:
    
    def __init__(self, name_cat, json=''):
        self.name_cat = name_cat
        self.json = json
    
    def loads_json(self, page):
        self.json = json.loads(page)
    
    def write_json(self):
        with open (f'data/{self.name_cat}.json', 'w') as f:
            json.dump(self.json, f, ensure_ascii=False, indent=4)
            
    def write_json_s(self):
        
        with open (f'data/{self.name_cat}.json', 'w') as f:
            f.write(json.dumps(self.json, ensure_ascii=False, indent=4))
            
class Items_json:
    
    def __init__(self, shard, cat_id):
        self.shard = shard
        self.cat_id = cat_id
        
        
    def item_info(self):
        self.info = []
        HEADERS_WB = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://www.wildberries.ru',
    'Connection': 'keep-alive',
    'Referer': 'https://www.wildberries.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
        }
        with requests.Session() as session:        
            page = 1
            r = session.get(f'https://catalog.wb.ru/catalog/{self.shard}/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat={self.cat_id}&curr=rub&dest=-1257786&page={page}')
            while True:
                try:
                    r = session.get(f'https://catalog.wb.ru/catalog/{self.shard}/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat={self.cat_id}&curr=rub&dest=-1257786&page={page}')
                    #print(r.text)
                    print(f'категория --- {self.shard} --- страница в категории --- {page} --- {r.status_code} -- {type(self.info)}\n')
                    page += 1
                    self.info.append(r.json())
                except Exception as ex:
                    print(f'Ыозникла ошибка {ex} вероятно достигнут конец пагинации\n')
                    print(f'Переход к следующей категории')
                    break
                time.sleep(0.5)
    
    
    
    
    
# wb_pars_cat = Parser('https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json',HEADERS_WB)

# wb_pars_item = Parser(items_url,HEADERS_WB)
#print(wb_pars.get_soup(wb_pars.get_page()))
# json_wb = json.loads(wb_pars.get_page())
# print(json_wb)
# with open ('test.json', 'w') as file:
#     json.dump(json_wb, file, ensure_ascii=False, indent=4)

# name_file = 'menu'
# wb_json = Json_file(name_file)

# wb_json.load_json(wb_pars_cat.get_page())
# wb_json.write_json()

# test = Items_json('bl_shirts', 8126, 1)
# test_wr = Json_write('bl_shirts', test.info)
# test_wr.write_json()

# item = Json_file()
# item.load_json(wb_pars_item.get_page())
# item.write_json()
def dict_info():
    dict_info = {}
    with open ('/home/alex/parser/new_project/menu.json') as f:
        name = json.load(f)
    #    name.pop(0)
    #print(type(name))    
    for item_cat in name:
        if not('shard' in item_cat):
            if 'childs' in item_cat:
                for child in item_cat['childs']:
                    #print(child, '\n')
                    if 'shard' in child:
                        dict_info[child['shard']] = child['id']
        elif item_cat['shard'] == 'blackhole':
            for child in item_cat['childs']:
                if 'shard' in child:
                    dict_info[child['shard']] = child['id']
    pages_item = [Items_json(f'{name}', value) for name, value in dict_info.items()]
    return pages_item
    #     #pass
        #print(item_cat, '\n') 
    #print(name[0])        
# for i in range(len(dict_info())):
#     asyncio.run(dict_info()[i].gather_item_info())



def main():
    for item in dict_info():
        item.item_info()
        page_info = Json_write(item.shard, item.info)
        page_info.write_json()
        
        
#        print(item.info)
#     print(pages_item)
    # print(dict_info()[0].info)
    # make_folder()
    # make_folder()
        # with open (f'data/{item.shard}.json', 'w') as f:
        #     json.dump(item.info, f, ensure_ascii=False, indent=4)
        
main()
#         print(key, " ", value, '\n')
    
                    
    
        