import requests
import time
from pydantic import BaseModel 

class pars_item(BaseModel):
    name : str
    price : int
    brand : str
    

class Items_json():
    
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
            max_retry = 10      
            page = 1
            r = session.get(f'https://catalog.wb.ru/catalog/{self.shard}/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat={self.cat_id}&curr=rub&dest=-1257786&page={page}')
            for ret in range(max_retry):
                time.sleep(0.2)
                while True:
                    try:
                        r = session.get(f'https://catalog.wb.ru/catalog/{self.shard}/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat={self.cat_id}&curr=rub&dest=-1257786&page={page}')
                        #print(r.text)
                        print(f'категория --- {self.shard} --- страница в категории --- {page} --- {r.status_code} -- {type(self.info)}\n')
                        page += 1
                        #print(r.json()['data']['products'])
                        self.info.append(r.json().get('data').get('products'))
                        time.sleep(0.2)
                    except Exception as ex:
                        print(f'Возникла ошибка {ex}\n')
                        print(f'попытка подключения {ret} из {max_retry} вероятно достигнут конец пагинации\n')
                        page -= 1
                        break
            print(f'Переход к следующей категории\n')
                        
                    
                #time.sleep(0.5)
    