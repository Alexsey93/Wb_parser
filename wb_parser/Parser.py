import requests
import os
import shutil
import time
from src.modules import Items
from src.modules import json
from src.modules import postgresql

URL = 'https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json'
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
time_counter = 0


class Parser():
    
    def __init__(self, url, header):
        self.__url = url
        self.__header = header
        
    def get_page(self):
        return requests.get(self.__url, self.__header).text
    
    def get_data_json(self):
        cat_json = json.Json_funct()
        cat_json.read_json(self.get_page())
        print(f'Получены данные по категориям формата JSON',)
        return cat_json.data_json
    
    def create_db(self, name_table, fields):
        db = postgresql.Psql_db('wb_parser', 'alex', 'afbdogs', '212.26.248.159')
        db.create_database()
        field_table = (f"{fields}")
        print(field_table)
        db.create_table(name_table, fields)
        print(f'БД и таблицы созданы')
        return db   
    # def make_folder(self):
    #     folder = "data"
    #     if os.path.exists(folder) == True:
    #         print("Найдена папка, хотите перезаписать?")
    #         if input("Если да, введите Y, если нет, введите N ") == "Y":
    #             shutil.rmtree(folder)
    #             os.mkdir(folder)
    #     else:
    #         os.mkdir(folder)
    #         print(f'{folder}')
            





def main():
    start_time = time.time()
    wb_parser = Parser(URL, HEADERS_WB)
    json_data = wb_parser.get_data_json()
    db = wb_parser.create_db('wb_json','id SERIAL PRIMARY KEY, wb_cat_json jsonb')
    db.json_to_db(json_data, 'wb_json', 'wb_cat_json','')
    cat_data = db.db_to_json('wb_cat_json', 'wb_json')
    db.create_table('item_cat',('id SERIAL PRIMARY KEY, name_cat_item varchar, json_cat jsonb'))
    db.create_table('cat_info',('id SERIAL PRIMARY KEY, id_cat integer UNIQUE, name_cat varchar'))
    db.create_table('item_info',('id SERIAL PRIMARY KEY, id_item integer UNIQUE, name_item varchar, brand_item varchar, price_item integer'))
    wb_items = Items.Items_json(cat_data)
    wb_items.cat_info(cat_data)
    cat_json = wb_items.dict_info_cat
    for name_cat, id_cat in cat_json.items():
        print(name_cat,id_cat)
        db.set_sql_request(f"INSERT INTO cat_info (id_cat,name_cat) VALUES ({id_cat[0]},'{name_cat}') ON CONFLICT (id_cat) DO NOTHING;")
    print(f"Заполнена информация по категориям в БД")
    if input('хотите обновить данные для внесения в БД? Введите Y') == 'Y':
        for name_cat, id_cat in cat_json.items():
            temp = wb_items.get_info(name_cat, id_cat)
            db.json_to_db(json_sql=temp, table_name='item_cat', column_name='name_cat_item,json_cat', values=f"'{name_cat}',")
    current_time = time.time()
    print(f'Создана БД всех предметов')
    
    print(f'[INFO] прошло времени: {time.gmtime(current_time - start_time)[3]} ч : {time.gmtime(current_time - start_time)[4]} мин : {time.gmtime(current_time - start_time)[5]} сек')  
if __name__ == '__main__':
    main()
#         print(key, " ", value, '\n')
    
                    
    
        