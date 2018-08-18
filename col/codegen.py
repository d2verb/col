def emit_fun_prologue():
    output = (
        "push rbp",
        "mov rbp, rsp",
        "sub rsp, 0x68"
    )
    print("\n".join(output))

def emit_fun_epilogue():
    output = (
        "add rsp, 0x68",
        "pop rbp",
        "ret"
    )
    print("\n".join(output))

def emit_binop(n):
    op_type = n[0]
    lhs, rhs = n[1], n[2]

    if lhs[0] == "num":
        print("push {}".format(lhs[1]))
    elif lhs[0] == "binop":
        emit_binop(lhs[1:])

    if rhs[0] == "num":
        print("push {}".format(rhs[1]))
    elif rhs[0] == "binop":
        emit_binop(rhs[1:])

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
    expression_type = n[0]
    if expression_type == "num":
        output = (
            "mov rax, {}".format(n[1]),
            "jmp {}_epilogue".format(fun_name)
        )
        print("\n".join(output))
    elif expression_type == "binop":
        emit_binop(n[1:])
        output = (
            "pop rax",
            "jmp {}_epilogue".format(fun_name)
        )
        print("\n".join(output))

def emit_statement(n, fun_name):
    statement_type = n[0]
    if statement_type == "ret":
        emit_ret(n[1], fun_name)

def emit_fundef(n):
    fun_name = n[0]
    print("{}:".format(fun_name))
    emit_fun_prologue()
    emit_statement(n[1], fun_name)
    print("{}_epilogue:".format(fun_name))
    emit_fun_epilogue()

def emit_prologue():
    output = (
        ".intel_syntax noprefix",
        ".globl _main",
        "_main = main"
    )
    print("\n".join(output))

def codegen(n):
    emit_prologue()
    node_type = n[0]
    emit_fundef(n[1:])
