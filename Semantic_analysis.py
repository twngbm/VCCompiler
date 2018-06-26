from symbol_table import *
def semantic_analyzer(parse_tree):
    with open('test.asm','w') as f:
        current_node=parse_tree
        while current_node.next_node()!=0:
            current_node=current_node.next_node()
            if current_node.data=="Program_Header":
                for i in PROLOGUE:
                    f.write(i)
                continue
            elif current_node.data=="Program_Body":
                continue
            elif current_node.data=="Data_Section":
                continue
            elif current_node.data=="int":
                if len(current_node.next_node().child)==0:
                    EPILOGUE.append("  {0}\t\t\tDD\t 0\n".format(current_node.next_node().data))
                    current_node=current_node.next_node()
                else:
                    EPILOGUE.append("  {0}\t\t\tDD\t {1}\n".format(current_node.next_node().data,current_node.next_node().next_node().data))
                    current_node=current_node.next_node()
                    current_node=current_node.next_node()
            elif current_node.data=="bool":
                if len(current_node.next_node().child)==0:
                    EPILOGUE.append("  {0}\t\t\tDB\t 0\n".format(current_node.next_node().data))
                    current_node=current_node.next_node()
                else:
                    if current_node.next_node().next_node().data=="TRUE":
                        EPILOGUE.append("  {0}\t\t\tDB\t 1\n".format(current_node.next_node().data))
                    else:
                        EPILOGUE.append("  {0}\t\t\tDB\t 0\n".format(current_node.next_node().data))
                    current_node=current_node.next_node()
                    current_node=current_node.next_node()
            elif current_node.data=="char":
                if len(current_node.next_node().child)==0:
                    EPILOGUE.append("  {0}\t\tDB\t ' '\n".format(current_node.next_node().data))
                    current_node=current_node.next_node()
                else:
                    EPILOGUE.append("  {0}\t\tDB\t {1}\n".format(current_node.next_node().data,current_node.next_node().next_node().data))
                    current_node=current_node.next_node()
                    current_node=current_node.next_node()
            elif current_node.data=="string":
                if "  _S0000\tDB\t 0\n" not in EPILOGUE:
                    EPILOGUE.append("  _S0000\tDB\t 0\n")
                if len(current_node.next_node().child)==0:
                    EPILOGUE.append("  {0}\t\tDD\t _S0000\n".format(current_node.next_node().data))
                    current_node=current_node.next_node()
                else:
                    if type(current_node.next_node().data)!=list:
                        EPILOGUE.append("  _S{0}\tDB\t {1},0\n".format(str(current_node.next_node().next_node().meta_data).zfill(4),current_node.next_node().next_node().data))
                        EPILOGUE.append("  {0}\t\tDD\t _S{1}\n".format(current_node.next_node().data,str(current_node.next_node().next_node().meta_data).zfill(4)))
                    else:
                        EPILOGUE.append("  _S{0}\tDB\t {1},0\n".format(str(current_node.next_node().next_node().meta_data).zfill(4),current_node.next_node().next_node().data))
                        for i in current_node.next_node().data:
                            EPILOGUE.append("  {0}\t\tDD\t _S{1}\n".format(i,str(current_node.next_node().next_node().meta_data).zfill(4)))
                    current_node=current_node.next_node()
                    current_node=current_node.next_node()

        for line in EPILOGUE:
            f.write(line)

        f.write("END\tmain\t\n")
                
    f.closed