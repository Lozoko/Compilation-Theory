
import sys
import ply.yacc as yacc
from Mparser import Mparser
from TreePrinter import TreePrinter
from lab3 import scanner

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "lab3example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    # #Mparser = Mparser()
    # parser = yacc.yacc(module=Mparser)
    # text = file.read()
    # print(dir(parser))
    # ast = parser.parse(text, lexer=scanner.lexer)
    # #print(ast)
    # #ast.printTree()

    Mparser = Mparser()
    parser = yacc.yacc(module=Mparser)
    text = file.read()
    parser.parse(text, lexer=Mparser.scanner)