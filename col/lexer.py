from ply import lex

tokens = (
    'NUM',
    'IDF',
    'FUN',
    'END',
    'RET',
)

t_IDF = r"[a-zA-Z_]+"
t_FUN = r":fun"
t_END = r":end"
t_RET = r":ret"

t_ignore = " \t"

def t_NUM(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Error: Lexer: Illegal character {}".format(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()
