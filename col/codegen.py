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

def emit_ret(n):
    expression_type = n[0]
    if expression_type == "num":
        print("mov rax, {}".format(n[1]))

def emit_statement(n):
    statement_type = n[0]
    if statement_type == "ret":
        emit_ret(n[1])

def emit_fundef(n):
    fun_name = n[0]
    print("{}:".format(fun_name))
    emit_fun_prologue()
    emit_statement(n[1])
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
