from symbol_table import *

class tree(object):
    def __init__(self,Data=None):
        self.father=None
        self.data=Data
        self.child=[]

    def list_child_name(self):
        child_list=[]
        for i in self.child:
            child_list.append(i.data)
        return child_list

    def is_leaf(self):
        if len(self.child)==0:
            return True
        else:
            return False

    def create_child(self,Data,Uniq=0):
        if Uniq==1:
            if Data in self.list_child_name():
                print("Error ,{0} appear more than one time".format(Data))
                return 0
        child_node=tree()
        child_node.father=self
        child_node.data=Data
        child_node.child=[]
        self.child.append(child_node)
        return child_node

    def next_node(self):
        if self.is_leaf()==False:
            return self.child[0]
        elif self.is_leaf()==True:
            while self.father.child[-1]==self:
                self=self.father
                if self.data=="root":
                    return 0
            return self.father.child[self.father.child.index(self)+1]


def syntax_analyzer(token_list,id_list):
    def get_next_token(shift=0):
        try:
            return token_list[current_token_index+shift]
        except:
            print("Error, No more token.")
            return 0
    id_type={}
    state=0
    error=0
    parse_tree=tree()
    parse_tree.data="root"
    current_token_index=0
    token_number=len(token_list)
    while current_token_index<token_number:
        token=token_list[current_token_index]
        if error!=0:
            return 0
        while state==0:
            token=get_next_token()
            if current_token_index==0 and token=="main":
                if get_next_token(1)=="(" and get_next_token(2)==")":
                    Program_Header=parse_tree.create_child(Data="Program_Header",Uniq=1)
                    current_token_index+=3
                    state=1
                    break
                else:
                    print("Error, expected ( and ) after main")
                    return 0
            else:
                print("Error , expected a main before any statment.")
                return 0

        while state==1:
            token=get_next_token()
            if token=="{":
                Program_Body=parse_tree.create_child(Data="Program_Body",Uniq=1)
                current_token_index+=1
                state=2
                break
            else:
                print("Error, expected { after main()")
                return 0
        while state==2:
            token=get_next_token()
            if token in TYPE_DECLARATION_WORD:
                try:
                    Data_Section in Program_Body.child
                except:
                    Data_Section=Program_Body.create_child(Data="Data_Section",Uniq=1)
                state=3
                break
            elif token=="}":
                return parse_tree
            else:
                print("Error, expected } after all statement.")
                return 0
        while state==3:
            token=token_list[current_token_index]
            if token=="const":
                state=4
                break 
            if token in ["bool","char","int","string"] or data_type in ["bool","char","int","string"]:
                if get_next_token(1) in id_list:
                    if get_next_token(1) in id_type:
                        print("Error redeclaration of {0}".format(get_next_token(1)))
                        return 0
                    elif get_next_token(2)==";":
                        if token in ["bool","char","int","string"]:
                            data_type=token
                        v_data=Data_Section.create_child(Data=data_type)
                        v_data.create_child(Data=get_next_token(1))
                        id_type[get_next_token(1)]=data_type
                        current_token_index+=3
                        state=2
                        data_type=None
                        break
                    elif get_next_token(2)=="," or data_type in ["bool","char","int","string"]:
                        if token in ["bool","char","int","string"]:
                            data_type=token
                        v_data=Data_Section.create_child(Data=data_type)
                        v_data.create_child(Data=get_next_token(1))
                        id_type[get_next_token(1)]=[data_type,v_data]
                        current_token_index+=2
                    else:
                        print("Error , expected ; or ,")
                        return 0
                else:
                    print("Error, expected an ID.")
                    return 0
        while state==4:
            token=token_list[current_token_index]
            if get_next_token(1) in id_list:
                if get_next_token(1) in id_type:
                    print("Error redeclaration of {0}".format(get_next_token(1)))
                    return 0
                if get_next_token(2)=="=":
                    if get_next_token(3) in id_list:
                        if get_next_token(3) in id_type:
                            v_data=id_type[get_next_token(3)][1]
                            if v_data.data!="string":
                                v_id_data=Data_Section.create_child(Data=v_data.data)
                                v_id_data.create_child(Data=get_next_token(1)).create_child(Data=v_data.next_node().next_node().data)
                                id_type[get_next_token(1)]=[v_data.data,v_id_data]
                            else:
                                v_data.next_node().data=[v_data.next_node().data,get_next_token(1)]
                                id_type[get_next_token(1)]=[v_data.data,v_data]
                        else:
                            print("Error , undeclared data.")
                    elif get_next_token(3).isdigit():
                        v_data=Data_Section.create_child(Data="int")
                        v_data.create_child(Data="v"+get_next_token(1)).create_child(Data=int(get_next_token(3)))
                        id_type["v"+get_next_token(1)]=["int",v_data]
                    elif get_next_token(3) in BOOL_WORD:
                        v_data=Data_Section.create_child(Data="bool")
                        v_data.create_child(Data=get_next_token(1)).create_child(Data=get_next_token(3))
                        id_type[get_next_token(1)]=["bool",v_data]
                    elif get_next_token(3).isprintable():
                        if get_next_token(3)[0]=="'":
                            v_data=Data_Section.create_child(Data="char")
                            v_data.create_child(Data=get_next_token(1)).create_child(Data=get_next_token(3))
                            id_type[get_next_token(1)]=["char",v_data]
                        else:
                            v_data=Data_Section.create_child(Data="string")
                            v_data.create_child(Data=get_next_token(1)).create_child(Data=get_next_token(3))
                            id_type[get_next_token(1)]=["string",v_data]
                    if get_next_token(4)==";":
                        current_token_index+=5
                        state=2
                        break
                    elif get_next_token(4)==",":
                        current_token_index+=4
                        continue
                    else:
                        print("Error, expected ; or ,")
                        return 0
                elif get_next_token(2)==";":
                    current_token_index+=3
                    state=2
                    break
                else:
                    print("Error, expected a =")
            elif get_next_token(1)==";":
                current_token_index+=2
                state=2
                break
            else:
                print("Error, expected an ID.")
                pass


