import dstools
# Recoge la consulta, 

import src.EXPTree as EXPtree

def optimizer(query, metadata):
    normalized_query = dstools.normalizar(query)
    print(normalized_query)
    arbol = EXPtree.EXPTree()
    query_en_arbol = query_a_arbol(query, arbol)
    return

def dummy():
    pass

def query_a_arbol(query, arbol):

    logical_operators = {
        '$or':dummy, # logical_operator_or,     # { $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
        '$and':dummy, # logical_operator_and,    # { $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
        '$not':dummy, # logical_operator_not,    # { field: { $not: { <operator-expression> } } }
        '$nor':dummy, # logical_operator_nor,    # { $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
        '$xor':dummy, # logical_operator_xor    # { $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
        }
    
    comparison_operators = {
        '$eq':dummy, # comparison_operator_eq,     # { field: {$eq: value} }
        '$ne':dummy, # comparison_operator_ne,     # { field: {$ne: value} }
        '$gt':dummy, # comparison_operator_gt,     # { field: {$gt: value} }
        '$gte':dummy, # comparison_operator_gte,   # { field: {$gte: value} }
        '$lt':dummy, # comparison_operator_lt,     # { field: {$lt: value} }
        '$lte':dummy, # comparison_operator_lte,   # { field: {$lte: value} }
        '$in':dummy, # comparison_operator_in,     # { field: {$in: [<value1>, <value2>, ... <valueN> ]} }
        '$nin':dummy, # comparison_operator_nin    # { field: {$nin: [ <value1>, <value2> ... <valueN> ]} }
        }

    functions = {
        '$round':dummy, # function_dummy,
        '$fix':dummy, # function_dummy,
        '$max':dummy, # function_dummy, # {$max : [val1, val2,... valn]},
        '$minAcum':dummy, # function_dummy
        }
    constant_operators = {
        '$true':dummy, # function_true,
        '$false':dummy, # function_false,
        '$db':dummy, # function_db
        }
    
    
    print_debug = False
    if print_debug:
        print('DEBUG: optimize. ', query, query.__class__.__name__)
    if query.__class__.__name__ == 'dict':
        lval = list(query.items())[0][0]
        rval = list(query.items())[0][1]
        # print('lval:',lval,'rval:',rval)
        nodo = EXPtree.EXPNode(lval)
        arbol.add_node_at_left(nodo)
        for h in rval:
            nodo = EXPtree.EXPNode(h)
            arbol.add_node_at_left(query_a_arbol(h,arbol))
        return #return logical_operators[lval](rval, ds_element)
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
    
    
    
    


if __name__ == '__main__':
    print('optimize.py')