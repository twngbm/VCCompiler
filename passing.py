from symbol_table import *


class Tree(object):
    def __init__(self):
        self.left=None
        self.right=None
        self.data=None

def scanner(source_code):
    ID=[]
    def get_next_char():
        return current_line[current_char_index+1]

    current_state=-1
    token_list=[]
    current_str=""
    source_code_len=len(source_code)
    if source_code_len==0:
        print("Error,Empty source code")
        return 0,0
    current_line_index=0
    for current_line_ in source_code:
        current_line_index+=1
        if current_line_index>=source_code_len:
            current_line_+="\n"
        
        current_line=list(current_line_)
        current_char_index=0
        while current_char_index<len(current_line):
            char=current_line[current_char_index]
            if current_state==-1:#handling un-stated token
                current_str=""
                if char=="\\":#handling \ not in string
                    print("Stray \\ in program")
                    return -1,0
                elif char==" " or char=="\t":#handling white space
                    current_char_index+=1
                elif char=="\n":#handling EOL
                    break
                #handing normal token
                elif char in ALL_CHAR or char=="!":#handling != but ! not in SPECIAL_SYMBOL
                    current_state=0
  
            elif current_state==0:#handling char or string not a token yet
                current_str+=char
                if current_str in RESERVED_WORD:
                    current_state=2
                elif current_str in SPECIAL_SYMBOL:
                    current_state=3
                elif current_str in DIGITS:
                    current_state=4
                elif get_next_char() in SPECIAL_SYMBOL or get_next_char()==" " or get_next_char()=="\n":
                    current_state=1
                else:
                    current_char_index+=1

            elif current_state==1: #handling ID
                if current_str not in ID:
                    ID.append(current_str)
                token_list.append(current_str)
                current_state=-1
                current_char_index+=1

            elif current_state==2:#habdling RESERVED_WORD
                if get_next_char()==" " or get_next_char()=="\n" or get_next_char() in SPECIAL_SYMBOL:
                    token_list.append(current_str)
                    current_state=-1
                elif get_next_char() in LETTER or get_next_char() in DIGITS:
                    current_state=0
                current_char_index+=1
            
            elif current_state==3:#habdling SPECIAL_SYMBOL and string and comment
                if current_str!="'" and current_str!='"':
                    if current_str=="!" and get_next_char()!="=":
                        print("Get ! without =.")
                        return -1,0    
                    elif current_str in ["<",">","=","!"] and get_next_char()=="=":#handling <= >= == !=
                        current_str+="="
                        token_list.append(current_str)
                        current_char_index+=1
                        current_state=-1
                    elif current_str=="/" and (get_next_char()=="/" or get_next_char()=="*"):#handling commemt
                        if get_next_char()=="/":#"//"type of comment
                            current_char_index+=1
                            current_state=32
                            continue
                        elif get_next_char()=="*":#"/*...*/"type of comment
                            current_char_index+=1
                            current_state=33
                            continue
                    else:
                        token_list.append(current_str)
                        current_state=-1
                        
                elif current_str=="'":
                    current_state=30
                    
                elif current_str=='"':
                    current_state=31
                current_char_index+=1
                    
            elif current_state==30:#handling string start with '
                current_str+=char
                if char=="\n":
                    print("Error, string end without an ' ")
                    return 0,0
                elif char=='\\':
                    current_str+=get_next_char()
                    current_char_index+=1 
                elif char=="'":
                    token_list.append(current_str)
                    current_state=-1
                current_char_index+=1
                    
            elif current_state==31:#handling string start with "
                current_str+=char
                if char=="\n":
                    print("Error, string end without an \" ")
                    return 0,0
                elif char=='\\':
                    current_str+=get_next_char()
                    current_char_index+=1
                elif char=='"':
                    token_list.append(current_str)
                    current_state=-1   
                current_char_index+=1

            elif current_state==32:#"//"type of comment
                if char=="\n":
                    current_state=-1
                current_char_index+=1
                    
                    
            elif current_state==33:#"/*...*/"type of comment
                if char=="\n":
                    break
                elif char=="*" and get_next_char()=="/":
                    current_char_index+=1
                    current_state=-1
                current_char_index+=1
                    
            elif current_state==4:#handling DIGITS
                if get_next_char() in DIGITS:
                    current_str+=get_next_char()
                else:
                    token_list.append(current_str)
                    current_state=-1
                current_char_index+=1  


        #handing normal token end 


    return token_list,ID


def syntax_analyzer(token_list):
    syntax_tree=Tree
    return syntax_tree