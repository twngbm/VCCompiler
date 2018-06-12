import time
from Lexical_analysis import *
from Syntactic_analysis import *

error=0
time1=time.time()

print("This is a vanilla c compiler.\n")

#source_code_file=str(input("input file name:\n"))
source_code_file="main.vc"

with open(source_code_file) as f:
    source_code=f.readlines()
f.close()

print("source code:\n")
for i in source_code:
    print("{0}: ".format(source_code.index(i)+1),i,end='')
print("\n\nend of source code.\n")

token_list,id_list=scanner(source_code)

if type(token_list)!=list:
    print("Error,Lexical error")
    error=1
elif len(token_list)==0:
    print("Error, No token found")
    error=1

if error==0:
    print("\ntoken list\n")
    for i in token_list:
        print("\n",i,end=" ")
    print("\n\nend of token list\n")
    print("id list:",id_list,"\n")

    parse_tree=syntax_analyzer(token_list,id_list)

    if type(parse_tree)==int:
        print("Error, Syntax error")
    else:
        with open('test.asm','w') as f:
            if "Program_Header" in parse_tree.list_child_name():
                for i in PROLOGUE:
                    f.write(i)
            if "Program_Body" in parse_tree.list_child_name():
                for i in EPILOGUE:
                    f.write(i)
                if "DCL_LIST" in parse_tree.get_child(1).list_child_name():
                    if "int" in parse_tree.get_child(1).get_child(1).list_child_name():
                        for i in parse_tree.get_child(1).get_child(1).get_child(0).list_child_name():
                            if parse_tree.get_child(1).get_child(1).get_child_by_name("int").get_child_by_name(i).list_child_name!=[]:
                                f.write("  v{0}  DD  {1}\n".format(i,parse_tree.get_child(1).get_child(1).get_child_by_name("int").get_child_by_name(i).get_child_by_name("data").data))
                            else:
                                f.write("  v{0}  DD  0\n".format(i))
                    if "bool" in parse_tree.get_child(1).get_child(1).list_child_name():
                        for i in parse_tree.get_child(1).get_child(1).get_child(0).list_child_name():
                            f.write("  {0}  DB 0\n".format(i))
                    if "char" in parse_tree.get_child(1).get_child(1).list_child_name():
                        for i in parse_tree.get_child(1).get_child(1).get_child(0).list_child_name():
                            f.write("  {0}  DB ''\n".format(i))
                    if "string" in parse_tree.get_child(1).get_child(1).list_child_name():
                        f.write("  _S0000  DB  0\n")
                        for i in parse_tree.get_child(1).get_child(1).get_child(0).list_child_name():
                            f.write("  {0}  DB _S0000\n".format(i))
                f.write("  	END	main    \n")
                
        f.closed

time2=time.time()
print("\nEnd Processing, waste",time2-time1,"\n")