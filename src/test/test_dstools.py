'''
Created on 08/08/2013

@author: jcpenuela
'''
import unittest
import dstools


class Dstools(unittest.TestCase):


    def setUp(self):
        pass
    
    def tearDown(self):
        pass


    def testNormalizar(self):
        # print('testNormalizar')
        condition = {'edad':{'$gt':20}}
        q = dstools.normalizar(condition)
        self.assertEqual(q, {'edad':{'$gt':20}}, q)
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()