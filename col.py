from col.lexer import lexer
from col.parser import parser
from col.codegen import CodeGenerator
from sys import argv

with open(argv[1], "r") as f:
    data = f.read()
    result = parser.parse(data, lexer=lexer)
    codegen = CodeGenerator()
    codegen.gen(result)
