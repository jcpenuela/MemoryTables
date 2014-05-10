__author__ = 'Juan Carlos'


class EXPNode(object):
    def __init__(self, text):
        self.text = text

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


