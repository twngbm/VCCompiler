import string
TYPE_DECLARATION_WORD=["bool","char","const","string","int"]
STRUCTURE_WORD=["if","else","while","main","read"]
BOOL_WORD=["FALSE","TRUE"]
RESERVED_WORD=TYPE_DECLARATION_WORD+STRUCTURE_WORD+BOOL_WORD
OPERATOR_SYMBOL=["+","-","*","/","%"]
ASSIGNMENT_SYMBOL=["="]
COMPARE_SYMBOL=["<","<=",">",">=","==","!="]
STRUCTURE_SYMBOL=["(",")","{","}",",",";","\'","\""]
SPECIAL_SYMBOL=OPERATOR_SYMBOL+ASSIGNMENT_SYMBOL+COMPARE_SYMBOL+STRUCTURE_SYMBOL
LETTER=list(string.ascii_letters)#A~Z,a~z
DIGITS=list(string.digits)#0~9
ALL_CHAR=SPECIAL_SYMBOL+LETTER+DIGITS

PROLOGUE=[
";-----------------------------------------------------------------------\n",
";        1         2         3         4         5         6         7\n",
";23456789012345678901234567890123456789012345678901234567890123456789012\n",
";-----------------------------------------------------------------------\n",
";\n"
"INCLUDE    Irvine32.inc\n",
"INCLUDELIB Irvine32.lib\n",
"INCLUDELIB Kernel32.lib\n",
"INCLUDELIB User32.lib\n",
";\n",
".STACK    4096\n",
".CODE\n"
]

EPILOGUE=[
"   pExit:\n",
"        call     CRLF\n",
"        call     ReadKey                ; Wait for a key before\n",
"                                        ; stopping program execution \n",
"        exit                            ; invoke   ExitProcess, 0\n",
"   main	ENDP\n",
".DATA\n",
"  _SID	DB	 \"x86 MASM Program.\"\n",
";-----------------------------------------------------------------------\n",
";23456789012345678901234567890123456789012345678901234567890123456789012\n",
";        1         2         3         4         5         6         7\n",
";-----------------------------------------------------------------------\n",
"  	END	main    \n"
]
