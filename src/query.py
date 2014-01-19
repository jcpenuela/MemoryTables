'''
Created on 19/01/2014

@author: jcpenuela
'''
import dstools

class Query(object):
    '''
    Objeto query que ayuda a conformar una consulta
    y que se podrá pasar como parámetro a la select o
    el update o delete, o cualquier método que precise
    de una selección en un dataset
    '''


    def __init__(self, condition = None):
        '''
        Constructor
        '''
        if condition != None:
            if not isinstance(condition, dict):
                raise Exception('Query.__init__()','Condition must be a dictionary')
            self.expression = dstools.normalizar(condition)
        else:
            self.expression = dict()

       
    def add_and(self, condition):
        '''
        Añade una pareja al árbol
        '''
        # Comprobamos la condición
        if not isinstance(condition, dict):
            raise Exception('Query.add_and()','Condition must be a dictionary') 
        if len(self.expression) == 0:
            self.expression = dstools.normalizar(condition)
        else:
            self.expression = dict({'$and' :[self.expression, dstools.normalizar(condition)]})
        return self.expression
 
    def add_or(self, condition):
        '''
        Añade una pareja al árbol
        '''
        # Comprobamos la condición
        if not isinstance(condition, dict):
            raise Exception('Query.add_or()','Condition must be a dictionary')
        if len(self.expression) == 0:
            self.expression = dstools.normalizar(condition)
        else:
            self.expression = dict({'$or' :[self.expression, dstools.normalizar(condition)]})
        return self.expression
    
    def add_not(self):
        '''
        Añade una pareja al árbol
        '''
        self.expression = dict({'$not' :self.expression})
        return self.expression
    
    def get_query(self):
        return self.expression
        
        
          

if __name__ == '__main__':
    q = Query()
    q.add_and({'ciudad':'Sevilla'})
    q.add_and({'edad':30, 'peso':{'$gt':50}})
    q.add_or({'ciudad':'Huelva'})
    print(q.expression)
    
    