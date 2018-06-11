from symbol_table import *

class tree(object):
    def __init__(self):
        self.father=None
        self.data=None
        self.child_node=[]
        self.node_name=""
    def list_child(self):
        child_list=[]
        for i in self.child_node:
            child_list.append((i,i.node_name))
        return child_list
    def get_child(self,child_index):
        return self.child_node[child_index]
    def create_child(self,_data):
        child_tree=tree()
        child_tree.father=self
        child_tree.data=_data
        child_tree.node_name=str(_data)
        self.child_node.append(child_tree)

def syntax_analyzer(token_list,id_list):
    syntax_tree=tree
    return syntax_tree