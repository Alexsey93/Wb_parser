class test1():
    
    def __init__(self):
        self.test = 1
        
class test2():
    
    def __init__(self):
        self.test = 2
        
class test3():
    
    def __init__(self):
        self.test = 3
        
class test4():
    
    def __init__(self):
        self.test = 4
        
class test5():
    
    def __init__(self):
        self.test = 5
        
list_test = [test1(),test2(),test3(),test4(),test5()]

for i in list_test:
    print(i.test)