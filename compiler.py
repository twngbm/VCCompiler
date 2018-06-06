import time
RESERVED_WORD=["bool","char","const","string","int","if","else","while","read","main","FALSE","TRUE"]
SPECIAL_SYMBOL=["+","-","*","/","%","=","<","<=",">",">=","==","!=","(",")","{","}",",",";","\'","\""]
def scanner(current_line,line):
    token_state=-1       #-1=undetermind token,0=command token,1=RESERVED_WORD,2=ID token,3=SPECIAL_SYMBOL
    error=0
    EOL=0
    token_list=[]
    char_list=list(current_line)
    current_char_index=0
    total_char=len(char_list)
    while current_char_index<=total_char-1:
        if error!=0:
            line=-1
            break
        if EOL==1:
            line+=1
            break
        current_char=char_list[current_char_index]
        print(current_char,type(current_char))
        while token_state==-1:
            if current_char=="\n":
                EOL=1
                break
            elif current_char==" ":
                current_char_index+=1
                break
            elif current_char=="/":
                if char_list[current_char_index+1]=="/":
                    current_char_index+=1
                    comment_type=1
                    token_state=0
                    break
                elif char_list[current_char_index+1]=="*":
                    current_char_index+=1
                    comment_type=2
                    token_state=0
                    break
                else:
                    print("In",line,"lines,",current_char_index,"char","error: expected identifier or '('")
                    error=1
                    break
            else:
                current_char_index+=1
                break
        while token_state==0:
            if current_char=="\n":
                EOL=1
                break
            elif current_char=="*" and char_list[current_char_index+1]=="/" and comment_type==2:
                current_char_index+=1
                token_state=-1
                break
            else:
                current_char_index+=1
                break
            
                
    return token_list,line

time1=time.time()
print("This is a vanilla c compiler.\n")
#source_code_file=str(input("input file name:\n"))
source_code_file="main.vc"
with open(source_code_file) as f:
    source_code=f.readlines()
f.close()

current_line_number=0
total_line=len(source_code)
print(total_line)
while current_line_number <= total_line-1: using for i in list ; c=list.index()
    token,current_line_number=scanner(source_code[current_line_number],current_line_number)
    if current_line_number<0:
        print("Error")
        break
time2=time.time()
print("\nEnd Processing, waste",time2-time1,"\n")