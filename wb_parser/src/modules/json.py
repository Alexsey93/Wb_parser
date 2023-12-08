import json

class Json_funct():
    
    def __init__(self):
        self.json = {}
    
    def loads_json(self, page):
        self.json = json.loads(page)