import requests
import time


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
                    print(f'Переход к следующей категории\n')
                    break
                time.sleep(0.5)
    