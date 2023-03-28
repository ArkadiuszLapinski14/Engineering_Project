class Views():
    def __init__(self):
        self.views={}
        
    def register(self,name,f):
        self.views.update({name:f})

    def getInstance(self,name):
        return self.views[name]()
    
    def getList(self):
        return self.views.keys()