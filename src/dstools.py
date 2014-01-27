def normalizar(nodo, nivel=1):
    '''
    Convierte la consulta en un árbol
    '''
    logical_operators = {
                '$or':'list',     # { $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
                '$and':'list',    # { $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
                '$not':'list',    # { field: { $not: { <operator-expression> } } }
                '$nor':'list',    # { $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
                '$xor':'list'    # { $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
                }
    
    function_operators = {
                '$round':'one',
                '$fix':'one',
                '$max':'list', # {$max : [val1, val2,... valn]},
                '$minAcum':'list'
                }
    
    comparison_operators = {
                '$eq':'list',
                '$ne':'list',
                '$gt':'list',
                '$gte':'list',
                '$lt':'list', # { $lte : [@campo, {$max : [val1, val2,... valn]}] }
                '$lte':'list', # { $lte : [@campo, val] }
                '$in':'list', # { $in : [@campo, val1, val2,... valn] }
                '$nin':'list'
                }
    constant_operators = {
                '$true':'',
                '$false':'',
                '$db':''
                }

    
    print_debug = False
    # numeric types: int, float, complex
    # text: str
    # sequence types: list, tuple, set, dict

    if nodo.__class__.__name__ in ('int','float','complex','str','bool'):
        # es un tipo considerado primitivo
        return nodo
    
    # es un tipo de lista, tupla, set o dict
    if len(nodo)>1:
        if nivel == 1:
            nq = dict()
            nq['$and'] = list()
            if nodo.__class__.__name__ == 'dict':        
                for lvalue,rvalue in nodo.items():
                    nq['$and'].append(normalizar({lvalue:rvalue}, nivel+1))
            else:
                for v in nodo:
                    nq['$and'].append(normalizar(v,nivel+1))
            return nq
        else:
            nq = list()
            if nodo.__class__.__name__ == 'dict':        
                for lvalue,rvalue in nodo.items():
                    nq.append(normalizar({lvalue:rvalue}, nivel+1))
            else:
                for v in nodo:
                    nq.append(normalizar(v,nivel+1))
            return nq
    else:
        # Se va a normalizar cada elemento, por lo que puede llegar aquí tras una
        # llamada: return { normalizar(lvalue):normalizar(rvalue) }
        if nodo.__class__.__name__ in ('list','set','tuple'):
            # es un tipo complejo no primitivo
            return normalizar(nodo[0], nivel)
                
        # tomamos el nodo y su parámetro (valor)
        # {'@edad':20}   ==>>   {'$eq':['@edad',20]}
        lvalue = list(nodo.items())[0][0]
        rvalue = list(nodo.items())[0][1]
        # ¿De qué tipo es el LVALUE? (k)
        if lvalue in list(logical_operators.keys()) + list(function_operators.keys()) + list(comparison_operators.keys()):
            if rvalue.__class__.__name__ not in ('list','set','tuple'):
                # print('DEBUG: nodo = ', nodo)
                raise Exception('Logical operator / function / comparison operator requieres a list argument',
                                'Given a type ' + rvalue.__class__.__name__)
            else:
                nl = list()
                for e in rvalue:
                    nl.append(normalizar(e,nivel+1))
                return {lvalue:nl}
        
        if lvalue in list(constant_operators.keys()):
            return {lvalue:rvalue}
            
        # es un operador de expresión a evaluar
        # tratamos los valores a asignar
        if rvalue.__class__.__name__ in ('list', 'set', 'tuple'):
            # normalizar lista $in
            nv = [ normalizar(lvalue, nivel+1) ]
            for i in rvalue:
                nv.append( normalizar(i, nivel+1) )
            return { '$in':nv }            
        else:
            # Es un par clave valor, con lo que ponemos nosotros el
            # operador $eq
            return { '$eq':[normalizar(lvalue,nivel+1), normalizar(rvalue,nivel+1)] }
            

                    
                    

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


def select_ids(query, datos):
    # IMPORTANTE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    # class Person(object):
    #     def addattr(self,x,val):
    #        self.__dict__[x]=val
    # Método de añadir de forma dinámica una variable a un objeto
    
    '''
    '''
    query = normalizar(query)
    
    nodes_selected = list()
    for ds_id, ds_element in datos.items():
        if evalue(query, ds_element):
            nodes_selected.append(ds_id)
        
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
    # print('DEBUG: logical_operator_not. ', rval, ds_element)
    # print('DEBUG: logical_operator_not. ', evalue(rval, ds_element))
    if evalue(rval[0],ds_element):
        return False
    return True

def logical_operator_nor(rval, ds_element):
    # NOT OR
    return logical_operator_not([logical_operator_or(rval,ds_element)],ds_element)

def logical_operator_xor(rval, ds_element):
    n = 0
    for i in rval:
        if evalue(i,ds_element):
            n += 1
            if n>1:
                return False
    return (n == 1)
    

# Comparaciones

def comparison_operator_eq(operands, ds_element):
    exp1 = evalue(operands[0], ds_element)
    exp2 = evalue(operands[1], ds_element)    
    return exp1 ==  exp2

def comparison_operator_ne(operands, ds_element):
    exp1 = evalue(operands[0], ds_element)
    exp2 = evalue(operands[1], ds_element)  
    return exp1 != exp2

def comparison_operator_gt(operands, ds_element):
    exp1 = evalue(operands[0], ds_element)
    exp2 = evalue(operands[1], ds_element)  
    return exp1 > exp2

def comparison_operator_gte(operands, ds_element):
    exp1 = evalue(operands[0], ds_element)
    exp2 = evalue(operands[1], ds_element)  
    return exp1 >= exp2

def comparison_operator_lt(operands, ds_element):
    exp1 = evalue(operands[0], ds_element)
    exp2 = evalue(operands[1], ds_element)  
    return exp1 < exp2

def comparison_operator_lte(operands, ds_element):
    exp1 = evalue(operands[0], ds_element)
    exp2 = evalue(operands[1], ds_element)  
    return exp1 <= exp2

def comparison_operator_in(operands, ds_element):
    exp1 = evalue(operands[0], ds_element)  
    for i in operands[1:]:
        exp2 = evalue(i, ds_element)
        if exp1 == exp2:
            return True
    return False

def comparison_operator_nin(operands, ds_element):
    exp1 = evalue(operands[0], ds_element)
    for i in operands[1:]:
        exp2 = evalue(i, ds_element)
        if exp1 == exp2:
            return False
    return True

# funciones
def function_dummy(options, ds_element):
    return True


# funciones sin parámetros (solo hacen uso del ds_element)
def function_true(ds_element):
    return True

def function_false(ds_element):
    return False

def function_db(ds_element):
    return 'Lo que sea'

# evaluador
def evalue(query, ds_element):

    logical_operators = {
        '$or':logical_operator_or,     # { $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
        '$and':logical_operator_and,    # { $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
        '$not':logical_operator_not,    # { field: { $not: { <operator-expression> } } }
        '$nor':logical_operator_nor,    # { $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
        '$xor':logical_operator_xor    # { $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
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

    functions = {
        '$round':function_dummy,
        '$fix':function_dummy,
        '$max':function_dummy, # {$max : [val1, val2,... valn]},
        '$minAcum':function_dummy
        }
    constant_operators = {
        '$true':function_true,
        '$false':function_false,
        '$db':function_db
        }
    
    
    print_debug = False
    if print_debug:
        print('DEBUG: evalue. ', query, query.__class__.__name__)
    if query.__class__.__name__ == 'dict':
        lval = list(query.items())[0][0]
        rval = list(query.items())[0][1]
        # print('lval:',lval,'rval:',rval)
        if lval in logical_operators: # ('$or','$and','$not'): 
            # es operador lógico
            return logical_operators[lval](rval, ds_element)
        elif lval in comparison_operators: # ('$or','$and','$not'): 
            # es operador lógico
            return comparison_operators[lval](rval, ds_element)
        elif lval in functions:
            return comparison_operators[lval](rval, ds_element)
        # TODO: Esto hay que revisarlo... estoy dando por bueno que llegue como
        # función o como constante más abajo
        elif lval in constant_operators:
            return constant_operators[lval](ds_element)
        else:
            raise Exception('select.evalue()','operador no contemplado:' + list(rval.items())[0][0])
    # es una lista o un elemento primitivo
    elif query.__class__.__name__ in ('int','float','complex','bool'):
        return query
    
    elif query.__class__.__name__ in ('str'):
        if query[0] == '@' and query[1] != '@': # Doble @ => @ 
            # devolver el valor del campo
            # getattr(x,'campo') == x.campo
            # print('return ',getattr(ds_element,query[1:]))
            return getattr(ds_element,query[1:])
        # si se trata de una constante de operador (función sin parámetros)
        # llamamos a la función
        if query[0] == '$' and query in constant_operators:
            return constant_operators[query](ds_element)
        # si no, devolver la cadena o el elemento que sea 
        return query
    
    # este últimop bloque no debería ejecutarse...
    # en principio, todas las funciones deben llevar una lista como argumento,
    # por lo que el sistema ha debido detectar una lista de argumentos antes de llegar
    # a este punto...... TODO: REVISAR ESTE DETALLE Y VER SI CONVIENE EVALUAR LISTAS SUELTAS
    elif query.__class__.__name__ in ('list','tuple','set'):
        nq = list()
        for i in query:
            nq.append(evalue(i,ds_element))
        return nq
