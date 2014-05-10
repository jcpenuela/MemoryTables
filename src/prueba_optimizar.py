__author__ = 'Juan Carlos'
import src.dstools as dstools
import src.persona as persona
import src.dataset as dataset
import src.query as query
def normalizar2(nodo, nivel=1):
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
    if nodo is None:
        return nodo

    if nodo.__class__.__name__ in ('int','float','complex','str','bool'):
        # es un tipo considerado primitivo
        return nodo

    # es un tipo de lista, tupla, set o dict
    if len(nodo) == 0:
        return nodo

    if len(nodo)>1:
        if nivel == 1:
            nq = dict()
            nq['$and'] = list()
            if nodo.__class__.__name__ == 'dict':
                for lvalue,rvalue in nodo.items():
                    nq['$and'].append(normalizar2({lvalue:rvalue}, nivel+1))
            else:
                for v in nodo:
                    nq['$and'].append(normalizar2(v,nivel+1))
            return nq
        else:
            nq = list()
            if nodo.__class__.__name__ == 'dict':
                for lvalue,rvalue in nodo.items():
                    nq.append(normalizar2({lvalue:rvalue}, nivel+1))
            else:
                for v in nodo:
                    nq.append(normalizar2(v,nivel+1))
            return nq
    else:
        # Se va a normalizar cada elemento, por lo que puede llegar aquí tras una
        # llamada: return { normalizar(lvalue):normalizar(rvalue) }
        if nodo.__class__.__name__ in ('list','set','tuple'):
            # es un tipo complejo no primitivo
            return normalizar2(nodo[0], nivel)

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
                    nl.append(normalizar2(e,nivel+1))
                return {lvalue:nl}

        if lvalue in list(constant_operators.keys()):
            return {lvalue:rvalue}

        # es un operador de expresión a evaluar
        # tratamos los valores a asignar
        if rvalue.__class__.__name__ in ('list', 'set', 'tuple'):
            # normalizar lista $in
            nv = [ normalizar2(lvalue, nivel+1) ]
            for i in rvalue:
                nv.append( normalizar2(i, nivel+1) )
            return { '$in':nv }
        else:
            # Es un par clave valor, con lo que ponemos nosotros el
            # operador $eq
            return { '$eq':[normalizar2(lvalue,nivel+1), normalizar2(rvalue,nivel+1)] }


def optimized_select_ids(query, ds):
    query = normalizar2(query)  # Convertimos la consulta en un árbol
    nodes_selected = list()

    print('Original:',query)
    # localizamos los nodos finales de la query
    final_query_nodes = list()

    # recorremos la consulta desde el nodo inicial
    print(hojas(query))

    return nodes_selected

def hojas(q, nivel=1):
    lista_operadores_validos = ['$eq','$in']
    lista_valores = set()
    if q.__class__.__name__ == 'list':
        for elemento in q:
            print('>'*nivel,elemento)
            nn = hojas(elemento,nivel+1)
            if nn is not None:
                if nn.__class__.__name__ != 'set':
                    lista_valores.add(nn)
                else:
                    for i in nn:
                        lista_valores.add(i)
        if len(lista_valores)>0:
            return lista_valores
        else:
            return None

    elif q.__class__.__name__ == 'dict':
        operador = list(q.keys())[0]
        valores = list(q.values())[0]
        if operador in lista_operadores_validos:
            return valores[0]
        return hojas(valores,nivel+1)

    else:
        return None

    # recorremos el dataset pasado en datos
    # para cada elemento del dataset aplicamos la expresión
    # for ds_id, ds_element in datos.items():
    #     # vemos si casa la query con el elemento concreto
    #     if dstools.evalue(query, ds_element):
    #         # si la consulta casa con el elemento, lo añadimos
    #         nodes_selected.append(ds_id)



def carga_datos2():
    d = dataset.Dataset()
    datos = [
        ['S18', 'Sevilla', 18, 45.6],
        ['S30', 'Sevilla', 30, 60.2],
        ['H19', 'Huelva', 19, 75.3],
        ['H25', 'Huelva', 25, 82.6],
        ['C40', 'Córdoba', 40, 59.2],
        ['C35', 'Córdoba', 35, 63.1],
        ['Z42', 'Cádiz', 42, 75.5],
        ['Z29', 'Cádiz', 29, 85.8]
    ]
    for i in datos:
        p = persona.Persona(i[0], i[1], i[2], i[3])
        d.insert(p)
    return d

if __name__ == '__main__':
    ds = carga_datos2()
    q = {'$or':[{'@edad':35},{'@ciudad':['Sevilla','Cádiz'],'@nombre':'S30'},{'@nombre':'Z29'},{'$gt':['@peso',70]}]}
    l = optimized_select_ids(q,ds)
    # print(l)
