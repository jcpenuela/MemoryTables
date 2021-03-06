'''
Created on 08/08/2013

@author: jcpenuela
'''
import unittest
import src.persona as persona
import src.dataset as dataset
import src.query as query


class MemoryListTest(unittest.TestCase):


    def setUp(self):
        self.tabla = dataset.Dataset()
        datos = carga_datos2()
        for k,v in datos.items():
            self.tabla.insert(v)
        self.tabla.index('ciudad','ciudad')
        self.tabla.index('pru','peso')
    
    def tearDown(self):
        pass

    def test_insert(self):
        # print('testInsert.....')
        self.assertEqual(self.tabla.count(), 8)
        # No debe insertar el nodo al estar duplicado
        self.tabla.insert(persona.Persona('S18', 'Sevilla', 18, 45.6))
        self.assertEqual(sorted(list(self.tabla.select().keys())), [1,2,3,4,5,6,7,8])
        self.tabla.insert(persona.Persona('S18', 'Sevilla', 18, 48))
        self.assertEqual(sorted(list(self.tabla.select().keys())), [1,2,3,4,5,6,7,8,9])
        self.tabla.insert(persona.Persona('S18', 'Sevilla', 18, 48))
        self.assertEqual(sorted(list(self.tabla.select().keys())), [1,2,3,4,5,6,7,8,9])
        self.tabla.insert(persona.Persona('S18', 'Sevilla', 18, 48), force = True)
        self.assertEqual(sorted(list(self.tabla.select().keys())), [1,2,3,4,5,6,7,8,9,10])
        
        
    def test_select(self):
        # print('testSelect.....')
        t = self.tabla
        seleccionados = t.select({'#':1})
        self.assertEqual(list(seleccionados.keys()), [1])
        seleccionados = t.select({'#':[1,3]})
        self.assertEqual(list(seleccionados.keys()), [1,3]) 
        seleccionados = t.select({'#':9})
        self.assertEqual(list(seleccionados.keys()), [])
        seleccionados = t.select({'#':[4,9]})
        self.assertEqual(list(seleccionados.keys()), [4])        
        seleccionados =  t.select({'#':[1,9]})
        self.assertEqual(list(seleccionados.keys()), [1])
        seleccionados = t.select({'!_hash':2027290602588602042})
        self.assertEqual(list(seleccionados.keys()), [1])
        seleccionados = t.select({'!_hash':[1026315136059584805,1009972526877977308]})
        self.assertEqual(sorted(list(seleccionados.keys())), [5,7])
        seleccionados = t.select({'!ciudad':['Sevilla','Córdoba','Huelva']})
        self.assertEqual(list(seleccionados.keys()), [1,2,3,4,5,6])
        seleccionados = t.select({'@nombre': 'S30'})
        self.assertEqual(list(seleccionados.keys()), [2])
        seleccionados = t.select({'@ciudad':['Sevilla','Cádiz']})
        self.assertEqual(sorted(list(seleccionados.keys())), [1,2,7,8])
        seleccionados = t.select(lambda x:x.ciudad in ('Sevilla','Cádiz'))
        self.assertEqual(sorted(list(seleccionados.keys())), [1,2,7,8])
        seleccionados = t.select(lambda x:x.edad >= 40)
        self.assertListEqual(sorted(list(seleccionados.keys())), [5,7])

        
        
    def test_query(self):
        # print('testQuery.....')
        t = self.tabla
        q = query.Query()
        q.add_and({'@ciudad':'Sevilla'})
        seleccionados = t.select(q)
        self.assertListEqual(sorted(list(seleccionados.keys())), [1,2])
        q.add_or({'@ciudad':'Huelva'})
        seleccionados = t.select(q)
        self.assertListEqual(sorted(list(seleccionados.keys())), [1,2,3,4])
        q.add_and({'$gt':['@edad',20]})
        seleccionados = t.select(q)
        self.assertListEqual(sorted(list(seleccionados.keys())), [2,4], q.get_query())
        q.add_not()
        seleccionados = t.select(q)
        self.assertListEqual(sorted(list(seleccionados.keys())), [1,3,5,6,7,8], q.get_query())
    

    
    
    def test_select_ids(self):
        # print('testSelect.....')
        t = self.tabla
        seleccionados = t.select_ids({'#':1})
        self.assertEqual(seleccionados, [1])
        seleccionados = t.select_ids({'#':[1,3]})
        self.assertEqual(seleccionados, [1,3])
        seleccionados = t.select_ids({'#':'1+2'}) # Evalua la expresión
        self.assertEqual(seleccionados, [3])
        seleccionados = t.select_ids({'#':'max(1,3,2)'}) # Evalua la expresión
        self.assertEqual(seleccionados, [3])
        seleccionados = t.select_ids({'#':9})
        self.assertEqual(seleccionados, [])
        seleccionados = t.select_ids({'#':[4,9]})
        self.assertEqual(seleccionados, [4])
        seleccionados =  t.select_ids({'#':[1,9]})
        self.assertEqual(seleccionados, [1])
        seleccionados = t.select_ids({'!_hash':2027290602588602042})
        self.assertEqual(seleccionados, [1])
        seleccionados = t.select_ids({'!_hash':[1026315136059584805,1009972526877977308]})
        self.assertEqual(sorted(seleccionados), [5,7])
        seleccionados = t.select_ids({'@nombre':'S30'})
        self.assertEqual(seleccionados, [2])
        seleccionados = t.select_ids({'@ciudad':['Sevilla','Cádiz']})
        self.assertEqual(sorted(seleccionados), [1,2,7,8])
        seleccionados = t.select_ids(lambda x:x.ciudad in ('Sevilla','Cádiz'))
        self.assertEqual(sorted(seleccionados), [1,2,7,8])
        seleccionados = t.select_ids(lambda x:x.edad >= 40)
        self.assertListEqual(sorted(seleccionados), [5,7])
        
        
        
    
    def test_delete(self):
        # print('testDelete.....')
        t = self.tabla
        t.delete({'#':1})
        self.assertEqual(sorted(list(t.nodes.keys())), [2,3,4,5,6,7,8])
        t.delete({'!_hash':[1026315136059584805,1009972526877977308]})
        self.assertEqual(sorted(list(t.nodes.keys())), [2,3,4,6,8])
        t.delete({'@nombre':'S30'})
        self.assertEqual(sorted(list(t.nodes.keys())), [3,4,6,8])
        t.delete(lambda x:x.ciudad in ('Sevilla','Cádiz'))
        self.assertEqual(sorted(list(t.nodes.keys())), [3,4,6])
        q = query.Query()
        # q.add_and({'$gt':['@peso',80]})
        q.add_and({'@peso':82.5})
        t.delete(q)
        # self.assertEqual(sorted(list(t.nodes.keys())), [3,6])
        self.assertEqual(sorted(list(t.nodes.keys())), [6])
        t.insert(persona.Persona('S18', 'Sevilla', 18, 45.6))
        # self.assertEqual(sorted(list(t.nodes.keys())), [3,6,9])
        self.assertEqual(sorted(list(t.nodes.keys())), [6,9])
        
        
    def test_updates(self):
        t = self.tabla
        anterior = t.select_ids({'@nombre':'S18'})
        self.assertEqual(anterior,[1])
        p = persona.Persona('J35', 'Jaén', 20, 70.5)
        nuevo_id = t.update({'#':1},p)
        self.assertEqual(nuevo_id,9)
        anterior = t.select({'@nombre':'S18'})
        self.assertEqual(anterior,{})

    
    def test_upsert(self):
        t = self.tabla
        anterior = t.select_ids({'@nombre':'S18'})
        self.assertEqual(anterior,[1])
        p = persona.Persona('J35', 'Jaén', 20, 70.5)
        nuevo_id = t.update({'#':1},p)
        self.assertEqual(nuevo_id,9)
        anterior = t.select({'@nombre':'S18'})
        self.assertEqual(anterior,{})        
        

    def test_modify(self):
        t = self.tabla
        anterior = t.select_ids({'@nombre':'S18'})
        self.assertEqual(anterior,[1])
        nuevo_id = t.modify({'#':1},{'nombre':'S99'})
        self.assertEqual(nuevo_id,[1])
        anterior = t.select({'@nombre':'S18'})
        self.assertEqual(anterior,{})
        anterior = t.select_ids({'@nombre':'S99'})
        self.assertEqual(anterior,[1])
        anterior = t.select_ids({'@nombre':'H19'})
        self.assertEqual(anterior,[3])
        anterior = t.select_ids({'@ciudad':'Huelva'})
        self.assertEqual(anterior,[3,4])
        nuevo_id = t.modify({'@nombre':'H19'},{'ciudad':'@nombre'})
        anterior = t.select_ids({'@ciudad':'Huelva'})
        self.assertEqual(anterior,[4])
        anterior = t.select_ids({'@ciudad':'H19'})
        self.assertEqual(anterior,[3])
        nuevo_id = t.modify({'@nombre':'H19'},{'ciudad':'Huelva'})
        self.assertEqual(anterior,[3])
        anterior = t.select_ids({'@ciudad':'Huelva'})
        self.assertEqual(anterior,[3,4])
        nuevo_id = t.modify({'@nombre':'H19'},{'es_huelva':'Otra'})
        self.assertEqual(nuevo_id,[3])
        anterior = t.select_ids({'@es_huelva':'Otra'})
        self.assertEqual(anterior,[3])
        # la modificación siguiente consiste en ejecutar una función del propio lenguaje
        nuevo_id = t.modify({'@es_huelva':'Otra'},{'$del_attribute':['es_huelva']})
        self.assertEqual(nuevo_id,[3])
        anterior = t.select_ids({'@es_huelva':'Otra'})
        self.assertEqual(anterior,[])


    def test_connect(self):
        t = self.tabla
        n1 = t.select({'@nombre':'S30'})
        self.assertEqual(n1[2].nombre, 'S30')
        t.connect({'@nombre':'S30'},{'@nombre':'C40'})
        self.assertEqual(t.linked_set({'@nombre':'S30'}), [[2,5]])
        t.connect({'@nombre':'S30'},{'@nombre':'Z29'})
        self.assertEqual(t.linked_set(), [[2,5],[2,8]])
        t.connect({'@nombre':'S30'},{'@nombre':'Z29'})
        self.assertEqual(t.linked_set(), [[2,5],[2,8]])
        t.connect({'@nombre':'S30'},{'@ciudad':'Sevilla'})
        self.assertEqual(sorted(t.linked_set()), [[2,1],[2,2],[2,5],[2,8]])
        
    def test_copiarDS(self):
        t = self.tabla
        
        new_ds = t.select_dataset({'@ciudad':'Sevilla'})
        self.assertEqual(new_ds.count(), 2)
        self.assertEqual(new_ds.linked_set(), [])
        
        t.connect({'@nombre':'S30'},{'@ciudad':['Sevilla','Cádiz']})
        new_ds = t.select_dataset({'@ciudad':'Sevilla'})
        self.assertEqual(new_ds.count(), 2)
        self.assertEqual(new_ds.linked_set(), [])
        
        # print('---------------------')
        #####################
        # VERIFICAR QUE AL COPIAR EL DS NO SE HACE REFERENCIA AL
        # MISMO OBJETO
        #####################
        new_ds = t.select_dataset({'@ciudad':'Sevilla'},True)
        self.assertEqual(new_ds.count(), 4)
        # print(new_ds.nodes)
        # print(t.nodes)
        # print(new_ds.links)
        # print(t.links)
        self.assertEqual(sorted(new_ds.linked_set()), [[2,1],[2,2],[2,3],[2,4]])
        self.assertEqual(new_ds.is_connected({'@nombre':'S30'},{'@ciudad':['Sevilla','Cádiz']}), True)
        
        # El siguiente es TRUE porque no tenemos 'Córdoba' en el nuevo dataset, así que el resultado
        # es que entre S30 y Sevilla SI ESTAN TODOS CONECTADOS
        self.assertEqual(new_ds.is_connected({'@nombre':'S30'},{'@ciudad':['Sevilla','Córdoba']}), True)
        self.assertEqual(t.is_connected({'@nombre':'S30'},{'@ciudad':['Sevilla']}), True)
        self.assertEqual(t.is_connected({'@nombre':'S30'},{'@ciudad':['Córdoba']}), False)
        # print('l>>>>>>')
        # TODO: Test de linked_nodes()
        t.linked_nodes({'@nombre':'S30'})


    def test_planesEjecucion(self):
        t = self.tabla
        new_ds = t.select_dataset({'@ciudad':'Sevilla'})
        
        
        


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