import json

class Json_funct():
    
    def __init__(self):
        self.data_json = {}
    
    def read_json(self, page):
        self.data_json = json.loads(page)
        
    def write_json(self):
        pass