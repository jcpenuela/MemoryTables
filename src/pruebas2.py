'''
Prueba de copiar o referenciar al objeto en la lista
'''

import copy
import pickle

class F(object):
    def __init__(self, dato):
        self.dato = dato

class LF(object):
    def __init__(self):
        self.lista = list()
    def add(self, o, referenciado = False):
        if referenciado:
            self.lista.append(o)
        else:
            nuevo = copy.deepcopy(o)
            self.lista.append(nuevo)

if __name__ == '__main__':
    
    
    f1 = F('original')
    lf = LF()
    
    print(f1.dato)
    lf.add(f1, False)
    # f1 = F('otro original')
    f1.dato = 'Modificado'
    print(f1.dato)
    print(lf.lista[0].dato)
    
    # if not referenced:
    # n = copy.deepcopy(new_element)
    # self.elements[id_element] = n