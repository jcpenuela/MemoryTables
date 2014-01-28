'''
Created on 27/01/2014

@author: jcpenuela
'''

class NodesLinks(object):
    '''
    Enlace entre nodos
    '''

    DIRECTIONAL = 1
    BIDIRECTIONAL = 2

    def __init__(self, source_id, target_id):
        '''
        Constructor
        '''
        self.source_id = source_id
        self.target_id = target_id
        self.attributes = dict()
        
    def set_attribute(self, attribute, data):
        self[attribute] = data
        
    def get_attribute(self, attribute):
        if attribute in self.attributes:
            return self.attributes[attribute]
        else:
            return None
        