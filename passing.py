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
    
    token_state=-1       #-1=undetermind token,0=command token,1=RESERVED_WORD,ID token,SPECIAL_SYMBOL
    error=0
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
        current_line=[w.replace("\t"," ") for w in current_line]
        current_char_index=0
        #print("char_split: ",current_line)

        #handing error
        if error!=0:
            return -1,0
        #handing error end

        while current_char_index<len(current_line):
            
            char=current_line[current_char_index]
            
            #handling error
            if error!=0:
                return -1,0
            #handling error end

            #handling un-stated token
            if token_state==-1:

                if char=="\\":
                    error=1
                    print("Stray \\ in program")
                    break
                #handling EOL
                if char=="\n":
                    break
                #handling EOL end
               
                #handling comment
                if char=="/": 
                    if get_next_char()=="/":#"//"type of comment
                        current_char_index+=2
                        comment_type=1
                        token_state=0
                        continue
                    elif get_next_char()=="*":#"/*...*/"type of comment
                        current_char_index+=2
                        comment_type=2
                        token_state=0
                        continue
                #handling comment end

                #handing normal token
                if char in ALL_CHAR or char=="!":#handling != but ! not in SPECIAL_SYMBOL
                    token_state=1
                    current_state=0
                    continue
                #handing normal token end 

                #tempory handling none handling char    
                else: 
                    current_char_index+=1
                    continue
            #handling un-stated token end

            #handling comment      
            if token_state==0: 
                if comment_type==1:#"//"type of comment
                    if char!="\n":
                        current_char_index+=1
                    else:
                        current_char_index+=1
                        token_state=-1
                        
                elif comment_type==2:#"/*...*/"type of comment
                    if char=="\n":
                        break
                    elif char=="*" and get_next_char()=="/":
                        current_char_index+=2
                        token_state=-1
                    else:
                        current_char_index+=1             
            #handling comment end

            #handing normal token
            if token_state==1:

                #handling char or string not a token yet
                if current_state==0:
                    current_str+=char
                    #print(current_str)
                    if get_next_char() in SPECIAL_SYMBOL or get_next_char()==" " or get_next_char()=="\n":
                        if current_str not in RESERVED_WORD and current_str not in SPECIAL_SYMBOL and current_str not in DIGITS:
                            current_state=1
                            continue
                    if current_str in RESERVED_WORD:
                            current_state=2
                            continue
                    elif current_str in SPECIAL_SYMBOL:
                        if current_str in OPERATOR_SYMBOL:
                            current_state=5
                            continue
                        elif current_str in ASSIGNMENT_SYMBOL:
                            current_state=6
                            continue
                        elif current_str in COMPARE_SYMBOL or current_str=="!":
                            current_state=7
                            continue
                        elif current_str in STRUCTURE_SYMBOL:
                            current_state=8
                            continue
                    elif current_str in DIGITS:
                        current_state=9
                        continue
                    else:
                       current_char_index+=1
                #handling char or string not a token yet end

                #handling ID
                elif current_state==1:
                    token_list.append(current_str)
                    if current_str not in ID:
                        ID.append(current_str)
                    current_str=""
                    token_state=-1
                    current_char_index+=1
                    continue
                #handling ID end

                #habdling RESERVED_WORD
                elif current_state==2:
                    if get_next_char()==" " or get_next_char()=="\n" or get_next_char() in SPECIAL_SYMBOL:
                        token_list.append(current_str)
                        current_str=""
                        current_char_index+=1
                        token_state=-1
                        continue
                    elif get_next_char() in LETTER or get_next_char() in DIGITS:
                        current_state=0
                        current_char_index+=1
                        continue

                #habdling RESERVED_WORD end
                
                #handling "+","-","*","/","%"
                elif current_state==5:
                    token_list.append(current_str)
                    current_str=""
                    current_char_index+=1
                    token_state=-1
                    continue
                #handling "+","-","*","/","%" end

                #handling = and ==
                elif current_state==6:
                    if get_next_char()!="=":
                        current_char_index+=1
                        token_list.append(current_str)
                        current_str=""
                        token_state=-1
                        continue
                    else:
                        current_char_index+=2
                        token_list.append("==")
                        current_str=""
                        token_state=-1
                        continue
                #handling = and == end
                
                #handling "<","<=",">",">=","==","!="
                elif current_state==7:
                    if current_str=="!":
                        if get_next_char()=="=":
                            token_list.append("!=")
                            current_str=""
                            token_state=-1
                            current_char_index+=2
                            continue
                        else:
                            print("Get ! without =.")
                            error=1
                            break
                    else:
                        if get_next_char()=="=":
                            current_str+="="
                            token_list.append(current_str)
                            current_str=""
                            current_char_index+=2
                            token_state=-1
                            continue
                        else:
                            token_list.append(current_str)
                            current_str=""
                            current_char_index+=1
                            token_state=-1
                            continue
                #handling "<","<=",">",">=","==","!=" end

                #habdling "(",")","{","}",",",";" symbol and string token
                elif current_state==8:
                    if current_str!="'" and current_str!='"':
                        token_list.append(current_str)
                        current_str=""
                        current_char_index+=1
                        token_state=-1
                        continue
                    elif current_str=="'":
                        current_state=80
                        current_char_index+=1
                        continue
                    elif current_str=='"':
                        current_state=81
                        current_char_index+=1
                        continue
                elif current_state==80:
                    current_str+=char
                    if char=="\n":
                        print("Error, string end without an ' ")
                        return 0,0
                    elif char=='\\':
                        current_str+=get_next_char()
                        current_char_index+=2
                        continue
                    elif char!="'":
                        current_char_index+=1
                        continue
                    else:
                        token_list.append(current_str)
                        current_str=""
                        current_char_index+=1
                        token_state=-1
                        continue
                elif current_state==81:
                    current_str+=char
                    if char=="\n":
                        print("Error, string end without an \" ")
                        return 0,0
                    elif char=='\\':
                        current_str+=get_next_char()
                        current_char_index+=2
                        continue
                    elif char!='"':
                        current_char_index+=1
                        continue
                    else:
                        token_list.append(current_str)
                        current_str=""
                        current_char_index+=1
                        token_state=-1
                        continue
                #habdling "(",")","{","}",",",";" symbol and string token end

                #handling DIGITS
                elif current_state==9:
                    if get_next_char() in DIGITS:
                        current_str+=get_next_char()
                        current_char_index+=1
                        continue
                    else:
                        token_list.append(current_str)
                        current_str=""
                        current_char_index+=1
                        token_state=-1
                        continue
                #handing DIGITS end

            #handing normal token end 
    if error!=0:
        return -1,0

    return token_list,ID


def syntax_analyzer(token_list):
    syntax_tree=Tree
    return syntax_tree