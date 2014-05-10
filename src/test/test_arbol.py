'''
Created on 08/08/2013

@author: jcpenuela
'''
import unittest
import src.EXPTree as EXPTree


class EXPTreeTest(unittest.TestCase):


    def setUp(self):
        self.tree = EXPTree.EXPTree()

    def tearDown(self):
        pass

    def test_insert(self):
        # print('testInsert.....')
        n = EXPTree.EXPNode('1')
        self.tree.add_node_as_root(n)
        self.assertEqual(self.tree.root, 0)
        n = EXPTree.EXPNode('0')
        self.tree.add_node_as_root(n)
        self.assertEqual(self.tree.root, 1)
        self.assertEqual(self.tree.fathers[0], 1)
        self.assertEqual(self.tree.sons[1], [0])
        self.assertEqual(self.tree.sons[0], [])
        n = EXPTree.EXPNode('2')
        self.tree.add_node_at_right(n,1)
        self.assertEqual(self.tree.root, 1)
        self.assertEqual(self.tree.fathers[0], 1)
        self.assertEqual(self.tree.fathers[2], 1)
        self.assertEqual(self.tree.sons[1], [0,2])
        self.assertEqual(self.tree.sons[0], [])
        self.assertEqual(self.tree.sons[2], [])
        n = EXPTree.EXPNode('3')  # [1:[0,2,3]]
        self.tree.add_node_at_right(n,1)
        self.assertEqual(self.tree.fathers[3], 1)
        self.assertEqual(self.tree.sons[1], [0,2,3])
        n = EXPTree.EXPNode('4')  # [1:[4,0,2,3]]
        self.tree.add_node_at_left(n,1)
        self.assertEqual(self.tree.fathers[4], 1)
        self.assertEqual(self.tree.sons[1], [4,0,2,3])
        n = EXPTree.EXPNode('5')  # [1:[4,0,5,2,3]]
        self.tree.add_node_at_position(n,1,2)
        self.assertEqual(self.tree.fathers[5], 1)
        self.assertEqual(self.tree.sons[1], [4,0,5,2,3])
        n = EXPTree.EXPNode('6')  # [1:[4,0,5:[6],2,3]]
        self.tree.add_node_at_left(n,5)
        self.assertEqual(self.tree.fathers[6], 5)
        self.assertEqual(self.tree.sons[1], [4,0,5,2,3])
        self.assertEqual(self.tree.sons[5], [6])
        n = EXPTree.EXPNode('7')  # [1:[4,0,5:[6,7],2,3]]
        self.tree.add_node_at_right(n,5)
        self.assertEqual(self.tree.fathers[7], 5)
        self.assertEqual(self.tree.sons[1], [4,0,5,2,3])
        self.assertEqual(self.tree.sons[5], [6,7])
        n = EXPTree.EXPNode('8')  # [1:[4,0,5:[8:[6],7],2,3]]
        self.tree.add_node_as_father(n,6)
        self.assertEqual(self.tree.fathers[6], 8)
        self.assertEqual(self.tree.sons[1], [4,0,5,2,3])
        self.assertEqual(self.tree.sons[5], [8,7])
        self.assertEqual(self.tree.sons[8], [6])
        n = EXPTree.EXPNode('9')  # [1:[4,0,5:[8:[6],9,7],2,3]]
        self.tree.add_node_at_position(n,5,1)
        # print(self.tree.fathers)
        self.assertEqual(self.tree.sons[5], [8,9,7])
        n = EXPTree.EXPNode('10')  # [1:[4,0,5:[10,8:[6],9,7],2,3]]
        self.tree.add_node_at_position(n,5,0)
        # print(self.tree.fathers)
        self.assertEqual(self.tree.sons[5], [10,8,9,7])
        n = EXPTree.EXPNode('11')  # [1:[4,0,5:[10,8:[6,11],9,7],2,3]]
        self.tree.add_node_at_right(n,8)
        # print(self.tree.fathers)
        self.assertEqual(self.tree.sons[5], [10,8,9,7])
        self.assertEqual(self.tree.sons[8], [6,11])
        n = EXPTree.EXPNode('12')  # [1:[4,0,5:[10,12:[8:[6,11]],9,7],2,3]]
        self.tree.add_node_as_father(n,8)
        # print(self.tree.fathers)
        self.assertEqual(self.tree.sons[5], [10,12,9,7])
        self.assertEqual(self.tree.sons[12], [8])
        self.assertEqual(self.tree.fathers[8], 12)
        n = EXPTree.EXPNode('13')  # [1:[4,0,5:[10,12:[13:[8:[6,11]]],9,7],2,3]]
        self.tree.add_node_as_father(n,8)
        # print(self.tree.fathers)
        self.assertEqual(self.tree.sons[5], [10,12,9,7])
        self.assertEqual(self.tree.sons[12], [13])
        self.assertEqual(self.tree.fathers[8], 13)
        n = EXPTree.EXPNode('14')  # [1:[4,0,5:[10,12:[13:[8:[6,11]]],9,7],2,14,3]]
        self.tree.add_node_at_position(n,1,4)
        # print(self.tree.fathers)
        self.assertEqual(self.tree.sons[1], [4,0,5,2,14,3])
        n = EXPTree.EXPNode('15')  # [15:[1:[4,0,5:[10,12:[13:[8:[6,11]]],9,7],2,14,3]]]
        self.tree.add_node_as_father(n,1)
        # print(self.tree.fathers)
        self.assertEqual(self.tree.sons[15], [1])


    def test_del_subtree(self):
        self.tree = load_tree() # [15:[1:[4,0,5:[10,12:[13:[8:[6,11]]],9,7],2,14,3]]]
        print('------------------')
        print(self.tree.nodes)
        print('------------------')
        self.assertEqual(self.tree.sons[8], [6,11])
        self.tree.delete_subtree(11) # [15:[1:[4,0,5:[10,12:[13:[8:[6]]],9,7],2,14,3]]]
        self.assertEqual(self.tree.sons[8], [6])
        self.tree.delete_subtree(12) # [15:[1:[4,0,5:[10,9,7],2,14,3]]]
        self.assertEqual(self.tree.sons[5], [10,9,7])
        print('------------------')
        print(self.tree.nodes)
        print('------------------')

def load_tree():
    tree = EXPTree.EXPTree()
    n = EXPTree.EXPNode('1')
    tree.add_node_as_root(n)
    n = EXPTree.EXPNode('0')
    tree.add_node_as_root(n)
    n = EXPTree.EXPNode('2')
    tree.add_node_at_right(n,1)
    n = EXPTree.EXPNode('3')  # [1:[0,2,3]]
    tree.add_node_at_right(n,1)
    n = EXPTree.EXPNode('4')  # [1:[4,0,2,3]]
    tree.add_node_at_left(n,1)
    n = EXPTree.EXPNode('5')  # [1:[4,0,5,2,3]]
    tree.add_node_at_position(n,1,2)
    n = EXPTree.EXPNode('6')  # [1:[4,0,5:[6],2,3]]
    tree.add_node_at_left(n,5)
    n = EXPTree.EXPNode('7')  # [1:[4,0,5:[6,7],2,3]]
    tree.add_node_at_right(n,5)
    n = EXPTree.EXPNode('8')  # [1:[4,0,5:[8:[6],7],2,3]]
    tree.add_node_as_father(n,6)
    n = EXPTree.EXPNode('9')  # [1:[4,0,5:[8:[6],9,7],2,3]]
    tree.add_node_at_position(n,5,1)
    n = EXPTree.EXPNode('10')  # [1:[4,0,5:[10,8:[6],9,7],2,3]]
    tree.add_node_at_position(n,5,0)
    n = EXPTree.EXPNode('11')  # [1:[4,0,5:[10,8:[6,11],9,7],2,3]]
    tree.add_node_at_right(n,8)
    n = EXPTree.EXPNode('12')  # [1:[4,0,5:[10,12:[8:[6,11]],9,7],2,3]]
    tree.add_node_as_father(n,8)
    n = EXPTree.EXPNode('13')  # [1:[4,0,5:[10,12:[13:[8:[6,11]]],9,7],2,3]]
    tree.add_node_as_father(n,8)
    n = EXPTree.EXPNode('14')  # [1:[4,0,5:[10,12:[13:[8:[6,11]]],9,7],2,14,3]]
    tree.add_node_at_position(n,1,4)
    n = EXPTree.EXPNode('15')  # [15:[1:[4,0,5:[10,12:[13:[8:[6,11]]],9,7],2,14,3]]]
    tree.add_node_as_father(n,1)
    return tree

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()