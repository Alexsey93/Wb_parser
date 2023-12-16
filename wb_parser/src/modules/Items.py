import requests
import time
from pydantic import BaseModel 
import json

class Items_json():
    
    def __init__(self, sql_response):
        self.sql_response = sql_response
        self.dict_info_cat = {}
            
    @staticmethod    
    def get_info(name_cat, id_cat):
        info = {}
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
            max_retry = 15      
            page = 1
            for retry in range(max_retry):
                time.sleep(0.2)
                while True:
                    try:
                        response = session.get(f'https://catalog.wb.ru/catalog/{name_cat}/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat={id_cat[0]}&curr=rub&dest=-1257786&page={page}')
                        info[str(page)] = (response.json().get('data').get('products'))
                        page += 1
                    except Exception as exeption:
                        break
        return info
                    
    def cat_info(self, sql_response):
        symb = f'\"-=+,./\\ \''
        sql_json = json.loads(json.dumps(sql_response))
        for childs in sql_json[0]:
            if 'childs' in childs:
                for childs_2l in childs['childs']:
                    if 'childs' in childs_2l:
                        for childs_3l in childs_2l['childs']:
                            if 'childs' in childs_3l:
                                #print('достигнут 3 уровень, имеется 4')
                                for childs_4l in childs_3l['childs']:
                                    if 'childs' in childs_4l:
                                        #print('достигнут 4 уровень, имеется 5')
                                        for childs_5l in childs_4l['childs']:
                                            if 'childs' in childs_5l:
                                                print('достигнут 5 уровень , имеется 6')
                                            else:
                                                shard = childs_5l['shard']
                                                name = childs_5l['name']
                                                url = childs_5l['url']
                                                for s in symb:
                                                    if s in shard:
                                                        shard = shard.replace(s,'_')
                                                self.dict_info_cat[shard] = childs_5l['id'], name, url
                                    else:
                                        shard = childs_4l['shard']
                                        name = childs_4l['name']
                                        url = childs_4l['url']
                                        for s in symb:
                                            if s in shard:
                                                shard = shard.replace(s,'_')
                                        self.dict_info_cat[shard] = childs_4l['id'], name, url
                            else:
                                if 'shard' in childs_3l:
                                    shard = childs_3l['shard']
                                    name = childs_3l['name']
                                    url = childs_3l['url']
                                    for s in symb:
                                        if s in shard:
                                            shard = shard.replace(s,'_')
                                    self.dict_info_cat[shard] = childs_3l['id'], name, url
                    else:
                        if 'shard' in childs_2l:
                            shard = childs_2l['shard']
                            name = childs_2l['name']
                            url = childs_2l['url']
                            for s in symb:
                                if s in shard:
                                    shard = shard.replace(s,'_')
                            self.dict_info_cat[shard] = childs_2l['id'], name, url
            else:
                if 'shard' in childs:
                    shard = childs['shard']
                    name = childs['name']
                    url = childs['url']
                    for s in symb:
                        if s in shard:
                            shard = shard.replace(s,'_')
                    self.dict_info_cat[shard] = childs['id'], name, url
