import time
from passing import *


time1=time.time()

print("This is a vanilla c compiler.\n")

#source_code_file=str(input("input file name:\n"))
source_code_file="main.vc"

with open(source_code_file) as f:
    source_code=f.readlines()
f.close()

print("source code:\n")
for i in source_code:
    print("{0}:   ".format(source_code.index(i)+1),i,end='')


token_list=scanner(source_code)

if type(token_list)!=list:
    print("error")
    exit()

print("\n",token_list)

syntax_tree=syntax_analyzer(token_list)
if syntax_tree!=Tree:
    print("error")
    exit()

with open('test.asm','w') as f:
    for i in PROLOGUE:
        f.write(i)

    f.write("   main	PROC\n")

    for i in EPILOGUE:
        f.write(i)
f.closed

time2=time.time()
print("\nEnd Processing, waste",time2-time1,"\n")
