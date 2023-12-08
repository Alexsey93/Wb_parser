import requests
import os
import shutil
import time
from src.modules import Items
from src.modules import json
from src.modules import postgresql

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
    
    def make_folder(self):
        folder = "data"
        if os.path.exists(folder) == True:
            print("Найдена папка, хотите перезаписать?")
            if input("Если да, введите Y, если нет, введите N ") == "Y":
                shutil.rmtree(folder)
                os.mkdir(folder)
        else:
            os.mkdir(folder)
            print(f'{folder}')

                

def main():
    start_time = time.time()
    url = 'https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json'
    cat = Parser(url, HEADERS_WB)
    cat.make_folder()
    cat_json = json.Json_funct()
    cat_json.loads_json(cat.get_page())
    #print(cat_json.json)
    db = postgresql.Psql_db('wb_parser', 'alex', 'afbdogs', '212.26.248.159')
    db.create_database()
    field_table = (f"json json")
    db.create_table('cat_json', field_table)
    current_time = time.time()
    print(f'[INFO] прошло времени: {time.gmtime(current_time - start_time)[3]} ч : {time.gmtime(current_time - start_time)[4]} мин : {time.gmtime(current_time - start_time)[5]} сек')  
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
    
                    
    
        