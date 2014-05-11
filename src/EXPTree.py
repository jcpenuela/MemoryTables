__author__ = 'Juan Carlos'

class EXPTreeExceptionBadRenumberInit(Exception):
    pass

class EXPNode(object):
    def __init__(self, text):
        self.text = text
        self.type = None # Tipo operador o argumento de expresión...

class EXPTree(object):
    def __init__(self):
        self.nodes = dict()
        self.root = None
        self.sons = dict() # {1:[2,3], 2:[4,5]}
        self.fathers = dict() # {2:1, 3:1, 4:2, 5:2}
        self.last_node_id = -1

    def _next_node_id(self):
        self.last_node_id += 1
        return self.last_node_id

    def add_node_as_root(self, new_node):
        new_node_id = self._next_node_id()
        if self.root is None:
            # es el primer nodo insertado
            self.fathers[new_node_id] = None
            self.sons[new_node_id] = []
        else:
            # ya hay nodos
            self.fathers[new_node_id] = None
            self.sons[new_node_id] = [self.root]
            self.fathers[self.root] = new_node_id
        self.root = new_node_id
        self.nodes[new_node_id] = new_node
        return new_node_id

    def add_node_at_left(self, new_node, father=None):
        if father is None:
            return self.add_node_as_root(new_node)
        if father not in self.fathers:
            raise Exception('Nodo id: ' + father + ' no existe')
        new_node_id = self._next_node_id()
        self.sons[father] = [new_node_id] + self.sons[father]
        self.fathers[new_node_id]=father
        self.sons[new_node_id]=[]
        self.nodes[new_node_id] = new_node
        return new_node_id

    def add_node_at_right(self, new_node, father=None):
        if father is None:
            return self.add_node_as_root(new_node)
        if father not in self.fathers:
            raise Exception('Nodo id: ' + father + ' no existe')
        new_node_id = self._next_node_id()
        self.sons[father] = self.sons[father] + [new_node_id]
        self.fathers[new_node_id]=father
        self.sons[new_node_id]=[]
        self.nodes[new_node_id] = new_node
        return new_node_id

    def add_node_at_position(self, new_node, father, position=0):
        """
        Inserta 'new_node', como hijo de 'father' id en posición 'position'
        """
        # print('fathers', self.fathers)
        if father not in self.fathers:
            raise Exception('Nodo id: ' + father + ' no existe')
        if len(self.sons[father]) < position:
            return self.add_node_at_right(new_node, father)
        elif position == 0:
            return self.add_node_at_left(new_node, father)
        else:
            new_node_id = self._next_node_id()
            self.sons[father] = self.sons[father][0:position] + [new_node_id] + self.sons[father][position:]
            self.fathers[new_node_id]=father
            self.sons[new_node_id]=[]
            self.nodes[new_node_id] = new_node
        return new_node_id

    def renumber_existent_nodes(self, new_initial_node_id):
        if new_initial_node_id <= self.last_node_id:
            raise EXPTreeExceptionBadRenumberInit()
        nodes_to_renumber = list(self.nodes.keys())
        for node_id in nodes_to_renumber:
            self.nodes[node_id + new_initial_node_id] = self.nodes[node_id]
            del(self.nodes[node_id])
        nodes_to_renumber = list(self.fathers.keys())
        for node_id in nodes_to_renumber:
            self.fathers[node_id + new_initial_node_id] = self.fathers[node_id]
            del(self.fathers[node_id])
        nodes_to_renumber = list(self.sons.keys())
        for father_id in nodes_to_renumber:
            self.sons[father_id + new_initial_node_id] = []
            for son_id in self.sons[father_id]:
                self.sons[father_id + new_initial_node_id].append(son_id + new_initial_node_id)
            del(self.sons[father_id])
        self.root = self.root + new_initial_node_id
        return [self.root, self.last_node_id]


    def add_tree_at_left(self, new_tree, father):
        if father not in self.fathers:
            raise Exception('Nodo id: ' + father + ' no existe')
        [new_subtree_root_id, new_last_node_id] = new_tree.renumber_existent_nodes(self.last_node_id + 1)
        self.sons[father] = [new_subtree_root_id] + self.sons[father]
        self.fathers.update(new_tree.fathers)
        self.fathers[new_subtree_root_id]=father
        self.sons.update(new_tree.sons)
        self.nodes.update(new_tree.nodes)
        self.last_node_id = new_last_node_id
        return new_subtree_root_id


    def add_tree_at_right(self, new_tree, father):
        if father not in self.fathers:
            raise Exception('Nodo id: ' + father + ' no existe')
        [new_subtree_root_id, new_last_node_id] = new_tree.renumber_existent_nodes(self.last_node_id + 1)
        self.sons[father] = self.sons[father] + [new_subtree_root_id]
        self.fathers.update(new_tree.fathers)
        self.fathers[new_subtree_root_id]=father
        self.sons.update(new_tree.sons)
        self.nodes.update(new_tree.nodes)
        self.last_node_id = new_last_node_id
        return new_subtree_root_id

    def add_tree_at_position(self, new_tree, father, position):
        if father not in self.fathers:
            raise Exception('Nodo id: ' + father + ' no existe')
        if len(self.sons[father]) < position:
            return self.add_tree_at_right(new_tree, father)
        elif position == 0:
            return self.add_tree_at_left(new_tree, father)
        else:
            [new_subtree_root_id, new_last_node_id] = new_tree.renumber_existent_nodes(self.last_node_id + 1)
            self.sons[father] = self.sons[father][0:position] + [new_subtree_root_id] + self.sons[father][position:]
            self.fathers.update(new_tree.fathers)
            self.fathers[new_subtree_root_id]=father
            self.sons.update(new_tree.sons)
            self.nodes.update(new_tree.nodes)
            self.last_node_id = new_last_node_id
        return new_subtree_root_id

    def add_node_as_father(self, new_node, son=None):
        if son is None:  # Va como root
            return self.add_node_as_root(new_node)
        if son == self.root:
            return self.add_node_as_root(new_node)
        if son not in self.fathers:
            raise Exception('Nodo id: ' + son + ' no existe')
        # el nodo sobre el que se quiere insertar es hijo (tiene padre)
        new_node_id = self._next_node_id()
        old_father = self.fathers[son]  # anterior padre (pasará a ser el padre del nodo nuevo)
        # print('son',son)
        # print('old_father', old_father)
        # print('self.sons',self.sons)
        # print('self.fathers',self.fathers)
        old_son_position = self.sons[old_father].index(son)  # posición que ocupaba entre sus hermanos
        # print('old_son_position',old_son_position)
        if old_son_position > 1:
            self.sons[old_father] = self.sons[old_father][:old_son_position - 1] + [new_node_id] + \
                                       self.sons[old_father][old_son_position + 1:] # insertamos nuevo en lista de hijos
        elif old_son_position == 1:
            self.sons[old_father] = self.sons[old_father][:1] + [new_node_id] + \
                                       self.sons[old_father][old_son_position + 1:] # insertamos nuevo en lista de hijos
        else:
            # print('XX')
            self.sons[old_father] = [new_node_id] + \
                                       self.sons[old_father][old_son_position + 1:] # insertamos nuevo en lista de hijos
        self.fathers[son] = new_node_id
        self.fathers[new_node_id] = old_father
        self.sons[new_node_id] = [son]
        self.nodes[new_node_id] = new_node
        # print('self.sons',self.sons)
        # print('self.fathers',self.fathers)
        return new_node_id

    def delete_subtree(self, node_id):
        """
        Borra el árbol completo que cuelga del nodo indicado
        """
        if node_id == self.root:
            self.nodes = dict()
            self.root = None
            self.sons = dict() # {1:[2,3], 2:[4,5]}
            self.fathers = dict() # {2:1, 3:1, 4:2, 5:2}
        elif node_id not in self.fathers:
            raise Exception("Nodo " + node_id + " no existe")
        elif self.sons[node_id] == []:
            self.delete_final_node(node_id)
        else:
            for s in self.sons[node_id]:
                # print('Bajando a nodo',s)
                self.delete_subtree(s)
            self.delete_final_node(node_id)
        return

    def delete_final_node(self, node_id):
        """
        Es un nodo final. Entrmos aquí con esa certeza
        """
        module_name = '[delete_final_node]'
        # print(module_name, node_id, ' => ', self.sons[node_id])
        self.sons[self.fathers[node_id]].remove(node_id)
        del self.fathers[node_id]
        del self.sons[node_id]
        del self.nodes[node_id]
        # print(module_name,' nodes_deleted')
        # print(module_name,' self.fathers', self.fathers)
        # print(module_name,' self.sons', self.sons)
        # print(module_name, 'self.nodes', self.nodes)

    def get_tree_links(self, node_id = None):
        # {0:[]}
        # {0:[{1:[]}]}
        # {0:[{1:[]},{2:[]}]}
        # {0:[{1:[{},{},{}]},{2:[]}]}
        if not node_id:
            node_id = self.root
        tree_links = dict()
        tree_links[node_id] = []
        for son_id in self.sons[node_id]:
            tree_links[node_id].append(self.get_tree_links(son_id))
        return tree_links




    def get_subtree(self, node_id):
        pass

    def get_final_subtrees(self):
        """
        Devuelve los últimos árboles (nodos con hijos) de la estructura
        """
        subtrees_list = dict()
        nodes_visited = list()
        for node_id in self.sons:
            if self.sons[node_id]:
                father_id = self.fathers[node_id]
                if father_id not in nodes_visited:
                    nodes_visited.append(father_id)
                    new_subtree = EXPTree()
                    new_subtree.root = father_id
                    new_subtree.last_node_id = max([father_id] + self.sons[father_id])
                    new_subtree.sons = dict()
                    new_subtree.sons[father_id] =0
                    subtrees_list.update(dict({self.fathers[node_id] : self.sons[self.fathers[node_id]]}))


    # Funciones de clase
    def build_tree(tree_structure, nodes):
        """
        Construye un árbol en base a la lista de nodos y los enlaces entre ellos
        {0:[{3:[]},{1:[{4:[]}]},{2:[]}]}
        """
        new_subtree = EXPTree()
        old_root_node_id = list(tree_structure.keys())[0]
        new_subtree.add_node_as_root(nodes[old_root_node_id])
        print(new_subtree.root)
        for subtree_estructure in tree_structure[old_root_node_id]:
            new_subtree.add_tree_at_right(EXPTree.build_tree(subtree_estructure,nodes), new_subtree.root)


