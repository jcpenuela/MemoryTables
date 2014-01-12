'''
Created on 11/01/2014

@author: jcpenuela
'''
import unittest
import matcher
import fact


class Test(unittest.TestCase):


    def setUp(self):
        self.lista_nodos = list()
        for i in range(0,10):
            n = fact.Fact('A_'+str(i))
            self.lista_nodos.append(n)
        

    def tearDown(self):
        pass


    def testExpression(self):
        expression = {'fact':'A'}
        m = matcher.Matcher(expression)
        self.assertDictEqual(expression, m.query_expression)
        self.assertTrue(m.match(self.lista_nodos[0]))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testExpression']
    unittest.main()