'''
Created on 08/08/2013

@author: jcpenuela
'''
import unittest
import persona
import dataset
import optimize


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

    def testPlanesEjecucion(self):
        optima = optimize.optimizer({'@nombre':'S30', '@ciudad':'Sevilla'},self.tabla)        
        # self.assertEqual(optima, {'$and':[{'$eq':['@Ciudad','Sevilla']},{'$eq':['@nombre','S30']}]})
        
        
        



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