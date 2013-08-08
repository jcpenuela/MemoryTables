'''
Created on 08/08/2013

@author: jcpenuela
'''
import copy
import MemoryListIndex as ix


class MemoryListTable(object):
    
    def __init__(self):
        self.elements = dict()     # nodes in memory 
        self.next_element_id = 1       # next free id out of free list
        self.index_list = dict()
        
        self.hk_index = ix.MemoryListIndex('contenido')

    def __getitem__(self, key):
        return self.get_element(key,False)
#    def __setitem__(self, key, value):
#        pass       
    def __delitem__(self, key):
        return self.remove_element(key)
           
    def __iter__(self):
        return iter(self.elements)
    
    

    def get_next_element_id(self):
        '''
        OK
        Obtiene el siguente id
        '''
        new_id = self.next_element_id
        self.next_element_id += 1
        return new_id

    def truncate(self):
        '''
        OK
        Borra el contenido completo de la red
        '''
        self.elements = dict() 
        self.next_element_id = 1       # next free id out of free list
        self.hk_index.clear()

    
    def add_element(self, new_element, referenced=False):
        '''
        OK
        Añade un elemento a la tabla. Devuelve el id de la tabla.
        referenced = True implica que no se almacena una copia del elemento,
        sino una referencia al elemento pasado (en el caso de que
        sea un elemento referenciao, objeto, lista, etc...)
        '''
        new_id = self.get_next_element_id()
        if not referenced:
            n = copy.deepcopy(new_element)
            self.elements[new_id] = n
        else:
            self.elements[new_id] = new_element
        return new_id


    def get_element(self, node_id, referenced=False):
        '''
        OK
        Recupera un elemento por el id
        referenced = True implica que recupera una referencia al elemento
        en lugar de una copia. Eso permite modificar el objeto que se recupera
        directamente (si es referenciado)
        '''

        if node_id in self.elements:
            if not referenced:
                e = copy.deepcopy(self.elements[node_id])
                return e
            else:
                return self.elements[node_id]
        else:
            return None


    def delete_element(self, node_id):
        '''
        OK
        Elimina el nodo de la red
        '''
        if node_id in self.elements:
            del(self.elements[node_id])
            return True
        else:
            return False


    def update_element(self, new_element, id, referenced=False):
        '''
        OK
        Sustituye un nodo en la red. El nodo debe llevar su id alimentado para localizarse en la red.
        Retorna el id del nodo
        '''
        if id not in self.elements:
            raise Exception('MemoryListTable.update_element','Element ID non existent in table')
        
        # Actualizar en la red
        if not referenced:
            n = copy.deepcopy(new_element)
            self.elements[id] = n
        else:
            self.elements[id] = new_element
        return id


    def count(self):
        '''
        OK
        '''
        return len(self.elements)


    def get_elements_list_by(self, att, value, referenced=False):
        '''
        Recupera una copia de la lista de ids de nodos cuyo hk coincide con el pasado
        None en caso contrario
        '''
        if att not in self.index_list:
            raise Exception('MemoryListTable.get_element_by','Att [' + att + '] must be indexed' )
        
        if value not in self.index_list[att]:
            return None
        
        return self.index_list[att][value]
        
         
    def index_by(self, att):
        '''
        '''
        if att in self.index_list:
            raise Exception('MemoryListTable.add_index','Adding an already existing index')
        
        
        self.index_list[att] = dict()
        








    
    
    def reindex(self, att=None):
        if not att:
            for i in self.index_list:
                self.reindex(i)
        else:
            self.index_list[att] = dict()
            for element in self.elements:
                pass
            
    def list_nodes(self):
        print('Lista de nodos: ', len(self.elements))
        for n in self.elements:
            print('id:', n, ' hk:', self.elements[n].node_hk , ' cont:', self.elements[n], ' o:', self.elements[n].out_connections, ' i:', self.elements[n].in_connections)
            
    def dump_index(self):
        '''
        '''
        self.hk_index.dump()

    
    

if __name__ == '__main__':
    red = MemoryListTable()
    red.test()

        