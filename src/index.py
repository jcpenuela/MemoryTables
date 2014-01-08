'''
Created on 06/01/2014

@author: jcpenuela
'''

class DatasetIndex(object):
    '''
    Índice de dataset
    '''

    def __init__(self, index_name, items, index_expression):
        self.reserved_indexes_names = {'_hash':'hash'}
        self.keys = dict()
        if index_name[0] == '_':
            # nombre reservado, es uno de los índices de sistema
            # Comprobar que es uno de lo índices válidos
            if index_name not in self.reserved_indexes_names:
                raise Exception('DatasetIndex. __init__','Nombre de índice interno no válido')
            self.index_name = index_name
            self.expression_type = 'R'   # Expresión Reservada
            self.index_expression = self.reserved_indexes_names[self.index_name]
        else:
            self.index_name = index_name
            self.index_expression = index_expression
            if self.index_expression[-1] == ')':
                # Puede ser método o función
                if self.index_expression[-2:] == '()':
                    # Es método a aplicar "Objeto.metodo()"
                    self.expression_type = 'M'
                else:
                    # Es método a aplicar "función(?)" sustituyendo la ?
                    # por el objeto
                    self.expression_type = 'F'
            else:
                self.expression_type = 'A'  # Expresión Atributo del objeto
        # indexa los elementos
        (nk, ni) = self.index(items)
        self.nkeys = nk
        self.nitems = ni
    
    
    def __getitem__(self, key):
        '''
        Devuelve la lista de ids por su clave
        '''
        return self.keys[key]

    def __delitem__(self, key):
        '''
        Borra un nodo interno por su clave
        '''
        return self.remove(key)
           
    def __iter__(self):
        '''
        Devuelve un iterador con las claves del índice
        '''
        return iter(self.keys)
    
        
    def index(self, items):
        '''
        Indexa un diccionario de objetos items := {id:objeto,...,id:objeto}
        devuelve tupla (numero_claves, numero_elementos_indexados)
        '''  
        nkeys = 0
        nitems = 0
        for i,o in items.items():
            k = self.get_key(o)
            inserted = self._add_item(k, i)
            nkeys += inserted[0]
            nitems += inserted[1]
        return (nkeys, nitems)



    def _add_item(self, key, item_id):
        '''
        Añade el item_id con la clave key al índice
        '''
        n = 0
        if key not in self.keys:
            self.keys[key] = list()
            n = 1
        self.keys[key].append(item_id)
        return (n,1)
    
    
    def get_key(self, item):
        '''
        Devuelve la clave key de un item (objeto)
        '''
        exp = self.expression_type
        # Reservada
        if exp == 'R':
            # _hash
            if self.index_name == '_hash':
                return hash(item)
            # No contemplado
            else:
                return None
        # Atributo
        elif exp == 'A':
            return getattr(item,self.index_expression)
        # Método
        elif exp == 'M':
            f = getattr(item,self.index_expression[0:-2])
            return f()
        # Función aplicada
        elif exp == 'F':
            expression = self.index_expression
            f = expression[:expression.index('?')] + 'item' + expression[expression.index('?')+1:]
            return eval(f)
        # No contemplado
        else:
            return None
            

    def remove_id(self, item_id):
        '''
        Elimina elementos  con id item_id del índice
        retorna clave o None según lo encuentre o no
        '''
        r = None
        for key, list_id in self.keys.items():
            if item_id in list_id:
                r = key
                break
        if len(self.keys[r])==1:
            del self.keys[r]
        else:
            self.keys[r].remove(item_id)

        return r
    
    def remove_key(self, key):
        '''
        Elimina la clave key del índice
        retorna la lista de ids elminados o None según lo encuentre o no
        '''
        r = None
        if key in self.keys:
            r = self.keys[key]
            del self.keys[key]
        return r

    def remove(self, items_to_remove):
        '''
        Elimina la clave key del índice
        retorna la lista de ids elminados o None según lo encuentre o no
        '''
        keys = set()
        for i,o in items_to_remove.items():
            k = self.get_key(o)
            if k != None:
                keys.add(k)
        nkeys = len(keys)
        nitems = 0
        for k in keys:
            nitems += len(self.remove_key(k))
            
        return (nkeys, nitems)
