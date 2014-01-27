'''
Created on 08/08/2013

@author: jcpenuela
'''
import unittest
import dstools

class Datos():
    def __init__(self):
        pass

class Dstools(unittest.TestCase):


    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    
    def testEvaluar(self):
        data = Datos()
        data.ciudad = 'Sevilla'
        data.destino = 'Córdoba'
        data.preferido = 'Sevilla'
        data.edad = 20
        data.peso = 65.3
        
        pruebas = [ 
                    # 1
                    [   {'@edad':20}, True  ],
                    [   {'@edad':21}, False  ],
                    [   {'@ciudad':'Sevilla'}, True  ],
                    [   {'@ciudad':'Córdoba'}, False  ],
                    # $and reducido
                    [   {'@ciudad':'Sevilla', '@edad':20}, True  ],
                    [   {'@edad':20, '@ciudad':'Sevilla'}, True  ],
                    [   {'@edad':20, '@ciudad':'Cádiz'}, False  ],
                    # $in reducido
                    [   {'@ciudad':['Sevilla','Córdoba']}, True  ],
                    [   {'@ciudad':['Málaga','Córdoba']}, False  ],
                    [   {'@ciudad':['Málaga','Córdoba','Sevilla']}, True  ],
                    # $in reducido y $and reducido
                    [   {'@ciudad':['Málaga','Córdoba','Sevilla'], '@edad':20}, True  ],
                    [   {'@ciudad':['Málaga','Córdoba'], '@edad':20}, False  ],
                    # operadores: $or
                    [   {'$or':[{'@ciudad':['Málaga','Córdoba']}, {'@edad':20}]}, True  ],
                    [   {'$or':[{'@ciudad':['Málaga','Córdoba']}, {'@edad':21}]}, False  ],
                    [   {'$or':[{'@ciudad':['Málaga','Sevilla','Córdoba']}, {'@edad':20}]}, True  ],
                    # operadores: $or, $ne, $nin
                    [   {'$or':[{'@ciudad':['Málaga','Córdoba']}, {'$ne':['@edad',21]}]}, True  ],
                    [   {'$or':[{'@ciudad':['Málaga','Córdoba']}, {'$ne':['@edad',20]}]}, False  ],
                    [   {'$or':[{'$nin':['@ciudad','Málaga','Córdoba']}, {'$ne':['@edad',20]}]}, True  ],
                    # operador $or, $gt, $nin
                    [   {'$gt':['@edad',23]}, False  ],
                    [   {'$or':[{'$nin':['@ciudad','Málaga','Córdoba']}, {'$gt':['@edad',19]}, {'@peso':65} ]}, True  ],
                    [   {'$or':[{'$nin':['@ciudad','Málaga','Sevilla','Córdoba']}, {'$gt':['@edad',23]}, {'@peso':65} ]}, False  ],
                    # operador $and, $gt, $nin
                    [   {'$and':[{'$nin':['@ciudad','Málaga','Córdoba']}, {'$gt':['@edad',19]} ]}, True  ],
                    [   {'$and':[{'$in':['@ciudad','Málaga','Sevilla','Córdoba']}, {'$gt':['@edad',23]}, {'@peso':65.3} ]}, False  ],
                    [   {'$and':[{'$in':['@ciudad','Málaga','Sevilla','Córdoba']}, {'$gt':['@edad',19]}, {'@peso':65.3} ]}, True  ],
                    # operador $or y $and
                    [   {'$and':[{'$or':[{'@ciudad':'Málaga'},{'@ciudad':'Sevilla'}]}, {'$gt':['@edad',19]} ]}, True  ],
                    [   {'$and':[{'$or':[{'@ciudad':'Málaga'},{'@ciudad':'Sevilla'}]}, {'$lt':['@edad',30]} ]}, True  ],
                    [   {'$and':[{'$or':[{'@ciudad':'Málaga'},{'@ciudad':'Sevilla'}]}, {'$lt':['@edad',20]} ]}, False  ],
                    # entre campos @
                    [   {'@ciudad':'@destino'}, False  ],
                    [   {'@ciudad':'@preferido'}, True  ],
                    [   {'$ne':['@ciudad','@preferido']}, False  ],
                    [   {'$ne':['@ciudad','@destino']}, True  ],
                    [   '@ciudad', 'Sevilla'  ],
                    [   {'$ne':[{'$ne':['@ciudad','@destino']},{'@destino':'Sevilla'}]}, True  ],
                    [   {'$and':[{'$ne':['@ciudad','@destino']},{'@preferido':'Córdoba'}]}, False  ],
                    [   {'$and':[{'$ne':['@ciudad','@destino']},{'@preferido':'Sevilla'}]}, True  ],
                    # caso especial (visto de casualidad), $ne de dos valores booleanos resultados de otras comparaciones
                    [   {'$ne':[{'$ne':['@ciudad','@destino']},{'@preferido':'Sevilla'}]}, False  ],
                    [   {'$ne':[{'$ne':['@ciudad','@destino']},{'@preferido':'Córdoba'}]}, True  ],
                    # $not
                    [   {'$not':[True]}, False  ],
                    # funciones constantes. casos de uso
                    [   {'$db':[]}, 'Lo que sea'  ],
                    [   ['$db'], 'Lo que sea'  ],
                    [   {'$eq':[{'$db':[]},'Lo que sea']}, True  ],
                    [   {'$neq':[{'$db':[]},'Lo que sea']}, False  ],
                    [   {'$eq':['$db','Lo que sea']}, True  ],
                    [   {'$eq':['$db','Lo que sea'],'@ciudad':'Sevilla'}, True  ],
                    [   [{'$eq':['$db','Lo que sea']},{'@ciudad':'Sevilla'}], True  ],
                  ]

        # print('testNormalizar')
        n = 0
        for p in pruebas:
            n = n + 1
            valor = dstools.evalue(dstools.normalizar(p[0]), data)
            self.assertEqual(valor, p[1])
        # print(dstools.evalue(dstools.normalizar({'$not':[True]}), data))
        
    
    def testNormalizar_dos(self):
        '''
        { '$or': [{'ciudad':'Sevilla'}, { {'$round(3)':'peso'} : 40 ] }
        { '$or': [{'ciudad':'Sevilla'}, { {'$round(3)':'peso'} : {'$gte':40} ] }
        { '$or': [{'ciudad':'Sevilla'}, { {'$round(3)':'peso'} : {'$gte':'@maximo'} ] }
        '''
        
        pruebas = [ 
                    # 1
                    [   {'@edad':20},
                        {'$eq':['@edad',20]}   ],
                    # 2
                    [   [{'@edad':20}], 
                        {'$eq':['@edad',20]}],
                    # 3
                    [   [{'@edad':20},{'@ciudad':'Sevilla'}], 
                        {'$and':[{'$eq':['@edad',20]},{'$eq':['@ciudad','Sevilla']}]}    ],
                  
                    # 4
                    [   [{'@edad':20, '@ciudad':'Sevilla'}],
                        [  {'$and':[{'$eq':['@edad',20]},{'$eq':['@ciudad','Sevilla']}]},
                           {'$and':[{'$eq':['@ciudad','Sevilla']},{'$eq':['@edad',20]}]}    ]    ],
                  
                    # 5
                    [   {'@edad':20, '@ciudad':'Sevilla'},
                        [   {'$and':[{'$eq':['@edad',20]},{'$eq':['@ciudad','Sevilla']}]},
                            {'$and':[{'$eq':['@ciudad','Sevilla']},{'$eq':['@edad',20]}]}   ]    ],
                    # 6
                    [   {'$eq':[{'$round':['@edad',1]}, 30]},
                        {'$eq':[{'$round':['@edad',1]}, 30]}    ],
                  
                    # 7
                    [   { '@ciudad':['Sevilla','Huelva'], '$gte':[{'$round':['@peso',10]},'@maximo'] },
                        [    { '$and':[{'$in':['@ciudad','Sevilla','Huelva']}, {'$gte':[{'$round':['@peso',10]},'@maximo']}] },
                             { '$and':[{'$gte':[{'$round':['@peso',10]},'@maximo']}, {'$in':['@ciudad','Sevilla','Huelva']}] }    ]    ],
                    # 8
                    [   { '@ciudad':['Sevilla','Huelva'], '$gte':[{'$round':['@peso',10]},{'$minAcum':['@maximo']}] }, 
                        [    { '$and':[{'$in':['@ciudad','Sevilla','Huelva']}, {'$gte':[{'$round':['@peso',10]},{'$minAcum':['@maximo']}]}] },
                             { '$and':[{'$gte':[{'$round':['@peso',10]},{'$minAcum':['@maximo']}]}, {'$in':['@ciudad','Sevilla','Huelva']}] }    ]    ],
                    # 9
                    [   { '$or':[{'@ciudad':['Sevilla','Huelva']}, {'@peso':{'$minAcum':['@maximo']}} ] }, 
                        [    { '$or':[{'$in':['@ciudad','Sevilla','Huelva']}, {'$eq':['@peso',{'$minAcum':['@maximo']}]}] },
                             { '$or':[{'$eq':['@peso',{'$minAcum':['@maximo']}]}, {'$in':['@ciudad','Sevilla','Huelva']}] }    ]    ]
                    
                         
                  ]
        
        print_debug = False
        # print('testNormalizar')
        n = 0
        for p in pruebas:
            n = n + 1
            if print_debug:
                print()
                print('*'*40)
                print()
                print('Prueba',str(n),p)
                print()
            normalizado = dstools.normalizar(p[0])
            if p[1].__class__.__name__ == 'list':
                if print_debug:
                    print('Es una lista de posibles valores válidos...')
                    print('A normalizar:')
                    print(p[0])
                    print('Normalizado:')
                    print(normalizado)
                resultado = False
                # print('...--- ',p[1])
                for r in p[1]:
                    if print_debug:
                        print('Valor a comparar:')
                        print(r)
                    if r == normalizado:
                        resultado = True
                if print_debug:
                    print('Fin de valores con los que comparar')
                
                self.assertTrue(resultado)
            else:
                if print_debug:
                    print('Solo hay un valor válido con el que comparar:')
                    print(p[1])
                    print('A normalizar:')
                    print(p[0])
                    print('Normalizado:')
                    print(normalizado)
                self.assertEqual(normalizado, p[1])
            
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()