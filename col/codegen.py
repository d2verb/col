def emit_fun_prologue():
    print("push rbp")
    print("mov rbp, rsp")
    print("sub rsp, 0x28")

def emit_fun_epilogue():
    print("mov rsp, rbp")
    print("pop rbp")
    print("ret")

# result is set to RAX
def emit_expression(n):
    expr_type = n[0]
    if expr_type == "binop":
        emit_binop(n[1:])
    elif expr_type == "num":
        print("push {}".format(n[1]))
    elif expr_type == "lcl":
        lcl_no = n[1]
        print("mov rax, qword ptr [rbp - {}]".format(0x28 - lcl_no))
        print("push rax")

def emit_binop(n):
    op_type = n[0]
    lhs, rhs = n[1], n[2]

    emit_expression(lhs)
    emit_expression(rhs)

    print("pop rbx\npop rax")

    if op_type == "+":
        print("add rax, rbx")
    elif op_type == "-":
        print("sub rax, rbx")
    elif op_type == "*":
        print("mul rbx")
    elif op_type == "/":
        print("div rbx")

    print("push rax")

def emit_ret(n, fun_name):
    emit_expression(n)
    print("pop rax")
    print("jmp {}_epilogue".format(fun_name))

def emit_asslcl(n):
    lcl_no = n[0]
    emit_expression(n[1])
    print("pop rax")
    print("mov qword ptr [rbp - {}], rax".format(0x28 - lcl_no))

def emit_statement(n, fun_name):
    statement_type = n[0]
    if statement_type == "ret":
        emit_ret(n[1], fun_name)
    elif statement_type == "asslcl":
        emit_asslcl(n[1:])

def emit_fundef(n):
    fun_name = n[0]
    print("{}:".format(fun_name))
    emit_fun_prologue()
    for statement in n[1]:
        emit_statement(statement, fun_name)
    print("{}_epilogue:".format(fun_name))
    emit_fun_epilogue()

def emit_prologue():
    print(".intel_syntax noprefix")
    print(".globl _main")
    print("_main = main")

def codegen(n):
    emit_prologue()
    node_type = n[0]
    emit_fundef(n[1:])
