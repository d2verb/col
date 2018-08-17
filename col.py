from col.lexer import lexer
from col.parser import parser
from col.codegen import codegen
from sys import argv

with open(argv[1], "r") as f:
    data = f.read()
    result = parser.parse(data, lexer=lexer)
    codegen(result)
