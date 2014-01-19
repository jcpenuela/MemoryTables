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
import dstools


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
        
    
    # TODO: el eval es peligroso si se pasa algo que no sea una lista 
    def select(self, select_expression):
        '''
        selecciona nodos del dataset. Devuelve un diccionario con los nodos
        en formato {id:nodo, id:nodo,..., id:nodo}
        expresión de query un diccionario
        {'r':'expresión python búsqueda'}
        
        { "persona": "persona.ciudad in ('Sevilla','Huelva') and persona.edad >= 30" }
        { "@indice": "['andrés','luís']" }
        { "#id" : "[123,34,55}" }
        
        '''
        if isinstance(select_expression, dict) == False:
            raise Exception('Dataset.select()','Query must be a dictionary')
        
        
        # La búsqueda puede ser:
        #    - Por id : #
        #    - Por índice : @
        #    - Por expresión a aplicar a cada nodo: $ / campo 
        search_for = ''
        
        lvalue = list(select_expression.keys())[0]
        rvalue = list(select_expression.values())[0]
        
        nodes_selected = dict()
        
        if lvalue[0] == '#':
            # hay búsqueda por ids. Da lo mismo el resto...
            # devolvemos todos los que
            if isinstance(rvalue,str):
                nodes_ids = eval(rvalue)
            else:
                nodes_ids = rvalue
                
            if isinstance(nodes_ids,int):
                nodes_ids = [nodes_ids]
                
            if (isinstance(nodes_ids,list) or isinstance(nodes_ids,set) or isinstance(nodes_ids,tuple)) == False:   
                raise Exception('Dataset.select()','RVALUE is not in list or int format')
        
            for node_id in nodes_ids:
                try:
                    nodes_selected[node_id] = self.nodes[node_id]
                except KeyError:
                    pass
                except:
                    raise
        
            return nodes_selected
        
        if lvalue[0] == '@':
            # la búsqueda es por índices
            # devolvemos todos los que estén en el index
            index_name = lvalue[1:]
            if isinstance(rvalue,str):
                index_values = eval(rvalue)
            else:
                index_values = rvalue
                
            if index_name not in self.indexes:
                raise Exception('Dataset.select()','Index name <' + index_name  + '> do not exist')
            
            if (isinstance(index_values,list) or isinstance(index_values,set) or isinstance(index_values,tuple)) == False:   
                index_values = [index_values]
                
            for index in index_values:
                try:
                    for node_id in self.indexes[index_name][index]:
                        nodes_selected[node_id] = self.nodes[node_id]
                except KeyError:
                    pass
                except:
                    raise           
            return nodes_selected
        
        # Es por expresión
        qfunction = eval("lambda " + lvalue + " : " + rvalue)
        for node_id, node in self.nodes.items():
            # aplicar búsque
            if qfunction(node):
                nodes_selected[node_id]=node
                       
        return nodes_selected
        

    def select2(self, select_expression):
        '''
        selecciona nodos del dataset. Devuelve un diccionario con los nodos
        en formato {id:nodo, id:nodo,..., id:nodo}
        expresión de query un diccionario
        {'r':'expresión python búsqueda'}
        
        { "persona": "persona.ciudad in ('Sevilla','Huelva') and persona.edad >= 30" }
        { "@indice": "['andrés','luís']" }
        { "#id" : "[123,34,55}" }
        
        '''
        
        # Si el parámetro es una función, la utilizamos para cada objeto del dataset
        # Ls función debe devolver True o False para incluir o no el objeto
        if hasattr(select_expression, '__call__'):
            # pasa una lambda para utilizarla
            nodes_selected = dict()
            for node_id, node in self.nodes.items():
            # aplicar búsque
                if select_expression(node):
                    nodes_selected[node_id]=node                      
            return nodes_selected

        # Si no era el caso anterior, debe ser un diccionario con la
        # expresión
        if isinstance(select_expression, dict) == False:
            raise Exception('Dataset.select2()','Query must be a function or formatted dictionary')
        
        
        # La búsqueda puede ser:
        #    - Por id : #
        #    - Por índice : @
        #    - Por expresión a aplicar a cada nodo: $ / campo 
        lvalue = list(select_expression.keys())[0]
        rvalue = list(select_expression.values())[0]
        
        nodes_selected = dict()
        
        if lvalue[0] == '#':
            # hay búsqueda por ids. Da lo mismo el resto...
            # devolvemos todos los que
            if isinstance(rvalue,str):
                nodes_ids = eval(rvalue)
            else:
                nodes_ids = rvalue
                
            if isinstance(nodes_ids,int):
                nodes_ids = [nodes_ids]
                
            if (isinstance(nodes_ids,list) or isinstance(nodes_ids,set) or isinstance(nodes_ids,tuple)) == False:   
                raise Exception('Dataset.select()','RVALUE is not in list or int format')
        
            for node_id in nodes_ids:
                try:
                    nodes_selected[node_id] = self.nodes[node_id]
                except KeyError:
                    pass
                except:
                    raise
        
            return nodes_selected
        
        if lvalue[0] == '@':
            # la búsqueda es por índices
            # devolvemos todos los que estén en el index
            index_name = lvalue[1:]
            if isinstance(rvalue,str):
                index_values = eval(rvalue)
            else:
                index_values = rvalue
                
            if index_name not in self.indexes:
                raise Exception('Dataset.select()','Index name <' + index_name  + '> do not exist')
            
            if (isinstance(index_values,list) or isinstance(index_values,set) or isinstance(index_values,tuple)) == False:   
                index_values = [index_values]
                
            for index in index_values:
                try:
                    for node_id in self.indexes[index_name][index]:
                        nodes_selected[node_id] = self.nodes[node_id]
                except KeyError:
                    pass
                except:
                    raise           
            return nodes_selected
        
        # Es por expresión
        nodes_selected = dstools.select(select_expression, self.nodes)
                       
        return nodes_selected
        



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
            print('id:', n, ' cont:', self.nodes[n], 'hash:', hash(self.nodes[n]))
            
    

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
    
        