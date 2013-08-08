'''
Created on 07/08/2013

Clase para índices de nodos en la red

@author: jcpenuela
'''

class MemoryListIndex(object):
    '''
    Índice de nodos
    Cada índice tiene su clave y una lista de ids
    '''
    

    def __init__(self, indexname=''):
        '''
        Constructor
        '''
        self.index = dict() # list of nodes
        self.indexname = indexname
        pass
    
    def clear(self):
        self.index = dict()
    
    def locate(self, key):
        if key in self.index:
            return self.index[key]
        else:
            return None
    
    def add(self, key, value):
        '''
        Añade el value al índice por clave key
        '''
        if key in self.index:
            if value not in self.index[key]:
                self.index[key].append(value)
        else:
            self.index[key] = [value]
        return key
        
    def delete(self, key, value):
        '''
        Elimina el value de la clave
        '''
        if key in self.index:
            if value in self.index[key]:
                if len(self.index[key]) == 1:
                    del(self.index[key])
                else:
                    self.index[key].remove(value)
            return key
        else:
            return None
        
    def update(self, key, old_key, value):
        '''
        '''
        if key == old_key:
            return key
        
        if key in self.index:
            if value not in self.index[key]:
                self.index[key].append(value)
        else:
            self.index[key] = [value]

        if old_key in self.index:
            if value in self.index[old_key]:
                self.index[old_key].remove(value)
                if len(self.index[old_key]) == 0:
                    del(self.index[old_key])
                    
        return key
            
    def dump(self):
        '''
        '''
        for key in self.index:
            print(key, self.index[key])

if __name__ == '__main__':
    memory_list_index = MemoryListIndex()
    
       
        
        