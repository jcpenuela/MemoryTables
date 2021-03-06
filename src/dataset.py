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
import src.fact as fact
import src.index as index
import src.dstools as dstools
import src.query as query
import src.nodeslinks as nodeslinks


class Dataset(object):
    
    
    def __init__(self, name = None):
        self.next_element_id = 1    # siguiente id libre
        self.name = name
        self.nodes = dict()     # objetos en memoria { object_id : object }
        self.links = dict()   # Lista de conexiones entre nodos
        self.groups = dict()   # Lista de grupos de nodos
        self.indexes = dict() # índices { index_name : DatasetIndex object }
        self.metadata = dict() # metadata del dataset
        self.nodes_metadata = dict() # metadata específica de cada nodo { node_id: { diccionario con metadata (clave, valor)} }
        # Crea los índices internos
        i = index.DatasetIndex('_hash', self.nodes, 'hash')
        self.indexes['_hash']=i

    def __getitem__(self, node_id):
        '''
        Devuelve un nodo por su id
        '''
        return self.nodes[node_id]

    def __delitem__(self, node_id):
        '''
        Borra un nodo interno por su id
        '''
        return self.delete({'#':node_id})
           
    def __iter__(self):
        '''        
        Devuelve un iterador con los nodos del dataset (node_id, node)
        '''
        for i,v in self.nodes.items():
            yield i,v
        # return iter(self.nodes)

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
        

    def insert(self, new_node, force = False, referenced = False):
        '''
        - Añade un elemento a la tabla. Devuelve el id insertado 
          para el nodo
        - Verifica si el elemento existe ya, si es así no inserta, sino que
          localiza el id y lo devuelve.
        - referenced = True implica que no se almacena una copia del elemento,
          sino una referencia al elemento pasado (en el caso de que
          sea un elemento referenciado, objeto, lista, etc...)     
        - El parámetro force indica que, a pesar de que el objeto exista, se
          insertará
        - Se comprobará el tipo del objeto a insertar, ya que si se quiere
          insertar objetos primitivos o tipos que no se puedan realizar
          un hash, se creará un objeto envoltorio para ellos
        '''
        
        # TODO:
        # Se debe ?? comprobará el tipo del objeto a insertar, ya que si se quiere
        #  insertar objetos primitivos o tipos que no se puedan realizar
        #  un hash, se creará un objeto envoltorio para ellos
        
        # TODO: Se podría verificar si un objeto a insertar tiene o no implementado un método __hash__()
        # como añadido, de forma que los que sean clases no primitivas, se controlen y se avise que no
        # se tiene hash() implementado, por lo que no se puede localizar correctamente el dato
        # Y, a ser posible, poner un wrapper que permita crear un hash por nuestra parte
        # (objeto.__hash__.__class__.__name__ == 'method-wrapper') => NO lo tiene implementado
        # (objeto.__hash__.__class__.__name__ == 'method') => SI lo tiene implementado
        h = hash(new_node)
        
        # Vemos si se pide una inserción forzada, en cuyo caso no comprobamos nada,
        # sino que pasamos directamente al proceso de inserción
        if not force:
            # Comprueba si ya existe el nodo
            if h in self.indexes['_hash'].keys:
                # Verificar que realmente es el mismo
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
        for index_name, index in self.indexes.items():
            self.indexes[index_name].index({new_id:new_node})
        
        return new_id
    

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
        
    

    def select(self, select_expression = None):
        '''
        selecciona nodos del dataset. Devuelve un diccionario con los nodos
        en formato {id:nodo, id:nodo,..., id:nodo}
        expresión de query un diccionario
        {'r':'expresión python búsqueda'}
        
        { "persona": "persona.ciudad in ('Sevilla','Huelva') and persona.edad >= 30" }
        { "!indice": "['andrés','luís']" }
        { "#id" : "[123,34,55}" }
        
        '''
        ids_selected = self.select_ids(select_expression)
        nodes_selected = dict()
        for node_id in ids_selected:
            nodes_selected[node_id]=self.nodes[node_id]
        return nodes_selected


    def select_ids(self, select_expression = None):
        '''
        selecciona ids del dataset. Devuelve una lista con los ids
        de los nodos seleccionados según la expresión
        expresión de query un diccionario
        
        ( lambda x: x.ciudad = 'Sevilla' )
        ({ '!indice': ['andrés','luís'] })
        ({ '#id' : [123,34,55] })
        ({ '@ciudad' : ['Sevilla','Huelva'] })
        
        '''
        
        if select_expression == None:
            return self.nodes.keys()
        
        # la expressión de consulta puede venir también en un
        # objeto de tipo query además de en una expresión
        if isinstance(select_expression, query.Query):
            select_expression = select_expression.get_query()
        
        # Si el parámetro es una función, la utilizamos para cada objeto del dataset
        # Ls función debe devolver True o False para incluir o no el objeto
        if hasattr(select_expression, '__call__'):
            # pasa una lambda para utilizarla
            nodes_selected = list()
            for node_id, node in self.nodes.items():
            # aplicar búsque
                if select_expression(node):
                    nodes_selected.append(node_id)
            return nodes_selected

        # Si no era el caso anterior, debe ser un diccionario con la
        # expresión
        if isinstance(select_expression, dict) == False:
            raise Exception('Dataset.select()','Query must be a function or formatted dictionary')
        
        
        # La búsqueda puede ser:
        #    - Por id : #
        #    - Por índice : !
        #    - Por expresión a aplicar a cada nodo: $ / campo 
        lvalue = list(select_expression.keys())[0]
        rvalue = list(select_expression.values())[0]
        
        nodes_selected = list()

        # (1) Búsqueda por id
        if lvalue[0] == '#':
            # hay búsqueda por ids. Da lo mismo el resto...
            # devolvemos todos los que
            # TODO: Revisar ésto,... el eval hay que sustituirlo por una selección de
            # tipos para añadir en el caso de que sean listas o tuplas de ids
            if isinstance(rvalue,str):
                nodes_ids = eval(rvalue)
            else:
                nodes_ids = rvalue

            # si es un entero lo convertimos en una lista de enteros
            if isinstance(nodes_ids,int):
                nodes_ids = [nodes_ids]
                
            if (isinstance(nodes_ids,list) or isinstance(nodes_ids,set) or isinstance(nodes_ids,tuple)) == False:   
                raise Exception('Dataset.select()','RVALUE is not in list of ints or int format')
        
            # recorremos la lista de ids pedidos y si están como
            # clave en la lista de nodos existentes, se añade a la
            # lista de ids a devolver
            for node_id in nodes_ids:
                if node_id in self.nodes:
                    nodes_selected.append(node_id)
        
            return nodes_selected
        

        # (2) Búsqueda usando un índice
        if lvalue[0] == '!':
            # la búsqueda es por índices
            # devolvemos todos los que estén en el index
            index_name = lvalue[1:]
            # TODO: Sustituir el eval por una selección según el tipo (lista, tupla, set)
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
                        nodes_selected.append(node_id)
                except KeyError:
                    pass
                except:
                    raise           
            return nodes_selected


        # (3) Es por expresión
        # Se encarga la función select_ids del paquete dstools
        nodes_selected = dstools.select_ids(select_expression, self.nodes)
        # ¿Planes de ejecución ?
        # nodes_selected = dstools.select_ids_planes(select_expression, self.nodes)
                       
        return nodes_selected
        
        

    def delete(self, select_expression):
        '''
        Elimina el elemento del dataset. Retorn la lista de ids borrados
        '''
        nodes_to_delete = self.select_ids(select_expression)
        return self.delete_ids(nodes_to_delete)
        

    def delete_ids(self, nodes_to_delete):
        '''
        Elimina el elemento del dataset. Retorn la lista de ids borrados
        '''
        if len(nodes_to_delete) > 0:
            for ids in nodes_to_delete:
                for inx_name,inx in self.indexes.items():
                    inx.remove_id(ids)
                del(self.nodes[ids])
        return nodes_to_delete
    

    def modify(self, select_expression, update_expression):
        '''
        Realiza modificaciones en lugar de sustituir un nodo por otro
        > ds.modify({'ciudad':'Sevilla'}, {'ciudad':'Almería', 'edad':20})
            carga el valor 'Almería' en el campo ciudad
            carga el valor 20 en el campo 'edad'
        > ds.modify({'#':35}, {'ciudad':'Almería'})
            carga el valor 'Almería' en el campo ciudad
        > ds.modify({'#':10}, {'ciudad':'@segunda_ciudad'})
            carga el valor del campo @segunda_ciudad en el campo ciudad
        '''
        # TODO: Por hacer esta parte
        # class Person(object):
        #     def addattr(self,x,val):
        #        self.__dict__[x]=val
        # Método de añadir de forma dinámica una variable a un objeto
        nodes_to_update = self.select_ids(select_expression)
        if len(nodes_to_update) > 0:
            lvalue = list(update_expression.keys())[0]
            rvalue = list(update_expression.values())[0]

            if lvalue[0] == '$':
                # se trata de una llamada a una función del lenguaje
                for node_id in nodes_to_update:
                    dstools.evalue(update_expression,self.nodes[node_id])
            else:
                # se trata de una modificación o asignación a un atributo existente o nuevo
                for node_id in nodes_to_update:
                    value_to_assign = dstools.evalue(rvalue,self.nodes[node_id])
                    self.nodes[node_id].__dict__[lvalue]=value_to_assign
        return nodes_to_update
    
    
    
    def update(self, select_expression, new_node, force = False, referenced=False):
        '''
        Retorna el id nuevo. Lo que en realidad hace es borrar uno y sustituir uno.
        No es un auténtico UPDATE. Para eso usaremos el método "modify"
        El método "upsert" insertará aunque no haya localizado el nodo a cambiar
        '''
        nodes_to_update = self.select_ids(select_expression)
        if len(nodes_to_update) == 0:
            # no se localizan los nodos a sustituir
            return []
        
        if len(nodes_to_update) == 1:
            self.delete_ids(nodes_to_update)
            new_node_id = self.insert(new_node, force, referenced)
        else:
            raise Exception('Dataset.update()','The select expression selects more than one node')
        return new_node_id
        

    def upsert(self, select_expression, new_node, force = False, referenced=False):
        '''
        Retorna el id nuevo. Lo que en realidad hace es borrar uno y sustituir uno.
        No es un auténtico UPDATE. Para eso usaremos el método "modify"
        El método "upsert" insertará aunque no haya localizado el nodo a cambiar
        '''
        nodes_to_update = self.select_ids(select_expression)
        if len(nodes_to_update) == 1:
            self.delete_ids(nodes_to_update)
        elif len(nodes_to_update) > 1:
            raise Exception('Dataset.update()','The select expression selects more than one node')
        new_node_id = self.insert(new_node, force, referenced)
        return new_node_id
        
        
    def connect(self, select_expression_1, select_expression_2, link_type = nodeslinks.NodesLinks.DIRECTIONAL):
        '''
        Conecta dos nodos del dataset
        '''
        nodes_source = self.select_ids(select_expression_1)
        if len(nodes_source) == 0:
            return []
        
        nodes_target = self.select_ids(select_expression_2)
        if len(nodes_target) == 0:
            return []
        # print(nodes_source)
        # print(nodes_target)
        for source in nodes_source:
            for target in nodes_target:
                link = nodeslinks.NodesLinks(source,target)
                if source not in self.links:
                    self.links[source] = dict()
                self.links[source][target] = link
                if link_type == nodeslinks.NodesLinks.BIDIRECTIONAL:
                    if target not in self.links:
                        self.links[target] = dict()
                    link = nodeslinks.NodesLinks(target,source)
                    self.links[target] = link          
        # print(self.links)
        
        

    def linked_set(self, select_expression = None):
        ''' 
        Retorna [[source, target], [source, target],... , [source, target]]
        '''
        links = list()
        nodes_selected = self.select_ids(select_expression)
        for node in sorted(nodes_selected):
            if node in self.links:
                for target in sorted(self.links[node]):
                    links.append([node,target])
        return links
    

    def linked_nodes(self, select_expression):
        '''
        Retorna { source_nodo_id: [{"node": nodo, "link": link_object}],  },
        '''
        nodes_to_return = dict()
        nodes_selected = self.select_ids(select_expression)
        for node in sorted(nodes_selected):
            if node in self.nodes:
                # print('links de ',node)
                # print(self.links[node])
                nodes_to_return[node] = list()
                for target in sorted(self.links[node]):
                    # print(target)
                    nodes_to_return[node].append(dict({"node":self.nodes[target], "link":self.links[node][target]}))
        # print( nodes_to_return)
        return nodes_to_return
        
        
    
    def is_connected(self, select_expression_1, select_expression_2):
        ids_1 = self.select_ids(select_expression_1)
        ids_2 = self.select_ids(select_expression_2)
        # print(ids_1)
        # print(ids_2)
        for id_1 in ids_1:
            for id_2 in ids_2:
                if id_1 not in self.links:
                    return False
                if id_2 not in self.links[id_1]:
                    return False
        return True
                
        
    def select_dataset(self, criteria, include_network = False):
        
        #
        # ESTO ESTA LISTO.... en su forma básica, pero hay que diseñar una
        # prueba unittest para corroborar su funcionamiento
        #
        
        ds = Dataset()
        nodes_selected = list()

        nodes_selected = self.select_ids(criteria)
            
        # creamos un dataset con los mismos nodos.
        # No se incluyen los índices
        nodes_inserted = dict()
        links_to_make = list()
        
        # print("nodes_selected:",nodes_selected)
        # print("links: ",self.links)
        while len(nodes_selected) > 0:
            node = nodes_selected[0]
            if node not in nodes_inserted:
                new_node = ds.insert(self.nodes[node])
                nodes_inserted[node] = new_node
                # ¿Hay que incluir la red?
                if include_network:
                    # ¿Tiene conexiones?
                    if node in self.links:
                        # Para cada conexión del nodo
                        for link in self.links[node]:
                            # Si el nodo al que conecta no se ha insertado antes
                            if link not in nodes_inserted:
                                # Entonces insertamos en la cola de nodos a procesar
                                nodes_selected.append(link)
                            # Si el enlace no estaba ya
                            if [node,link] not in links_to_make:
                                # insertamos el enlace (con ids antiguos)
                                links_to_make.append([node,link])
                                
            del(nodes_selected[0])
            # print("quedan nodos:",nodes_selected)
            
        # print("links to make:",links_to_make)
        while len(links_to_make) > 0:
            ds.connect({"#":nodes_inserted[links_to_make[0][0]]},{"#":nodes_inserted[links_to_make[0][1]]})
            del(links_to_make[0])
            
        return ds
        


        
        
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
    pass    
        