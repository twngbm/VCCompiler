from symbol_table import *
ID=[]

class Tree(object):
    def __init__(self):
        self.left=None
        self.right=None
        self.data=None

def scanner(source_code):
    
    token_state=-1       #-1=undetermind token,0=command token,1=RESERVED_WORD,ID token,SPECIAL_SYMBOL
    error=0
    token_list=[]
    current_str=""

    for current_line_ in source_code:
        
        current_line=list(current_line_)
        current_char_index=0
        print("char_split: ",current_line)
        #handing error
        if error!=0:
            break
        #handing error end

        while current_char_index<len(current_line):
            
            char=current_line[current_char_index]
            
            #handling error
            if error!=0:
                token_list=-1
                break
            #handling error end

            #handling un-stated token
            if token_state==-1:

                #handling EOL
                if char=="\n":
                    break
                #handling EOL end
               
                #handling comment
                if char=="/": 
                    if current_line[current_char_index+1]=="/":#"//"type of comment
                        current_char_index+=2
                        comment_type=1
                        token_state=0
                        continue
                    elif current_line[current_char_index+1]=="*":#"/*...*/"type of comment
                        current_char_index+=2
                        comment_type=2
                        token_state=0
                        continue
                #handling comment end

                #handing normal token
                if char in ALL_CHAR:
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
                    elif char=="*" and current_line[current_char_index+1]=="/":
                        current_char_index+=2
                        token_state=-1
                    else:
                        current_char_index+=1             
            #handling comment end

            #handing normal token
            if token_state==1:
                if current_state==0:
                    current_str+=char
                    #print(current_str)
                    if current_str in ID:
                        current_state=1
                        continue
                    elif current_str in RESERVED_WORD:

                        #habdling "bool","char","const","string","int"
                        if current_str in TYPE_DECLARATION_WORD:
                            current_state=2
                            continue
                        #habdling "bool","char","const","string","int" end

                        #handling "if","else","while","main","read"
                        elif current_str in STRUCTURE_WORD:
                            current_state=3
                            continue
                        #handling "if","else","while","main","read" end

                        elif current_str in BOOL_WORD:
                            current_state=4
                            continue
                    elif current_str in SPECIAL_SYMBOL:
                        if current_str in OPERATOR_SYMBOL:
                            current_state=5
                            continue
                        elif current_str in ASSIGNMENT_SYMBOL:
                            current_state=6
                            continue
                        elif current_str in COMPARE_SYMBOL:
                            current_state=7
                            continue

                        #habdling "(",")","{","}",",",";" symbol and string token
                        elif current_str in STRUCTURE_SYMBOL:
                            current_state=8
                            continue
                        #habdling "(",")","{","}",",",";" symbol and string token end

                    else:
                       current_char_index+=1
                elif current_state==1:
                    pass

                #habdling "bool","char","const","string","int"
                elif current_state==2:
                    pass
                #habdling "bool","char","const","string","int" end

                #handling "if","else","while","main","read"
                elif current_state==3:
                    if current_line[current_char_index+1]=="(":
                        token_list.append(current_str)
                        current_str=""
                        token_list.append("(")
                        current_char_index+=2
                        token_state=-1
                        continue
                    elif current_line[current_char_index+1] in LETTER or current_line[current_char_index+1] in DIGITS:
                        current_state=0
                        current_char_index+=1
                        continue
                    elif current_line[current_char_index+1] in SPECIAL_SYMBOL and current_line[current_char_index+1]!="(":
                        token_list.append(current_str)
                        current_str=""
                        current_char_index+=1
                        token_state=-1
                        continue
                    elif current_line[current_char_index+1]==" " or current_line[current_char_index+1]=="\n":
                        token_list.append(current_str)
                        current_str=""
                        current_char_index+=1
                        token_state=-1
                        continue
                #handling "if","else","while","main","read" end
                    
                elif current_state==4:
                    pass
                elif current_state==5:
                    pass
                elif current_state==5:
                    pass
                elif current_state==6:
                    pass
                elif current_state==7:
                    pass

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
                    if char=='\\':
                        pass
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
                    if char!='"':
                        current_char_index+=1
                    else:
                        token_list.append(current_str)
                        current_str=""
                        current_char_index+=1
                        token_state=-1
                        continue
                #habdling "(",")","{","}",",",";" symbol and string token end
            #handing normal token end 

    return token_list

def syntax_analyzer(token_list):
    syntax_tree=Tree
    return syntax_tree