class RegisterPanel():
    def __init__(self):
        self.element={}
        
    def register(self,name,f):
        self.element.update({name:f})

    def getInstance(self,name):
        return self.element[name]()
    
    def getList(self):
        return self.element.keys()