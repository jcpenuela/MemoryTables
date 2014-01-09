'''
Created on 08/08/2013

@author: jcpenuela
'''


# TODO: Métodos que cada objeto debe incorporar:
# obj.__hash__() => Llamada cuando hash(objeto)
# obj.__eq__() => llamada cuando objeto1 == objeto2

import copy
import types
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
        i = index.DatasetIndex('_hash', self.nodes, 'hash')
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
        

    def insert(self, new_node, referenced = False):
        '''
        - Añade un elemento a la tabla. Devuelve el id insertado 
          para el nodo
        - Verifica si el elemento existe ya, si es así no inserta, sino que
          localiza el id y lo devuelve.
        - referenced = True implica que no se almacena una copia del elemento,
          sino una referencia al elemento pasado (en el caso de que
          sea un elemento referenciado, objeto, lista, etc...)       
        '''
        
        h = hash(new_node)
        
        # Comprueba si ya existe el nodo
        if h in self.indexes['_hash'].keys:
            # Localizar un id y mandarlo de vuelta
            nodes_id_list = self.indexes['_hash'].keys[h]
            for node_id in nodes_id_list:
                # los nodos deben implementar __eq__
                if new_node == self.nodes[node_id]:
                    return node_id
        
        # No hay nodo igual al que se quiere insertar, 
        # aunque pueda tener el mismo hash, aparentemente es distinto
        new_id = self._get_next_element_id()
        if not referenced:
            n = copy.deepcopy(new_node)
            self.nodes[new_id] = n
        else:
            self.nodes[new_id] = new_node
    
        # indexar elemento recien insertado
        self._index_nodes({new_id:new_node})
        
        return new_id
    
    
    def _index_nodes(self, nodes):
        '''
        agrega los nodos 'nodes' a todos los índices 
        '''        
        for index_name, index in self.indexes.items():
            self.indexes[index_name].index(nodes)
    

    def index(self, index_name, index_expression):
        '''
        Crea un índice llamado 'index_name' por una 'index_expression'
        No admite el uso de índices reservados '_<nombre_indice>'
        Devuelve una tupla (número de claves, número de nodos indexados)
        '''
        if index_name[0] == '_':
            # se levanta excepción
            raise Exception('Dataset.index()','Reserved index name used')
        
        if index_name in self.indexes:
            # el nombre ya existe
            raise Exception('Dataset.index()','Index name is in use')
            
        new_index = index.DatasetIndex(index_name, self.nodes, index_expression)
        self.indexes[index_name] = new_index
        
        # retornamos el número de claves y de nodos del nuevo índice
        return new_index.nkeys, new_index.nitems
        
        
    def select(self, select_expression):
        '''
        selecciona nodos del dataset.
        expresión de query en json, similar a mongodb
        http://docs.mongodb.org/manual/reference/operator/query/
        '''
        if isinstance(select_expression, dict) == False:
            raise Exception('Dataset.select()','Query must be a dict instance')
        
        print()
        print('SELECT EXPRESSION: ', select_expression)
        nodes = dict()
        # t.select({'fact':{'$in':['uno','dos']}})
        print('Hay ', len(select_expression), 'elementos en la expresión de consulta')
        for lvalue, rvalue in select_expression.items():
            print('LVALUE:', lvalue, 'RVALUE:', rvalue)
            if lvalue[0] in ('$','_','#'):
                print('es operador, dato reservado o refiere a índice') 
            else:
                print('es comparación directa')
        
        return nodes
        
        
        
        
        
    
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
        print('Lista de elementos: ', len(self.nodes))
        print('Índices: ')
        for index_name in self.indexes:
            print('   - ' + index_name + ': ' + \
                  self.indexes[index_name].index_expression + ' | ' + \
                  self.indexes[index_name].expression_type)
            for key in self.indexes[index_name].keys:
                print('         [' + str(key) + ']:' + str(self.indexes[index_name].keys[key]))
        print('nodos: ')
        for n in self.nodes:
            print('id:', n, ' cont:', self.nodes[n])
            
    

if __name__ == '__main__':
    t = Dataset()
    f = fact.Fact("uno")
    t.insert(f)
    f = fact.Fact("dos")
    t.insert(f)
    f = fact.Fact("tres")
    t.insert(f)

    t.index('hecho', 'content()')

    t.dump_data()
    
    t.select({'fact':{'$in':['uno','dos']}})
    t.select({'#indice':{'$eq':['uno','dos']}})
    t.select({'_indice':1, '#indice':'valor'})
    
        