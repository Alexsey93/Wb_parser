import requests
from bs4 import BeautifulSoup as bs
import json
import asyncio
from aiohttp import ClientSession
import os
import shutil
import time
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent


time_counter = 0
url = ''

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

# class Async_parser:
    
#     def __init__(self, shard, cat_id):
#         self.shard = shard
#         self.cat_id = cat_id
        
#     async def get_data(self):
#         proxies = {
#             'https' : 'https://51.159.111.39:8000',
#         }
#         ua = UserAgent(min_percentage=1.3)
#         headers = {
#     'User-Agent': f'{ua.random}',
#     'Accept': '*/*',
#     'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
#     # 'Accept-Encoding': 'gzip, deflate, br',
#     'Origin': 'https://www.wildberries.ru',
#     'Connection': 'keep-alive',
#     'Referer': 'https://www.wildberries.ru/',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'cross-site',
# }
        
#         async with ClientSession() as session:
#             print(f'Выполняется парсинг ')
#             r = await session.get(url=self.url, headers=headers)
#             self.info = r.json() 
#             time.sleep(0.5)
#             print(r.status)
#             await self.info   

    
#     async def gather_data(self):
#         ua = UserAgent(min_percentage=1.3)
#         headers = {
#     'User-Agent': f'{ua.random}',
#     'Accept': '*/*',
#     'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
#     # 'Accept-Encoding': 'gzip, deflate, br',
#     'Origin': 'https://www.wildberries.ru',
#     'Connection': 'keep-alive',
#     'Referer': 'https://www.wildberries.ru/',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'cross-site',
# }
#         proxies = {
#             'https' : 'https://51.159.111.39:8000',
#         }
#         page = 1
#         tasks = []
#         self.url = f'https://catalog.wb.ru/catalog/{self.shard}/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat={self.cat_id}&curr=rub&dest=-1257786&page={page}'
#         async with ClientSession() as session:
#             self.r = await session.get(self.url)
#             while self.r.status == 200:
#                     self.r = await session.get(self.url)
#                     self.url = f'https://catalog.wb.ru/catalog/{self.shard}/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat={self.cat_id}&curr=rub&dest=-1257786&page={page}'
#                     print(page)
#                     task = asyncio.create_task(self.get_data())
#                     tasks.append(task)
#                     time.sleep(2)
#                     page += 1   
#             await asyncio.gather(*tasks)     
async def get_page(page, shard, cat_id):
    url = f'https://catalog.wb.ru/catalog/{shard}/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat={cat_id}&curr=rub&dest=-1257786&page={page}'
    ua = UserAgent(min_percentage=1.3)
    headers = {
    'User-Agent': f'{ua.random}',
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
    async with ClientSession() as s:
        r = await s.get(url, headers=headers)
        print(r.status)
        print(url)
            
async def gather_data():
    for shard, cat_id in dict_info().items():
        page = 1
        url = f'https://catalog.wb.ru/catalog/{shard}/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat={cat_id}&curr=rub&dest=-1257786&page={page}'
        ua = UserAgent(min_percentage=1.3)
        headers = {
        'User-Agent': f'{ua.random}',
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
        tasks = []
        async with ClientSession() as s:
            r = await s.get(url, headers=headers)
            while r.json:
                r = await s.get(url, headers=headers)
                task = asyncio.create_task(get_page(page, shard, cat_id))
                tasks.append(task)
                page += 1
                time.sleep(0)
            await asyncio.gather(*tasks)
                
                

        
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
    # pages_item = [Async_parser(f'{name}', value) for name, value in dict_info.items()]
    return dict_info           
        
        
        

async def main():
    await gather_data()
        #print(item)
        #print(item.info)
    
#         print(key, " ", value, '\n')
    
                    
    
if __name__ == '__main__':
    asyncio.run(main())      