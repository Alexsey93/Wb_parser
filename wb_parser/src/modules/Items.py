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
        for cat in sql_json[0]:
            if not('shard' in cat):
                if 'childs' in cat:
                    for child in cat['childs']:
                        if 'shard' in child:
                            name = str(child['shard'])
                            for s in symb:
                                if s in name:
                                    name = name.replace(s,'_')
                            self.dict_info_cat[name] = [child['id'],child['name']]
            elif cat['shard'] == 'blackhole':
                for child in cat['childs']:
                    if 'shard' in child:
                        name = str(child['shard'])
                        for s in symb:
                            if s in name:
                                name = name.replace(s,'_')
                        self.dict_info_cat[name] = [child['id'],child['name']]                           
    