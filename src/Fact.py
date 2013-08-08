# Class fact

import hashlib
import random


class Fact(object):

    def __init__(self, f = ""):
        self.fact_rk = random.random()
        self.fact_type = "T" 
        self.fact = f
        self.fact_hk = hashlib.md5(f.encode('utf-8')).hexdigest()
    
    def set_fact(self, f):
        self.fact = f
        self.fact_hk = hashlib.md5(f.encode('utf-8')).hexdigest()
    
    def content(self):
        return self.fact 

if __name__ == '__main__':
    f = Fact("A")
    print(f.content())




