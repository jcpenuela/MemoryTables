'''
Created on 08/08/2013

@author: jcpenuela
'''
import unittest
import fact as Fact
from dataset import Dataset


class MemoryListTest(unittest.TestCase):


    def setUp(self):
        self.tabla = Dataset()


    def tearDown(self):
        pass


    def testUpdates(self):
        t = self.tabla
        
        f = Fact.Fact("uno")
        t.add_element(f)
        f = Fact.Fact("dos")
        t.add_element(f)
        f = Fact.Fact("tres")
        t.add_element(f)
        
        f.set_fact("DOS")
        
        t.update_element(f, 2, False)
        self.assertEqual(t[2].Fact, "DOS" )


    def testIndex(self):
        t = self.tabla
        
        f = Fact.Fact("uno")
        t.add_element(f)
        f = Fact.Fact("dos")
        t.add_element(f)
        f = Fact.Fact("tres")
        t.add_element(f)

        t._index_by('hecho', f.content)
 



    def testBorrados(self):
        t = self.tabla
        
        f = Fact.Fact("uno")
        t.add_element(f)
        f = Fact.Fact("dos")
        t.add_element(f)
        f = Fact.Fact("tres")
        t.add_element(f)
        
        self.assertEqual(t.count(), 3)
        self.assertEqual(t[2].Fact, "dos")
        
        t.delete_element(2)
        self.assertEqual(t[2], None)
        
        f = Fact.Fact("cuatro")
        t.add_element(f)
        self.assertEqual(t[4].Fact, "cuatro")
        
        self.assertEqual(t.count(), 3)
        
        

    def testReferencias(self):
        f = Fact.Fact("original")
        self.tabla.add_element(f)
        
        # g es deepcopy del elemento de la tabla
        g = self.tabla.get_element(1)
        self.assertEqual(g.content(), "original")
        
        # cambiamos el objeto original
        f.set_fact("cambiado")
        self.assertEqual(f.content(), "cambiado")
        self.assertEqual(g.content(), "original")
        g.set_fact("nuevo G")
        self.assertEqual(f.content(), "cambiado")
        self.assertEqual(g.content(), "nuevo G")
         
        g2 = self.tabla.get_element(1)
        self.assertEqual(g2.content(), "original")
        self.assertEqual(f.content(), "cambiado")
        self.assertEqual(g.content(), "nuevo G")
        
        g3 = self.tabla.get_element(1,True)
        g3.set_fact("Cambiado por referencia")
        self.assertEqual(g2.content(), "original")
        self.assertEqual(f.content(), "cambiado")
        self.assertEqual(g.content(), "nuevo G")
        self.assertEqual(g3.content(), "Cambiado por referencia")

        g4 = self.tabla[1]
        self.assertEqual(g2.content(), "original")
        self.assertEqual(f.content(), "cambiado")
        self.assertEqual(g.content(), "nuevo G")
        self.assertEqual(g3.content(), "Cambiado por referencia")
        self.assertEqual(g4.content(), "Cambiado por referencia")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()