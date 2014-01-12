# Class Fact
import hashlib
class Fact(object):

    def __init__(self, f = ""):
        self.fact_type = "T" 
        self.Fact = f
    
    def __hash__(self):
        return int(hashlib.md5(self.Fact.encode()).hexdigest(),16)
        
        
    def content(self):
        return self.Fact + "LL" 




