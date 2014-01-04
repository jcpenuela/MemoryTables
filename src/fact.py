# Class Fact

import hashlib
import random


class Fact(object):

    def __init__(self, f = ""):
        self.fact_rk = random.random()
        self.fact_type = "T" 
        self.Fact = f
        self.fact_hk = hashlib.md5(f.encode('utf-8')).hexdigest()
    
    def set_fact(self, f):
        self.Fact = f
        self.fact_hk = hashlib.md5(f.encode('utf-8')).hexdigest()
    
    def content(self):
        return self.Fact 

if __name__ == '__main__':
    f = Fact("A")
    print(f.content())




