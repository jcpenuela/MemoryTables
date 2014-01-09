'''
Created on 08/08/2013

@author: jcpenuela
'''


# TODO: Métodos que cada objeto debe incorporar:
# obj.__hash__() => Llamada cuando hash(objeto)
# obj.__eq__() => llamada cuando objeto1 == objeto2

import copy
import pickle
# import types
# import MemoryListIndex as ix
import fact
import index


class Dataset(object):
    
    def __init__(self):
        self.next_element_id = 1    # siguiente id libre 
        self.nodes = dict()     # objetos en memoria { object_id : object }
        self.indexes = dict() # índices { index_name : DatasetIndex object }
        # Crea los índices internos
        i = index.DatasetIndex('_hash', self.objects_list, 'hash')
        self.indexes['_hash']=i

    def __getitem__(self, key):
        '''
        Devuelve un nodo por su clave
        '''
        return self.get_element(key,False)

    def __delitem__(self, key):
        '''
        Borra un nodo interno por su clave
        '''
        return self.remove_element(key)
           
    def __iter__(self):
        '''        
        Devuelve un iterador con los nodos del dataset
        '''
        return iter(self.nodes)

    def _get_next_element_id(self):
        '''
        Obtiene el siguente id interno de nodo
        '''
        new_id = self.next_element_id
        self.next_element_id += 1
        return new_id

      
    def truncate(self, drop_indexes = False, reset_ids = True):
        '''
        Borra el contenido completo del dataset
        drop_indexes (deafult False). Si True -> elmina los índices
        reset_ids (default True). Si True -> reinicia los ids, comienza por 1 otra vez
        '''
        self.nodes = dict()
        
        if drop_indexes:
            self.indexes = dict()
            i = index.DatasetIndex('_hash', self.objects_list, 'hash')
            self.indexes['_hash']=i
        else:
            for inx in self.indexes:
                inx.truncate()
                
        if reset_ids:
            self.next_element_id = 1       # next free id out of free list
        


    def add(self, new_node, referenced = False):
        '''
        - Añade un elemento a la tabla. Devuelve el id de la tabla.
        - Verifica si el elemento existe ya, si es así no inserta, sino que
        localiza el id y lo devuelve.
        - referenced = True implica que no se almacena una copia del elemento,
        sino una referencia al elemento pasado (en el caso de que
        sea un elemento referenciado, objeto, lista, etc...)       
        '''
        
        h = hash(new_node)
        
        # Comprueba si ya existe el nodo
        if h in self.index_list['_hash']['keys']:
            # Localizar un id y mandarlo de vuelta
            nodes_id_list = self.index_list['_hash']['keys'][h]
            for node_id in nodes_id_list:
                # los nodos deben implementar __eq__
                if new_node == nodes[node_id]:
                    return node_id
        
        # No hay nodo igual al que se quiere insertar, 
        # aunque pueda tener el mismo hash, aparentemente es distinto
        new_id = self._get_next_element_id()
        if not referenced:
            n = copy.deepcopy(new_node)
            self.nodes[new_id] = n
        else:
            self.nodes[new_id] = new_element
    
        # indexar elemento recien insertado
        self._index_nodes({new_id:new_node})
        
        return new_id

    
    def _index_nodes(self, nodes):
        '''
        agrega los nodos 'nodes' a todos los índices 
        '''        
        for index_name, index in self.indexes.items():
            self.indexes[index_name].index(nodes)
    

    def index_by(self, index_name, index_expression):
        '''
        Crea un índice llamado 'index_name' por una 'index_expression'
        No admite el uso de índices reservados '_<nombre_indice>'
        Devuelve una tupla (número de claves, número de nodos indexados)
        '''
        if index_name[0] = '_':
            # se levanta excepción
            raise Exception('Dataset.index_by()','Reserved index name used')
        
        if index_name in self.indexes:
            # el nombre ya existe
            raise Exception('Dataset.index_by()','Index name is in use')
            
        new_index = index.DatasetIndex(index_name, self.nodes, index_expression)
        self.indexes[index_name] = new_index
        
        # retornamos el número de claves y de nodos del nuevo índice
        return new_index.nkeys, new_index.nitems
        
        
    
    
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


    def delete_element(self, element_id):
        '''
        OK
        Elimina el elemento de la red
        '''
        self.unindex_element(element_id)
        if element_id in self.elements:
            del(self.elements[element_id])
            return True
        else:
            return False


    def update_element(self, new_element, id_element, referenced=False):
        '''
        OK
        Sustituye un nodo en la red. El nodo debe llevar su id alimentado para localizarse en la red.
        Retorna el id del nodo
        '''
        if id_element not in self.elements:
            raise Exception('Dataset.update_element','Element ID non existent in table')
        
        # elimino las entradas de índices
        self.unindex_element(id_element)
        
        # Actualizar en la red
        if not referenced:
            n = copy.deepcopy(new_element)
            self.elements[id_element] = n
        else:
            self.elements[id_element] = new_element
        
        # indexo el nuevo elemento
        self.index_element(id_element)    
        return id_element
    

    def count(self):
        '''
        Devuelve el número de nodos
        '''
        return len(self.nodes)


    
    
        
        
            
    def dump_data(self):
        print('Lista de elementos: ', len(self.elements))
        print('Índices: ')
        for index_name in self.index_list:
            print('   - ' + index_name + ': ' + \
                  self.index_list[index_name]['exp'] + ' | ' + \
                  self.index_list[index_name]['original_exp'])
            for key in self.index_list[index_name]['keys']:
                print('         [' + str(key) + ']:' + str(self.index_list[index_name]['keys'][key]))
        print('Elementos: ')
        for n in self.elements:
            print('id:', n, ' cont:', self.elements[n])
            
    

if __name__ == '__main__':
    t = Dataset()
        
    f = fact.Fact("uno")
    t.add(f)
    f = fact.Fact("dos")
    t.add(f)
    f = fact.Fact("tres")
    t.add(f)

    t.index_by('hecho', '.content()')

    print(t.select_elements_order_by_ix('_insert', referenced=True))
    print(t.select_elements_order_by_ix('_content', referenced=True))
    print(t.select_elements_order_by_ix('hecho', referenced=True))

    t.dump_data()
        