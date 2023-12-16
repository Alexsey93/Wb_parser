import requests
import os
import shutil
import time
from src.modules import Items
from src.modules import json
from src.modules import postgresql
import csv
from psycopg2.extras import Json

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
        self.db = postgresql.Psql_db('wb_parser', 'alex', 'afbdogs', '212.26.248.159')
        self.create_db('wb_json','id SERIAL PRIMARY KEY, wb_cat_json jsonb')
        self.start_time = time.time()
        
    def get_page(self):
        return requests.get(self.__url, self.__header).text
    
    def get_data_json(self):
        self.cat_json = json.Json_funct()
        self.cat_json.read_json(self.get_page())
        return self.cat_json.data_json
    
    def create_db(self, name_table, fields):
        self.db.create_database()
        self.db.create_schemas('public')
        self.db.create_schemas('item_pages')
        self.db.create_schemas('items_info')
        self.db.create_table(name_table, fields)
        self.db.create_table('cat_info',('id SERIAL PRIMARY KEY,shard_cat varchar,id_cat integer UNIQUE, name_cat varchar, url varchar'))
        print(f'БД и таблицы созданы')  
    
    def add_json_cat_to_bd(self):
        self.db.json_to_db(self.get_data_json(), 'wb_json', 'wb_cat_json','', unique_field='id', update_field='wb_cat_json')
        self.wb_items = Items.Items_json(self.get_json_cat())
    
    def get_json_cat(self):
        self.cat_data = self.db.db_to_json('wb_cat_json', 'wb_json')
        return self.cat_data
        
    def get_cat_data(self):
        self.wb_items.cat_info(self.cat_data)
        self.cat_json_data = self.wb_items.dict_info_cat
        
    def create_cat_info(self):
        self.get_cat_data()
        for name_cat, info in self.cat_json_data.items():
            self.db.set_sql_request(f"INSERT INTO cat_info (shard_cat,id_cat,name_cat,url) VALUES ('{name_cat}',{info[0]},'{info[1]}','{info[2]}') ON CONFLICT (id_cat) DO NOTHING;")
    
    def add_page_cat_to_bd(self):
        pages_list = ''
        values_list = []
        symb = f'\"-=+,./\\ \''
        self.get_cat_data()
        for name_cat, id_cat in self.cat_json_data.items():
            temp = self.wb_items.get_info(name_cat, id_cat)
            self.db.create_table(f"item_pages.{name_cat}",('id SERIAL PRIMARY KEY, json_page jsonb'))
            for page_data, values in temp.items():
                values_list.append(values)
            self.db.json_to_db_many(json_sql=values_list, table_name=f"item_pages.{name_cat}", column_name='json_page', unique_field='id', update_field='json_page')
            values_list = []
            temp = {}
            print(f'Выполнена вставка категории {name_cat}')
            current_time = time.time()
            print(f'[INFO] прошло времени: {time.gmtime(current_time - self.start_time)[3]} ч : {time.gmtime(current_time - self.start_time)[4]} мин : {time.gmtime(current_time - self.start_time)[5]} сек')   
            
    def parse_info_to_item(self):
        sql_values = ''
        symb = f'\"-=+,./\\ \'!'
        self.get_cat_data()
        for name_cat, id_cat in self.cat_json_data.items():
            self.db.create_table(f'items_info.items_{name_cat}',('id_item INTEGER PRIMARY KEY,name_item varchar'))
            items = self.db.get_sql_response(f"SELECT json_page FROM item_pages.{name_cat};")
            for item in items:
                for i in item:
                    for k in i:
                        name_brand = k['brand']
                        name_item = k['name']
                        for s in symb:
                            if s in name_item:
                                name_item = name_item.replace(s,'_')
                            if s in name_brand:
                                name_brand = name_brand.replace(s,'_')
                        #sql_request.append(f"INSERT INTO items_info.items_{name_cat} (id_item,name_item) VALUES ('{k['id']}','{name_item}') ON CONFLICT (id_item) DO NOTHING;")
                        sql_values = sql_values + (f"('{k['id']}', '{name_item}'),")
            sql_request = f"INSERT INTO items_info.items_{name_cat} (id_item,name_item) VALUES {(sql_values)} ON CONFLICT (id_item) DO NOTHING;"
            tmp = list(sql_request)
            del tmp[-35]
            sql_request = ''.join(tmp)
            #print(sql_request)
            self.db.set_sql_request(sql_request)
            sql_request = ''
            sql_values = ''
            #print(sql_request)
            
    
    # def csv_writer():
    #     pass        

def main():
    symb = f'\"-=+,./\\ \''
    start_time = time.time()
    wb_parser = Parser(URL, HEADERS_WB)
    wb_parser.add_json_cat_to_bd()
    wb_parser.create_cat_info()
    if input('хотите обновить данные для внесения в БД? Введите Y') == 'Y':
        wb_parser.add_page_cat_to_bd()
    wb_parser.parse_info_to_item()
    current_time = time.time()
    print(f'[INFO] прошло времени: {time.gmtime(current_time - start_time)[3]} ч : {time.gmtime(current_time - start_time)[4]} мин : {time.gmtime(current_time - start_time)[5]} сек')  

if __name__ == '__main__':
    main()
    
                    
    
        