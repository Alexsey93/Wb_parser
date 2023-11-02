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
    with open ('bazaraki_test.html', 'w') as file:
        file.write(market.get_data())
        
def parser_tags():
    sub_category_info = {}
    category_info = {}
    with open ('bazaraki_test.html') as file:
        src = file.read()
#   print(src)    
    soup = BeautifulSoup(src, 'lxml')
    categories = soup.find_all('div', class_='category-item')
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
    print(category_info)
    
if __name__ == '__main__':
    parser_page('https://www.bazaraki.com/')
    parser_tags()