import requests
import json
import os
import shutil
import time
from src.modules import Items
from src.modules import write
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
    dict_info_d = {}
    with open ('data/menu.json', encoding="utf-8") as f:
        name = json.load(f)
    #    name.pop(0)
    #print(type(name))    
    for item_cat in name:
        if not('shard' in item_cat):
            if 'childs' in item_cat:
                for child in item_cat['childs']:
                    #print(child, '\n')
                    if 'shard' in child:
                        dict_info_d[child['shard']] = [child['id'],child['name']]
        elif item_cat['shard'] == 'blackhole':
            for child in item_cat['childs']:
                if 'shard' in child:
                    dict_info_d[child['shard']] = [child['id'],child['name']]
    pages_item = [Items.Items_json(f'{name}', value[0]) for name, value in dict_info_d.items()]
    return pages_item, dict_info_d

def main():
    need_info = {}
    make_folder()
    url = 'https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json'
    menu = Parser(url, HEADERS_WB)
    write_menu_json = write.Json_write('menu')
    write_menu_json.loads_json(menu.get_page())
    write_menu_json.write_json()
    start_time = time.time()
    new_db = postgresql.Psql_db('wb_parser', 'alex', 'afbdogs', '212.26.248.159')
    new_db.create_database()
    list_db = []
    for item in dict_info()[0]:
        item.item_info()
        new_db.create_table(item.shard)
        page_json_items = [page_json_item for pages in item.info
                                    for page_json_item in pages]
        for items in page_json_items:
            need_info[items["id"]] = [items["name"],items["brand"]]
        # print(need_info)
        for id, name in need_info.items():
            name_table = item.shard
            symb = ['/','\\','.',' ','-','\'']
            for sym in symb:
                if sym in name[0]:
                    name[0] = name[0].replace(sym,'_')
                if sym in name[1]:
                    name[1] = name[1].replace(sym,'_')
                if sym in name_table:
                    name_table = name_table.replace(sym,'_')
            list_db.append(f"INSERT INTO {item.shard}(id_item, name, brand) VALUES ({id},'{name[0]}','{name[1]}');")
        #print(list_db)
        new_db.insert_data(list_db)
            # new_db.insert_data(id, name[0], name[1])
        need_info = {}
        # all_items[dict_info()[1][item.shard][1]] = page_json_items
        # page_info = write.Json_write(dict_info()[1][item.shard][1], page_json_items)
        # page_info.write_json()
        current_time = time.time()
        print(f'[INFO] прошло времени: {time.gmtime(current_time - start_time)[4]} мин : {time.gmtime(current_time - start_time)[5]} сек : {time.gmtime(current_time - start_time)[6]} мс')
    # global_info_json = write.Json_write('Список всех предметов', all_items)
    # global_info_json.write_json()
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
    
                    
    
        