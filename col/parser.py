from col.lexer import tokens
from ply import yacc

precedence = (
    ("left", "AND"),
    ("left", "LTH", "EQ2"),
    ("left", "ADD", "SUB"),
    ("left", "MUL", "DIV"),
    ("right", "NOT"),
)

def p_program(p):
    '''
    program : program function_def
            |
    '''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = list()

def p_function_def(p):
    '''
    function_def : FUN IDF statements END
    '''
    p[0] = ("fundef", p[2], p[3])

def p_statements(p):
    '''
    statements : statements statement
               |
    '''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = list()

def p_statement(p):
    '''
    statement : RET expression
              | IF expression statements END
              | WHL expression statements END
              | LCL EQU expression
              | ARG EQU expression
              | PUT expression
              | expression
    '''
    if p[1] == ":ret":
        p[0] = ("ret", p[2])
    elif p[1] == ":if":
        p[0] = ("if", p[2], p[3])
    elif p[1] == ":whl":
        p[0] = ("whl", p[2], p[3])
    elif p[1] == ":put":
        p[0] = ("put", p[2])
    elif p[1] > 0 :
        p[0] = ("asslcl", p[1] - 1, p[3])
    elif p[1] < 0:
        p[0] = ("assarg", -p[1] - 1, p[3])

def p_expression(p):
    '''
    expression : expression AND expression
               | expression LTH expression
               | expression EQ2 expression
               | expression ADD expression
               | expression SUB expression
               | expression MUL expression
               | expression DIV expression
    '''
    p[0] = ("binop", p[2], p[1], p[3])

def p_expression_not(p):
    '''
    expression : NOT expression
    '''
    p[0] = ("not", p[2])

def p_expression_group(p):
    '''
    expression : LPR expression RPR
    '''
    p[0] = p[2]

def p_expression_number(p):
    '''
    expression : NUM
    '''
    p[0] = ("num", p[1])

def p_expression_lcl(p):
    '''
    expression : LCL
    '''
    p[0] = ("lcl", p[1] - 1)

def p_expression_arg(p):
    '''
    expression : ARG
    '''
    p[0] = ("arg", -p[1] - 1)

def p_expression_fun_call(p):
    '''
    expression : IDF LPR params RPR
    '''
    p[0] = ("funcall", p[1], p[3])

def p_params(p):
    '''
    params : params COM expression
           | expression
           |
    '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = list()

def p_error(p):
    print("Error: Parser: Syntax error")

parser = yacc.yacc()
