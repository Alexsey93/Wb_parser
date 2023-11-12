from bs4 import BeautifulSoup
import requests 
import json

class Session:
    def __init__(self, url) -> None:
        self.url = url
    
    def get_data (self):
        r = requests.get(self.url)
        return r.text
    
    def send_request():
        pass
    pass

def parser_page(url):
    market = Session(url)
    return market.get_data()
        
def parser_cat():
    sub_category_info = {}
    category_info = {}  
    catalog = BeautifulSoup(parser_page('https://www.bazaraki.com/'), 'lxml')
    categories = catalog.find_all('div', class_='category-item')
    for category in categories:
        name_category = category.find('p').text
        if not (category.find('ul') == None):
            sub_categories = category.find('ul', class_='sub-category-ul').find_all('li')
        for sub_category in sub_categories:
            sub_category_info[(sub_category.find('a').text)] = 'https://www.bazaraki.com' + sub_category.find('a')["href"]
        category_info[name_category] = sub_category_info
        sub_category_info = {}
    with open ('test.json', 'w') as file:
        file = json.dump(category_info, file, indent=4, ensure_ascii=False)        
#        print(name_sub_category)
#        print(name_category.text)

def parser_announcements():
    dict_anouncements = {}
    with open ('test.json') as file:
        cat = json.load(file)
        for cat_name, cat_dict in cat.items():
            for sub_category, link in cat_dict.items():
                max_page = BeautifulSoup(parser_page(f'{link}'), 'lxml').find_all('a', class_='page-number js-page-filter')[-1].text
                print(max_page)
                for page in range (1, int(max_page) + 1):
                    anouncements = BeautifulSoup(parser_page(f'{link}/?page={page}'), 'lxml')
                    block_anouncements = anouncements.find_all('div', class_='advert js-item-listing')
                    for item in block_anouncements:
                        #dict_anouncements[item.find('a', class_='advert__content-title').text[11:-9:]] = BeautifulSoup(parser_page(f'https://www.bazaraki.com{item.find("a").get("href")}'), 'lxml').find('span', class_='counter-views').text  
                        try:
                            print(BeautifulSoup(parser_page(f'https://www.bazaraki.com{item.find("a", class_="advert__content-title").get("href")}'), 'lxml').find('span', class_='counter-views').text)  
                        except:
                            print(f'ошибка{page}{item}')
if __name__ == '__main__':
    parser_cat()
    parser_announcements()