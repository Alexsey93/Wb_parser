import requests
from bs4 import BeautifulSoup as bs
import json
#import asyncio
#from aiohttp import ClientSession
import os
import shutil
import time
from aiohttp_retry import RetryClient, ExponentialRetry
from src.modules import Items
from src.modules import write
time_counter = 0


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


# pattern = (r'^/\w+')
class Parser():
    
    def __init__(self, url, header):
        self.url = url
        self.header = header
    
    def get_page(self):
        return requests.get(self.url, self.header).text

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
    pages_item = [Items.Items_json(f'{name}', value) for name, value in dict_info.items()]
    return pages_item

def main():
    url = 'https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json'
    menu = Parser(url, HEADERS_WB)
    write_menu_json = write.Json_write('menu')
    write_menu_json.loads_json(menu.get_page())
    write_menu_json.write_json()
    start_time = time.time()
    for item in dict_info():
        item.item_info()
        page_info = write.Json_write(item.shard, item.info)
        page_info.write_json()
        current_time = time.time()
        print(f'[INFO] прошло времени: {time.gmtime(current_time - start_time)[4]} мин : {time.gmtime(current_time - start_time)[5]} сек')
    end_time = time.time()    
    print(f'[INFO] затрачено вермя: {end_time - start_time}')    
#        print(item.info)
#     print(pages_item)
    # print(dict_info()[0].info)
    # make_folder()
    # make_folder()
        # with open (f'data/{item.shard}.json', 'w') as f:
        #     json.dump(item.info, f, ensure_ascii=False, indent=4)
if __name__ == '__main__':
    main()
#         print(key, " ", value, '\n')
    
                    
    
        