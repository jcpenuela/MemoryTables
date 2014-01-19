def normalizar(nodo, nivel=1):
    '''
    Convierte la consulta en un árbol
    '''
    logical_operators = {
                '$or':'list',     # { $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
                '$and':'list',    # { $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
                '$not':'one',    # { field: { $not: { <operator-expression> } } }
                '$nor':'list'    # { $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
                }
    
    if len(nodo)>1:
        # Hay un AND de algún tipo no reflejado con operador lógico
        # {'ciudad':['Sevilla','Huelva'], 'edad':30} o
        # [{'ciudad':['Sevilla','Huelva'], 'edad':30}] =>
        # {'$and':[{'ciudad':['Sevilla','Huelva']}, {'edad':30}]}
        nq = dict()
        nq['$and'] = list()
        if isinstance(nodo, list) or isinstance(nodo, set) or isinstance(nodo, tuple):
            for v in nodo:
                nq['$and'].append(normalizar(v,nivel+1))
        elif isinstance(nodo, dict):
            for k,v in nodo.items():
                nq['$and'].append(normalizar({k: v},nivel+1))
        return nq
    
    else:
        # tomamos el nodo y su parámetro (valor)
        k = list(nodo.items())[0][0]
        v = list(nodo.items())[0][1]
        # ¿es operador lógico?
        if k not in logical_operators: #('$and','$or','$not'):
            # es un operador de expresión de comparación
            # tratamos los valores a asignar
            if isinstance(v,list):
                # normalizar lista $in
                nv = dict()
                nv['$in'] = list()
                for i in v:
                    nv['$in'].append(i)
                return { k: nv }
            elif isinstance(v,dict):
                # se supone que es un par clave:valor
                return { k: v}
            else:
                # DEBUG:
                return { k: {'$eq':v} }
        else:
            # es operador lógico
            # Si la lista que acompaña al operador solo tiene un elemento
            # contamos, de momento, con que los operadores son de lista de elementos
            # teniendo en cuenta que tenemos que introducir operadores unarios {'$not':{'ciudad':'sevilla'}}
            if logical_operators[k] == 'one':
                # es operador lógico unario
                return { k: normalizar(v, nivel+1)}
            else: # es un operador cuyo operando es una lista de elementos ($and o un $or)
                # es operador lógico binario
                if isinstance(v,list) or isinstance(v,tuple) or isinstance(v,set) or isinstance(v,dict):            
                    if len(v) == 1: # si solo tiene un elemento en esa lista, quitamos el operador
                        # Por ejemplo: {'$or':[{'ciudad':'Sevilla'}]}
                        # Pasa a convertirse en {'ciudad':'Sevilla'}
                        if isinstance(v,list) or isinstance(v,tuple) or isinstance(v,set):
                            return normalizar(v[0], nivel+1)
                        else:
                            # en caso de tupla se recoje como un elemento suelto... no se por qué!
                            return normalizar(v, nivel+1)
                    else:
                        # el operador trae una lista como parámetros de entrada
                        nv = dict()
                        nv[k] = list() # Elemento con el operador como clave
                        # pasamos a formar la lista con cada elemento 
                        # normalizado
                        for i in v:
                            nv[k].append(normalizar(i, nivel+1))
                        return nv
                else:
                    # un operador de lista debe llevar una lista
                    raise Exception('¿¿Pero esto que es...??','{<OperadorLógico>:<lista>|<dict>|<set>|<tupla>}')



def select(query, datos):
    # IMPORTANTE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    # class Person(object):
    #     def addattr(self,x,val):
    #        self.__dict__[x]=val
    # Método de añadir de forma dinámica una variable a un objeto
    
    '''
    '''
    query = normalizar(query)
    
    nodes_selected = dict()
    for ds_id, ds_element in datos.items():
        if evalue(query, ds_element):
            nodes_selected[ds_id] = ds_element
        
    return nodes_selected


def logical_operator_or(rval, ds_element):
    for i in rval:
        if evalue(i,ds_element):
            return True
    return False

def logical_operator_and(rval, ds_element):
    for i in rval:
        if not evalue(i,ds_element):
            return False
    return True


def logical_operator_not(rval, ds_element):
    if evalue(rval,ds_element):
        return False
    return True

def logical_operator_nor(rval, ds_element):
    if evalue(rval,ds_element):
        return False
    return True

def comparison_operator_eq(exp1, exp2):
    return exp1 == exp2

def comparison_operator_ne(exp1, exp2):
    return exp1 != exp2

def comparison_operator_gt(exp1, exp2):
    return exp1 > exp2

def comparison_operator_gte(exp1, exp2):
    return exp1 >= exp2

def comparison_operator_lt(exp1, exp2):
    return exp1 < exp2

def comparison_operator_lte(exp1, exp2):
    return exp1 <= exp2

def comparison_operator_in(exp1, exp2):
    for i in exp2:
        if exp1 == i:
            return True
    return False

def comparison_operator_nin(exp1, exp2):
    for i in exp2:
        if exp1 == i:
            return False
    return True

def evalue(query, ds_element):

    logical_operators = {
        '$or':logical_operator_or,     # { $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
        '$and':logical_operator_and,    # { $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
        '$not':logical_operator_not,    # { field: { $not: { <operator-expression> } } }
        '$nor':logical_operator_nor    # { $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
        }
    
    comparison_operators = {
        '$eq':comparison_operator_eq,     # { field: {$eq: value} }
        '$ne':comparison_operator_ne,     # { field: {$ne: value} }
        '$gt':comparison_operator_gt,     # { field: {$gt: value} }
        '$gte':comparison_operator_gte,   # { field: {$gte: value} }
        '$lt':comparison_operator_lt,     # { field: {$lt: value} }
        '$lte':comparison_operator_lte,   # { field: {$lte: value} }
        '$in':comparison_operator_in,     # { field: {$in: [<value1>, <value2>, ... <valueN> ]} }
        '$nin':comparison_operator_nin    # { field: {$nin: [ <value1>, <value2> ... <valueN> ]} }
        }
    
    for lval,rval in query.items():
        # print('lval:',lval,'rval:',rval)
        if lval in logical_operators: # ('$or','$and','$not'): 
            # es operador lógico
            return logical_operators[lval](rval, ds_element)
        elif list(rval.items())[0][0] in comparison_operators:
            # es campo:expresion
            # según el tipo de los datos sean diccionario u objeto tomamos el
            # valor de la expresión (la procedente del objeto)
            # de una forma u otra
            if isinstance(ds_element,dict):
                # es diccionario
                exp1 = ds_element[lval]
            else:
                # Método usando EVAL
                # exp1 = eval('ds_element.'+lval)
                # Método usando __dict__     
                # exp1 = ds_element.__dict__[lval]
                exp1 = ds_element.__dict__[lval]
            op = list(rval.items())[0][0]
            exp2 = list(rval.items())[0][1]
            # evaluamos la expresión
            return comparison_operators[op](exp1,exp2)
        else:
            raise Exception('select.evalue()','operador no contemplado:' + list(rval.items())[0][0])

