'''
Created on 05/01/2014

@author: jcpenuela
'''
import hashlib
class Persona(object):
    def __init__(self, nombre, ciudad = None, edad = None, peso = None):
        self.nombre = nombre
        self.ciudad = ciudad
        self.edad = edad
        self.peso = peso
        
    def __eq__(self, *args, **kwargs):
        return args[0].key == self.key()
    
    def key(self):    
        return str((self.nombre, self.ciudad, self.edad, self.peso)).encode()
    
    def __hash__(self):
        # return int(hashlib.md5(self.key()).hexdigest(),16)
        return int(hashlib.md5(self.key()).hexdigest(),16)

if __name__ == '__main__':
    p = Persona('juan','Sevilla',10,3) # -8717269349345654830
    print(hash(p))