from symbol_table import *

def scanner(source_code):
    ID=[]
    def get_next_char():
        return current_line[current_char_index+1]
    comment_state=0
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
            current_str+=char
            if char=="\\":#handling \ not in string
                print("Stray \\ in program")
                return -1,0
            elif char==" " or char=="\t" :#handling white space
                current_char_index+=1
                current_str=""
            elif char=="\n":#handling EOL
                current_str=""
                break
            #handing normal token
            elif char in ALL_CHAR or comment_state==1:#handling != but ! not in SPECIAL_SYMBOL
                if current_str in RESERVED_WORD:
                    if get_next_char()==" " or get_next_char()=="\n" or get_next_char()=="\t" or get_next_char() in SPECIAL_SYMBOL:
                        token_list.append(current_str)
                        current_str=""
                    current_char_index+=1
                elif current_str in SPECIAL_SYMBOL or comment_state==1:
                    if current_str!="'" and current_str!='"':
                        if current_str=="!" and get_next_char()!="=":
                            print("Get ! without =.")
                            return -1,0    
                        elif current_str in ["<",">","=","!"] and get_next_char()=="=":#handling <= >= == !=
                            current_str+="="
                            token_list.append(current_str)
                            current_char_index+=2
                            current_str=""
                        elif current_str=="/" and get_next_char()=="/":#"//"type of comment
                            current_str=""
                            current_char_index+=2
                            while current_line[current_char_index]!="\n":
                                current_char_index+=1
                        elif (current_str=="/" and get_next_char()=="*") or comment_state==1:#"/*...*/"type of comment
                            if comment_state!=1:
                                current_char_index+=2
                                comment_state=1
                            while (current_line[current_char_index]!="*" or get_next_char()!="/") and current_line[current_char_index]!="\n":
                                current_char_index+=1
                            if current_line[current_char_index]=="*" and get_next_char()=="/":
                                current_str=""
                                comment_state=0
                                current_char_index+=2
                        else:
                            token_list.append(current_str)
                            current_str=""
                            current_char_index+=1
                    elif current_str=="'" or current_str=='"':
                        start_symbol=current_str
                        current_char_index+=1
                        while current_line[current_char_index]!=start_symbol:
                            current_str+=current_line[current_char_index]
                            if current_line[current_char_index]=="\n":
                                print("Error, string end without an ' ")
                                return 0,0
                            elif current_line[current_char_index]=='\\':
                                current_str+=get_next_char()
                                current_char_index+=1 
                            current_char_index+=1
                        current_str+=current_line[current_char_index]
                        current_char_index+=1
                        token_list.append(current_str)
                        current_str=""    
                elif current_str in DIGITS:
                    while get_next_char() in DIGITS:
                        current_str+=get_next_char()
                        current_char_index+=1
                    token_list.append(current_str)
                    current_char_index+=1
                    current_str=""
                elif get_next_char() in SPECIAL_SYMBOL or get_next_char()==" " or get_next_char()=="\n":
                    if current_str not in ID:
                        ID.append(current_str)
                    token_list.append("_"+current_str)
                    current_char_index+=1
                    current_str=""
                else:
                    current_char_index+=1
        #handing normal token end 

    new_ID=[]
    for item in ID:
        new_ID.append("_"+item)
    return token_list,new_ID


