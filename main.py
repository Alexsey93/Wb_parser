import requests 

class Session:
    def __init__(self, url) -> None:
        self.url = url
    
    def get_data (self):
        r = requests.get(self.url)
        return print(r.text)
    
    def send_request():
        pass
    pass

ozon = Session('https://www.wildberries.ru/')
wb = Session('https://www.wildberries.ru/')
wb.get_data()
ozon.get_data()

if __name__ == '__main__':
    wb.get_data()
    ozon.get_data()