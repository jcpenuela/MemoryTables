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


class Dataset(object):
    
    def __init__(self):
        self.elements = dict()     # nodos en memoria 
        self.next_element_id = 1       # siguiente id libre
        self.index_list = dict() # lista vacía de índices creados para
        '''
             { index_name : 
                           { 
                                'exp' : expresion,
                                'original_exp': expresion original,
                                'keys' :
                                    {
                                        clave1 : [],
                                        clave2 : [],
                                        ...
                                        claven : []
                                    } 
                            } 
        '''
        self._internal_indexes()

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
        return iter(self.elements)



    def _internal_indexes(self):
        '''
        
        Crea los dos índices internos _insert y _content
        
        '''
        self._index_by('_insert', '_insert')
        self._index_by('_content', '_content')
        self._index_by('_hash', '_hash')

    def _get_next_element_id(self):
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
        self.index_list = dict()
        self._internal_indexes()




    def add_element(self, new_element, referenced=False):
        '''
        OK
        Añade un elemento a la tabla. Devuelve el id de la tabla.
        referenced = True implica que no se almacena una copia del elemento,
        sino una referencia al elemento pasado (en el caso de que
        sea un elemento referenciado, objeto, lista, etc...)
        
        Verifica si el elemento existe ya, si es así no inserta, sino que
        localiza el id y lo devuelve
        '''
        
        h = hash(new_element)
        if h in self.index_list['_hash']['keys']:
            return 0
        
        new_id = self._get_next_element_id()
        if not referenced:
            n = copy.deepcopy(new_element)
            self.elements[new_id] = n
        else:
            self.elements[new_id] = new_element
    
        # indexar elemento
        self.index_element(new_id)
        
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
        
        return id
    
    


    def count(self):
        '''
        OK
        '''
        return len(self.elements)


    
    
    def select_element_ids_order_by_ix(self, index_name, limit=0):
        '''
        devuelve todos los elementos de la tabla ordenados por un índice
        el campo limit indica si quiere una cantidad concreta de elementos o la lista
        completa de elementos
        '''
        elements = []
        n = 0
        if index_name not in self.index_list:
            raise Exception('Dataset.get_element_by','Index [' + index_name + '] not exists.' )
        
        for element_ids_list in sorted(self.index_list[index_name]['keys']):
            n+=1
            if limit==0 or (limit>0 and n <= limit):  
                elements = elements + element_ids_list
            else:
                break
        
        return elements


    def select_elements_order_by_ix(self, index_name, limit=0, referenced=False):
        '''
        devuelve todos los elementos de la tabla ordenados por un índice
        el campo limit indica si quiere una cantidad concreta de elementos o la lista
        completa de elementos
        '''
        elements = []
        n = 0
        if index_name not in self.index_list:
            raise Exception('Dataset.get_element_by','Index [' + index_name + '] not exists.' )
        
        print((self.index_list[index_name]['keys']))
        for element_ids_list in sorted((self.index_list[index_name]['keys']).keys()):
            if limit==0 or (limit>0 and n <= limit):
                for element_id in self.index_list[index_name]['keys'][element_ids_list]:
                    n+=1
                    if limit==0 or (limit>0 and n <= limit):
                        if referenced:
                            elements.append(self.elements[element_id])
                        else:
                            e = copy.deepcopy(self.elements[element_id])
                            elements.append(e)
                    else:
                        break
            else:
                break

        return elements



    def select_element_ids_where_ix_value(self, index_name, value, limit=0):
        '''
        Recupera una copia de la lista de ids de nodos cuyo value coincide con el pasado
        None en caso contrario
        '''
        n = 0
        
        if index_name not in self.index_list:
            raise Exception('Dataset.select_element_ids_where_value','Index [' + index_name + '] not exists.' )
        
        if value not in self.index_list[index_name]['keys']:
            return None
        if limit == 0:
            return list(self.index_list[index_name]['keys'][value])
        else:
            element_ids_list = []
            while n < limit:
                element_ids_list.append(self.index_list[index_name]['keys'][value][n-1])
                n+=1
            return element_ids_list
                
        
    
    def select_elements_where_ix_value(self, index_name, value, limit=0, referenced=False):
        '''
        Recupera una copia de la lista de nodos cuya clave coincide con el pasado
        None en caso contrario
        '''
        if index_name not in self.index_list:
            raise Exception('Dataset.select_elements_where_value','Index [' + index_name + '] not exists.' )
        
        if value not in self.index_list[index_name]['keys']:
            return None
        
        elements_list = list()
        n = 0
        for element_id in self.index_list[index_name]['keys'][value]:
            n+=1
            if limit==0 or (n <= limit):
                if referenced:
                    elements_list.append(self.elements[element_id])
                else:
                    e = copy.deepcopy(self.elements[element_id])
                    elements_list.append(e)
            else:
                break
        
        return elements_list
    
    
    
    def index_by(self, index_name, expresion):
        if index_name[0] == '_':
            raise Exception('Dataset._index_by','Index name [' + index_name + '] can not start with underscore (reserved).')
        return self._index_by(index_name, expresion)
    
         
    def _index_by(self, index_name, expresion):
        '''
        Crea un índice. La clave del índice se genera con la "expresion"
        
        La función no puede esperar argumentos, ya que no se le van a pasar argumentos
        a la hora de evaluarlo con "eval"
        
        "funcion(elemento)" -> En caso de ser elemento básico y no un objeto
        "funcion(.campo1)" -> evalua como función
        "funcion(.metodo1())" -> evalua como función 
        ".metodo1()" ->
        ".campo3" ->
        "#expresion" -> (passthrough)
        "lambda ..." ->
        "_interno" -> Acciones internas reservadas, por ejemplo "_natural"
        
        Devuelve una tupla con dos elementos (número de claves y número de elementos)
        '''
        if index_name in self.index_list:
            raise Exception('Dataset.index_by','Index [' + index_name + '] already exists.')
        
        
        # t = type(function_name)
        
        indexed_elements = 0
        indexed_keys = 0
        # se llama a una expresión que está en el objeto
        # ".metodo1()" ->
        # ".campo3" ->
        # prepara el código a evaluar
        
        if expresion[0] == '#':
            # passthrough 
            code = expresion[1:]
            
        elif expresion[0] == '_':
            # expresión interna a la clase Dataset
            if expresion == '_insert':
                # orden de entrada
                code = 'element_id'
            elif expresion == '_content':
                # hash del contenido del elemento
                code = 'hash(str(self.elements[element_id]))'
            else:
                # caso no reconocido
                code = ''
                
        elif expresion[0:6] == 'lambda ':
            # lambda
            code = expresion
            
        elif expresion[0] == '.':
            # expresión interna al objeto
            code = 'str(self.elements[element_id]' + expresion + ')'
             
        else:
            # se llama a una expresión externa
            # "funcion()" -> En caso de ser elemento básico y no un objeto,lleva al objeto como argumento
            # "funcion(.campo1)" -> evalua como función
            # "funcion(.metodo1())" -> evalua como función
            fn = expresion[0:expresion.find('(')+1] # funcion
            if expresion[expresion.find('(')+1] == ')': 
                # lleva al propio objeto como argumento
                code = fn + 'self.elements[element_id])'
            else:
                vr = expresion[expresion.find('(')+2:-1]
                code = fn + 'self.elements[element_id].' + vr + ')'

        # crea la entrada del índice en el conjunto  de índices y almacenamos las expresión
        self.index_list[index_name] = dict()
        self.index_list[index_name]['exp'] = code
        self.index_list[index_name]['original_exp'] = expresion
        self.index_list[index_name]['keys'] = dict()

        # ejecuta el código obtenido de la expresión para los elementos existentes        
        for element_id in self.elements:
            # ejecuta el código para obtener la clave de índice
            try:
                # value = self.elements[element_id].function_name()
                value = eval(code)
                # value = function_name()
                # DEBUG
                # print(self.elements[element_id].content)
            except NameError:
                raise Exception('Dataset.index_by','Index [' + index_name + ']. Index expression [' + expresion + '] fails.' )
            
            # el valor retornado por la ejecución del código de generación de clave
            # se inserta
            if value in self.index_list[index_name]['keys']:
                self.index_list[index_name]['keys'][value].append(element_id)
            else:
                self.index_list[index_name]['keys'][value] = [element_id]
                indexed_keys += 1
                
            indexed_elements += 1
        
        
        return (indexed_keys, indexed_elements)


    def index_element(self, element_id):
        '''
        agrega a todos los índices (indexa) el elemento con indice "element_id" de "self.elements"
        '''
        
        indexes_processed = 0
        
        for index_name in self.index_list:
            
            code = self.index_list[index_name]['exp']
        
            try:
                #DEBUG
                # print(code)
                value = eval(code)
                #DEBUG
                # print(value)
            except NameError:
                raise Exception('Dataset.index_element','Index [' + index_name + ']. Index code [' + code + '] fails.' )
            
            # el valor retornado por la ejecución del código de generación de clave
            # se inserta
            if value in self.index_list[index_name]['keys']:
                self.index_list[index_name]['keys'][value].append(element_id)
            else:
                self.index_list[index_name]['keys'][value] = [element_id]
            
            indexes_processed += 1
            
        return indexes_processed 
    
    
    def unindex_element(self, element_id):
        '''
        elimina las entradas del índice correspondientes al elemento
        '''
        indexes_processed = 0
        
        for index_name in self.index_list:
            
            code = self.index_list[index_name]['exp']
        
            try:
                value = eval(code)
                # DEBUG
                # print(value)
            except NameError:
                raise Exception('Dataset.unindex_element','Index [' + index_name + ']. Index code [' + code + '] fails.' )
            
            # el valor retornado por la ejecución del código de generación de clave
            # se borra de la lista de elementos de esa clave
            if value in self.index_list[index_name]['keys']:
                self.index_list[index_name]['keys'][value].remove(element_id)
            
            indexes_processed += 1
            
        return indexes_processed
            
            
    
    def reindex_element(self, element_id):
        '''
        actualiza todos los índices del elemento con indice "element_id" de "self.elements"
        Este procedimiento implica una búsqueda en profundidad del elemento en los índices
        para eliminarlo
        '''
        
        # borramos todas las entradas de element_id en los índices existentes
        for index_name in self.index_list:
            for key_value in self.index_list[index_name]['keys']:
                while element_id in self.index_list[index_name]['keys'][key_value]:
                    self.index_list[index_name]['keys'][key_value].remove(element_id)
        
        # indexamos de nuevo el elemento en base a su expresión
        return self.index_element(element_id)
        


    
    def remove_index(self, index_name):
        if index_name not in self.index_list:
            raise Exception('Dataset.remove_index','Index [' + index_name + '] not exists.' )
        del(self.index_list[index_name])
        return
    
    def _remove_index(self, index_name):
        if index_name[0] == '_':
            raise Exception('Dataset.remove_index','Index name [' + index_name + '] can not start with underscore (reserved).')
        self.remove_index(index_name)
        return
    
    
    def reindex_by(self, index_name):
        '''
        reconstruye el índice index_name en caso de corrupción
        '''
        if index_name[0] == '_':
            raise Exception('Dataset.reindex_by','Index name [' + index_name + '] can not start with underscore (reserved).')
        return self._reindex_by(index_name)
    
    
    def _reindex_by(self, index_name):
        '''
        reconstruye el índice index_name en caso de corrupción
        '''
        if index_name not in self.index_list:
            raise Exception('Dataset.reindex_by','Index [' + index_name + '] not exists.' ) 
        
        # cogemos la expresión
        code = self.index_list[index_name]['exp']
        # borramos la entrada del índice
        self.remove_index(index_name)
        # indexamos con un passthrough de la expresión
        self._index_by(index_name, '#'+code)
        
        return
        
        
            
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
    t.add_element(f)
    f = fact.Fact("dos")
    t.add_element(f)
    f = fact.Fact("tres")
    t.add_element(f)

    t.index_by('hecho', '.content()')

    print(t.select_elements_order_by_ix('_insert', referenced=True))
    print(t.select_elements_order_by_ix('_content', referenced=True))
    print(t.select_elements_order_by_ix('hecho', referenced=True))

    t.dump_data()
        