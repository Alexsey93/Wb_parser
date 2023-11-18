import os
import requests
from string import ascii_letters

COOKIES_WB = {
    '_ym_uid': '1696796575630911011',
    '_ym_d': '1696796575',
    'BasketUID': 'a020881c12ce4b6ab33dff73d9cf4293',
    '___wbu': '9c2e13ff-c415-4ada-9bad-834ff55e6355.1698750848',
    '_wbauid': '10161437551698750848',
    '__wba_s': '1',
    '___wbs': 'b1740dc5-cf28-460c-9d51-9cbf955c8fe9.1700312845',
}

HEADERS_WB = {
    'authority': 'www.wildberries.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': '_ym_uid=1696796575630911011; _ym_d=1696796575; BasketUID=a020881c12ce4b6ab33dff73d9cf4293; ___wbu=9c2e13ff-c415-4ada-9bad-834ff55e6355.1698750848; _wbauid=10161437551698750848; __wba_s=1; ___wbs=b1740dc5-cf28-460c-9d51-9cbf955c8fe9.1700312845',
    'if-modified-since': 'Thu, 16 Nov 2023 08:38:40 GMT',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

class Parser():
      
    def __init__(self, *args, **kwargs):
        
        self.url = args[0]
        self.header = args[1]
        self.cookie = args[2]
        self.retrv = args[3]
        
    @classmethod
    def verify_url(self, url):
        if type(url) != str:
            raise TypeError("адрес должен быть строкой")
        if not('https://' in url) and not('http://' in url):
            raise TypeError("ошибка в адресе")
        if len(url.strip(ascii_letters + '://.')) != 0:
            raise ValueError("адрес содержит кирилицу")
        
    @property
    def url(self):
        return self.__url
    
    @url.setter
    def url(self, url):
        self.verify_url(url)
        self.__url = url       
    
    @property
    def header(self):
        return self.__header 
    
    @header.setter
    def header(self, header):
        self.__header = header   
    
    @property
    def cookie(self):
        return self.__cookie
    
    @cookie.setter
    def cookie(self, cookie):
        self.__cookie = cookie 
        
    @property
    def retrv(self):
        return self.__retrv
    
    @retrv.setter
    def retrv(self, retrv):
        self.__retrv = retrv 
        
    def get_response(self):
        s = requests.Session()
        self.__r = s.get(url=self.__url,headers=self.__header,cookies=self.__cookie)
        self.__r = self.__r.text
    
    def write_page(self):
        with open ('index.html', 'w') as file:
            file.write(self.__r)
    
    
        

        
p = Parser('https://google.com',HEADERS_WB, COOKIES_WB, 5)
p.get_response()
print(p.write_page())