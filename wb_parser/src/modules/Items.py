import requests
import time
from pydantic import BaseModel 
import json

# class pars_item(BaseModel):
#     name : str
#     price : int
#     brand : str
    

class Items_json():
    
    def __init__(self, sql_response):
        self.sql_response = sql_response
        self.dict_info_cat = {}
        
        
    def get_info(self):
        self.dict_info_cat = self.cat_info(self.sql_response)
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
        for cat, id_cat in self.dict_info_cat.items():
            with requests.Session() as session:
                max_retry = 10      
                page = 1
                r = session.get(f'https://catalog.wb.ru/catalog/{cat}/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat={id_cat[0]}&curr=rub&dest=-1257786&page={page}')
                for ret in range(max_retry):
                    time.sleep(0.2)
                    while True:
                        try:
                            r = session.get(f'https://catalog.wb.ru/catalog/{cat}/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat={id_cat[0]}&curr=rub&dest=-1257786&page={page}')
                            #print(r.text)
                            print(f'категория --- {cat} --- страница в категории --- {page} --- {r.status_code} -- {type(self.info)}\n')
                            page += 1
                            #print(r.json()['data']['products'])
                            self.info[f'{cat}'] = (r.json().get('data').get('products'))
                        except Exception as ex:
                            print(f'Возникла ошибка {ex}\n')
                            print(f'попытка подключения {ret} из {max_retry} вероятно достигнут конец пагинации\n')
                            page -= 1
                            break
            print(f'Переход к следующей категории\n')
                        
                    
                #time.sleep(0.5)
    @classmethod
    def cat_info(self, sql_response):
                sql_json = json.loads(json.dumps(sql_response))
                for cat in sql_json[0]:
                    if not('shard' in cat):
                        if 'childs' in cat:
                            for child in cat['childs']:
                                if 'shard' in child:
                                    print(child, '\n')
                                    self.dict_info_cat[child['shard']] = [child['id'],child['name']]
                    elif cat['shard'] == 'blackhole':
                        for child in cat['childs']:
                            if 'shard' in child:
                                self.dict_info_cat[child['shard']] = [child['id'],child['name']]
                                
    