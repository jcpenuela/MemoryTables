'''
Created on 08/08/2013

@author: jcpenuela
'''
import unittest
import persona
import dataset
import query


class MemoryListTest(unittest.TestCase):


    def setUp(self):
        print('setUp.....')
        self.tabla = dataset.Dataset()
        datos = carga_datos2()
        for k,v in datos.items():
            self.tabla.insert(v)
    
    def tearDown(self):
        pass


    def testInsert(self):
        print('testInsert.....')
        self.assertEqual(self.tabla.count(), 8)
        
        
    def testSelect(self):
        print('testSelect.....')
        t = self.tabla
        seleccionados = t.select2({'#':1})
        self.assertEqual(list(seleccionados.keys()), [1])
        seleccionados = t.select2({'#':[1,3]})
        self.assertEqual(list(seleccionados.keys()), [1,3]) 
        seleccionados = t.select2({'#':9})
        self.assertEqual(list(seleccionados.keys()), [])
        seleccionados = t.select2({'#':[4,9]})
        self.assertEqual(list(seleccionados.keys()), [4])
        seleccionados =  t.select2({'#':[1,9]})
        self.assertEqual(list(seleccionados.keys()), [1])
        seleccionados = t.select2({'@_hash':2027290602588602042})
        self.assertEqual(list(seleccionados.keys()), [1])
        seleccionados = t.select2({'@_hash':[1026315136059584805,1009972526877977308]})
        self.assertEqual(sorted(list(seleccionados.keys())), [5,7])
        seleccionados = t.select2({'nombre':'S30'})
        self.assertEqual(list(seleccionados.keys()), [2])
        seleccionados = t.select2({'ciudad':['Sevilla','Cádiz']})
        self.assertEqual(sorted(list(seleccionados.keys())), [1,2,7,8])
        seleccionados = t.select2(lambda x:x.ciudad in ('Sevilla','Cádiz'))
        self.assertEqual(sorted(list(seleccionados.keys())), [1,2,7,8])
        seleccionados = t.select2(lambda x:x.edad >= 40)
        self.assertListEqual(sorted(list(seleccionados.keys())), [5,7])
 
    def testQuery(self):
        print('testQuery.....')
        t = self.tabla
        q = query.Query()
        q.add_and({'ciudad':'Sevilla'})
        seleccionados = t.select2(q)
        self.assertListEqual(sorted(list(seleccionados.keys())), [1,2])
        q.add_or({'ciudad':'Huelva'})
        seleccionados = t.select2(q)
        self.assertListEqual(sorted(list(seleccionados.keys())), [1,2,3,4])
        q.add_and({'edad':{'$gt',20}})
        seleccionados = t.select2(q)
        self.assertListEqual(sorted(list(seleccionados.keys())), [2,4], q.get_query())
        
        
    
    def testDelete(self):
        print('testDelete..... pendiente')
        
    # def MuestraHash(self):
    #     for k,v in self.tabla:
    #        print(k, v.nombre, hash(v))
    #        

 
def carga_datos():
    d = dict()
    d[1] = {'nombre': 'S18', 'ciudad':'Sevilla', 'edad':18, 'peso':45.6 }
    d[2] = {'nombre': 'S30', 'ciudad':'Sevilla', 'edad':30, 'peso':60.2 }
    d[3] = {'nombre': 'H19', 'ciudad':'Huelva', 'edad':19, 'peso':75.3 }
    d[4] = {'nombre': 'H25', 'ciudad':'Huelva', 'edad':25, 'peso':82.6 }
    d[5] = {'nombre': 'C40', 'ciudad':'Córdoba', 'edad':40, 'peso':59.2 }
    d[6] = {'nombre': 'C35', 'ciudad':'Córdoba', 'edad':35, 'peso':63.1 }
    d[7] = {'nombre': 'Z42', 'ciudad':'Cádiz', 'edad':42, 'peso':75.5 }
    d[8] = {'nombre': 'Z29', 'ciudad':'Cádiz', 'edad':29, 'peso':85.8 }
    return d

def carga_datos2():
    d = dict()
    p = persona.Persona('S18', 'Sevilla', 18, 45.6)
    d[1] = p
    p = persona.Persona('S30', 'Sevilla', 30, 60.2)
    d[2] = p
    p = persona.Persona('H19', 'Huelva', 19, 75.3)
    d[3] = p
    p = persona.Persona('H25', 'Huelva', 25, 82.6)
    d[4] = p
    p = persona.Persona('C40', 'Córdoba', 40, 59.2)
    d[5] = p
    p = persona.Persona( 'C35', 'Córdoba', 35, 63.1)
    d[6] = p
    p = persona.Persona('Z42', 'Cádiz', 42, 75.5)
    d[7] = p
    p = persona.Persona('Z29', 'Cádiz', 29, 85.8)
    d[8] = p
    return d
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()