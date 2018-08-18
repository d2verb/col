from ply import lex

tokens = (
    "NUM",
    "IDF",
    "FUN",
    "END",
    "RET",
    "ADD",
    "SUB",
    "MUL",
    "DIV",
    "LTH",
    "AND",
    "NOT",
    "LPR",
    "RPR",
    "EQU",
    "EQ2",
    "LCL",
    "ARG",
    "IF",
    "WHL",
    "COM",
    "PUT",
)

t_IDF = r"[a-zA-Z_]+"
t_FUN = r":fun"
t_END = r":end"
t_RET = r":ret"
t_IF  = r":if"
t_WHL = r":whl"
t_PUT = r":put"
t_ADD = r"\+"
t_SUB = r"-"
t_MUL = r"\*"
t_DIV = r"/"
t_LPR = r"\("
t_RPR = r"\)"
t_EQU = r"="
t_EQ2 = r"=="
t_LTH = r"<"
t_AND = r":and"
t_NOT = r":not"
t_COM = r","

t_ignore = " \t"

def t_LCL(t):
    r"@[a-z]"
    t.value = ord(t.value[1]) - ord("a") + 1
    return t

def t_ARG(t):
    r"\#[a-z]"
    t.value = -(ord(t.value[1]) - ord("a") + 1)
    return t

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
