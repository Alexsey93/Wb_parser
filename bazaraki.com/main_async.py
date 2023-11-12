from bs4 import BeautifulSoup
import requests 
import json
import os
import aiohttp
import asyncio
import shutil
import time


url = "https://www.bazaraki.com"
headers = {
           "Accept" : "application/json, text/plain, */*",
           "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
           "Cookie" : "csrftoken=8dtnN8eUQvgoakOcLRB1SHeAfzrQDLN01Ka9ESbRtMeNTrO9HS8ZqsR7F9mhLPxJ; sessionid=2dvkmtd6sxh729yt0l6ayzgzop6caorz"
         }

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

def http_session(url, headers=headers, retry=5):
    try:
        s = requests.Session()
        r = s.get(url, headers=headers)
    except Exception as ex:
        time.sleep(5)
        if retry:
            print(f"[INFO] retry={retry} => {url}")
            return http_session(url, retry=(retry-1))
        else:
            print(ex)
            s.close
    else:
        return r.content    
    
def parser_page(url):
    soup = BeautifulSoup(http_session(url), 'lxml')
    return soup
    
def catalog_info(soup):
    dict_categories = {}
    dict_sub_categories = {}
    categories = soup.find_all('div', class_='category-item')
    for category in categories:
        name_category = category.find('p').text
        if category.find('ul') is not None:
            sub_categories = category.find('ul', class_='sub-category-ul').find_all('li')
        for sub_category in sub_categories:
            dict_sub_categories[(sub_category.find('a').text)] = url + sub_category.find('a')["href"]
        dict_categories[name_category] = dict_sub_categories
        dict_sub_categories = {}
    with open ('category_info.json', 'w') as file:
        file = json.dump(dict_categories, file, indent=4, ensure_ascii=False) 
                        
def list_announcements():
    dict_announcements = {}
    with open ('category_info.json') as file:
         cat = json.load(file)    
    for cat_name, sub_cat_info in cat.items():
        for name, link in sub_cat_info.items():
            try:
                max_page = parser_page(link).find_all('a', class_='page-number js-page-filter')[-1].text
                print(max_page)
            except Exception as ex:
                max_page = 0 
                print(max_page, link, ex)           
#   with open ('announcements_info.json', 'w') as file:
#       file = json.dump(dict_announcements, file, indent=4, ensure_ascii=False) 
    
                 
# class Session:
#     def __init__(self, url) -> None:
#         self.url = url
#         self.headers = {
#             "Accept" : "application/json, text/plain, */*",
#             "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
#             "Cookie" : "csrftoken=8dtnN8eUQvgoakOcLRB1SHeAfzrQDLN01Ka9ESbRtMeNTrO9HS8ZqsR7F9mhLPxJ; sessionid=2dvkmtd6sxh729yt0l6ayzgzop6caorz"
#         }
    
#     def get_data (self):
#         r = requests.get(self.url, headers=self.headers)
#         return r.text
    
#     def send_request():
#         pass
#     pass

# def parser_page(url):
#     market = Session(url)
#     return market.get_data()
        
# def parser_cat():
#     os.mkdir('pages')
#     sub_category_info = {}
#     category_info = {}  
#     catalog = BeautifulSoup(parser_page('https://www.bazaraki.com/'), 'lxml')
#     categories = catalog.find_all('div', class_='category-item')
#     for category in categories:
#         name_category = category.find('p').text
#         if category.find('ul' is not None:
#             sub_categories = category.find('ul', class_='sub-category-ul').find_all('li')
#         for sub_category in sub_categories:
#             sub_category_info[(sub_category.find('a').text)] = 'https://www.bazaraki.com' + sub_category.find('a')["href"]
#         category_info[name_category] = sub_category_info
#         sub_category_info = {}
#     with open ('test.json', 'w') as file:
#         file = json.dump(category_info, file, indent=4, ensure_ascii=False)        
# #        print(name_sub_category)
# #        print(name_category.text)

# def parser_announcements():
#     dict_anouncements = {}
#     with open ('test.json') as file:
#         cat = json.load(file)
#         for cat_name, cat_dict in cat.items():
#             for sub_category, link in cat_dict.items():
#                 with open (f'pages/{sub_category}.html', 'w') as file:
#                     file.write(BeautifulSoup(parser_page(f'{link}'), 'lxml').text)
#                 max_page = BeautifulSoup(parser_page(f'{link}'), 'lxml').find_all('a', class_='page-number js-page-filter')[-1].text
#                 print(max_page)
#                 for page in range (1, int(max_page) + 1):
#                     anouncements = BeautifulSoup(parser_page(f'{link}/?page={page}'), 'lxml')
#                     block_anouncements = anouncements.find_all('a', class_='advert__content-title')
#                     for item in block_anouncements:
#                         #dict_anouncements[item.find('a', class_='advert__content-title').text[11:-9:]] = BeautifulSoup(parser_page(f'https://www.bazaraki.com{item.find("a").get("href")}'), 'lxml').find('span', class_='counter-views').text  
#                         try:
#                             if (BeautifulSoup(parser_page(f'https://www.bazaraki.com{item["href"]}'), 'lxml').find('span', class_='counter-views')) is not None:    
#                                 print(page, item["href"], type(BeautifulSoup(parser_page(f'https://www.bazaraki.com{item["href"]}'), 'lxml').find('span', class_='counter-views')))  
#                         except:
#                             print(page, item["href"], 'Ошибка', BeautifulSoup(parser_page(f'https://www.bazaraki.com{item["href"]}'), 'lxml').find('span', class_='counter-views'))
#                         #print(f'ошибка{page}{item}')
def main():
#    make_folder()
    catalog_info(parser_page(url))
    list_announcements()

if __name__ == '__main__':
    main()