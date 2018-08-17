from col.lexer import tokens
from ply import yacc

def p_function_def(p):
    '''
    function_def : FUN IDF statement END
    '''
    p[0] = ("fundef", p[2], p[3])

def p_statement(p):
    '''
    statement : RET expression
    '''
    p[0] = ("ret", p[2])

def p_expression(p):
    '''
    expression : NUM
    '''
    p[0] = ("num", p[1])

def p_error(p):
    print("Error: Parser: Syntax error")

parser = yacc.yacc()
