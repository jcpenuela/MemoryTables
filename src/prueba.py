'''
Created on 07/01/2014

@author: jcpenuela
'''


import fact
import index

def crea():
    items = dict()
    inxx = index.DatasetIndex('att', items, 'Fact')
    for i in range(0,10):
        o = fact.Fact('A'+str(i))
        print(hash(o), o)
        items[i] = o

    items[2].Fact = items[4].Fact
    
    
    inx = index.DatasetIndex('_hash', items, 'hash')
    
    
    inx2 = index.DatasetIndex('Contenido', items, 'content()')
    inx3 = index.DatasetIndex('att', items, 'Fact')
    inx4 = index.DatasetIndex('atet', items, '"C_" + str(hash(?.content()))')
    
    print(items)
    o = dict()
    o[20] = fact.Fact('B')
    print(o)
    
    inx.index(o)
    inx2.index(o)
    inx3.index(o)
    inx4.index(o)
    inxx.index(o)
    
    print(inx.keys)
    print(inx2.keys)
    print(inx3.keys)
    print(inxx.keys) # vacío... no estoy actualizando
    print(inx4.keys)
    
    for l in inx4:
        print(l, inx4[l])


if __name__ == '__main__':
    crea()