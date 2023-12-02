import json

class Json_write():
    
    def __init__(self, name_cat, json=''):
        self.name_cat = name_cat
        self.json = json
    
    def loads_json(self, page):
        self.json = json.loads(page)
    
    def write_json(self):
        symb = '\/-., '
        name = self.name_cat
        for sym in symb:
            if sym in name:
                name = name.replace(sym,'_')
        with open (f'data/{name}.json', 'w', encoding="utf-8") as f:
            json.dump(self.json, f, ensure_ascii=False, indent=4)
            
    def write_json_s(self):
        
        with open (f'data/{self.name_cat}.json', 'w', encoding="utf-8") as f:
            f.write(json.dumps(self.json, ensure_ascii=False, indent=4))