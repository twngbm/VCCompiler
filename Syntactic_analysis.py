from symbol_table import *

class tree(object):
    def __init__(self,_data=None,name=None):
        self.father=None
        self.data=_data
        self.child_node=[]
        self.node_name=name
    def list_child(self):
        child_list=[]
        for i in self.child_node:
            child_list.append((i,i.node_name))
        return child_list
    def list_child_name(self):
        child_list=[]
        for i in self.child_node:
            child_list.append(i.node_name)
        return child_list
    def get_child(self,child_index):
        return self.child_node[child_index]
    def create_child(self,_data=None,name=None,only=0):
        if only==1:
            for i in self.child_node:
                child_list.append(i.node_name)
            if name in child_list:
                print("Error, multi element found,but can only have one.")
                return -1
        child_tree=tree()
        child_tree.father=self
        child_tree.data=_data
        child_tree.node_name=str(name)
        self.child_node.append(child_tree)
        return 0
    def create_leaf(self,_data,name,only=0):
        if only==1:
            for i in self.child_node:
                child_list.append(i.node_name)
            if name in child_list:
                print("Error, multi element found,but can only have one.")
                return -1
        child_tree=leaf()
        child_tree.father=self
        child_tree.data=_data
        child_tree.node_name=str(name)
        self.child_node.append(child_tree)
        return 0
    def add_child(self,child_name,only=0):
        if only==1:
            child_list=[]
            for i in self.child_node:
                child_list.append(i.node_name)
            if child_name in child_list:
                print("Error, multi element found,but can only have one.")
                return -1
        self.child_node.append(child_name)
        return 0

class leaf():
    def __init__(self,_father=None,_data=None,name=""):
        self.father=_father
        self.data=_data
        self.node_name=name


def syntax_analyzer(token_list,id_list):
    error=0
    parse_tree=tree()
    parse_tree.node_name="Program"


    def link(father,son,only=0):
        error=father.add_child(son,only)
        if error==0:
            son.father=father
            return 0
        return -1
    def get_next_token(shift):
        try:
            return token_list[current_token_index+shift]
        except:
            print("Error, No more token.")

    current_token_index=0
    token_number=len(token_list)
    token_stack=[]
    while current_token_index<token_number:
        token=token_list[current_token_index]
        if error!=0:
            return 0
        token_stack.append(token)
        if token in RESERVED_WORD:
            if token == "main":
                if get_next_token(1)=="(" and get_next_token(2)==")":
                        Program_Header=tree(None,"Program_Header")
                        Program_Header.create_leaf(token,"main")
                        Program_Header.create_leaf("()","()")
                        error=link(parse_tree,Program_Header,1)
                        current_token_index+=3
                else:
                    print("Error, Except ( or ) after main.")
                    return 0
            else:
                pass
        elif token in id_list:
            pass
        elif token=="{" and get_next_token(1)=="}":
            Program_Body=tree(name="Program_Body")
            Program_Body.create_leaf(token,"{")
            Program_Body.create_leaf("}","}")
            error=link(parse_tree,Program_Body,1)
            current_token_index+=2
        elif token=="{" and get_next_token(1) in TYPE_DECLARATION_WORD:
            Program_Body=tree(name="Program_Body")
            Program_Body.create_leaf(token,"{")
            Program_Body.create_child(name="DCL_LIST")
            DCL_LIST=Program_Body.get_child(1)
            while True:
                current_token_index+=1
                token=token_list[current_token_index]
                multi_defin=0
                if token=="}":
                    Program_Body.create_leaf("}","}")
                    error=link(parse_tree,Program_Body,1)
                    break
                elif token=="int" or multi_defin==1:
                    if "int" not in Program_Body.get_child(1).list_child_name():
                        DCL_LIST.create_child(name="int")
                        INT=DCL_LIST.get_child(0)
                    if get_next_token(1) not in id_list:
                        print("Error, Excpet an ID")
                        return 0
                    else:
                        INT.create_leaf(_data=get_next_token(1),name=get_next_token(1))
                        if get_next_token(2)==";":
                            current_token_index+=2
                            continue
                        elif get_next_token(2)==",":
                            multi_defin=1
                            continue
                        else:
                            print("Error, Except , or ; after define.")
                            return 0
                        
            
        else:
            print("Error, Except { or } after main()")

        if "Program_Header" not in parse_tree.list_child_name():
            print("Error, Start without main")
            return 0
        
        if "Program_Header" in parse_tree.list_child_name() and "Program_Body" in parse_tree.list_child_name():
            return parse_tree
    return parse_tree




##########################################################################
"""
        if token in RESERVED_WORD:
            if token == "main":
                if get_next_token(1)=="(" and get_next_token(2)==")":
                     Program_Header=tree(None,"Program_Header")
                     Program_Header.create_leaf(token,"main")
                     Program_Header.create_leaf("()","()")
                     error=link(parse_tree,Program_Header,1)
                     current_token_index+=3
                else:
                    print("Error, Except ( or ) after main.")
                    return 0
            else:
                pass
        elif token in STRUCTURE_SYMBOL:
            pass
        if "Program_Header" not in parse_tree.list_child_name():
            print("Error, Start without main")
            return 0
        else:
            pass
"""


    