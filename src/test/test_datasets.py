'''
Created on 08/08/2013

@author: jcpenuela
'''
import unittest
import fact
import dataset


class MemoryListTest(unittest.TestCase):


    def setUp(self):
        print('setUp.....')
        self.tabla = dataset.Dataset()
        f = fact.Fact("uno") # 420534919696307790
        # print('hash f:',hash(f))
        self.tabla.insert(f)
        f2 = fact.Fact("dos") # 1877651724996747602
        # print('hash f:',hash(f2))
        self.tabla.insert(f2)
        f3 = fact.Fact("uno") # 420534919696307790
        # print('hash f:',hash(f3))
        self.tabla.insert(f3)
        # self.tabla.dump_data()               

    def tearDown(self):
        pass


    def testInsert(self):
        print('testInsert.....')
        self.assertEqual(self.tabla.count(), 3)
        
        
    def testSelect(self):
        print('testSelect.....')
        t = self.tabla
        seleccionados = t.select({'#':1})
        self.assertEqual(list(seleccionados.keys()), [1])
        seleccionados = t.select({'#':[1,3]})
        self.assertEqual(list(seleccionados.keys()), [1,3]) 
        seleccionados = t.select({'#':9})
        self.assertEqual(list(seleccionados.keys()), [])
        seleccionados = t.select({'#':[4,9]})
        self.assertEqual(list(seleccionados.keys()), [])
        seleccionados =  t.select({'#':[1,9]})
        self.assertEqual(list(seleccionados.keys()), [1])
        seleccionados = t.select({'@_hash':1877651724996747602})
        self.assertEqual(list(seleccionados.keys()), [2])
        seleccionados = t.select({'hecho':'hecho.Fact == "uno"'})
        self.assertEqual(list(seleccionados.keys()), [1,3])
 
    def testDelete(self):
        print('testDelete.....')
        t = self.tabla
 
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()