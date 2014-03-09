import dstools
# Recoge la consulta, 
def optimizer(query, metadata):
    normalized_query = dstools.normalizar(query)
    print(normalized_query)
    optimized_query = normalized_query
    return optimized_query

    
def elemento(exp):
    
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
        print('DEBUG: optimize. ', query, query.__class__.__name__)
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
    
    
    
    


if __name__ == '__main__':
    print('optimize.py')