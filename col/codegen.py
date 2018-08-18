class CodeGenerator:
    def emit_expression(self, n):
        expr_type = n[0]
        if expr_type == "binop":
            self.emit_binop(n[1:])
        elif expr_type == "num":
            print("push {}".format(n[1]))
        elif expr_type == "lcl":
            lcl_no = n[1]
            print("mov rax, qword ptr [rbp - {}]".format(0x28 - lcl_no * 8))
            print("push rax")
        elif expr_type == "not":
            self.emit_expression(n[1])
            print("pop rax")
            print("cmp rax, 0")
            print("je 1f")
            print("push 0")
            print("jmp 2f")
            print("1:")
            print("push 1")
            print("2:")

    def emit_binop(self, n):
        op_type = n[0]
        lhs, rhs = n[1], n[2]

        self.emit_expression(lhs)
        self.emit_expression(rhs)

        print("pop rbx")
        print("pop rax")

        if op_type == "+":
            print("add rax, rbx")
            print("push rax")
        elif op_type == "-":
            print("sub rax, rbx")
            print("push rax")
        elif op_type == "*":
            print("mul rbx")
            print("push rax")
        elif op_type == "/":
            print("div rbx")
            print("push rax")
        elif op_type == "<":
            print("cmp rax, rbx")
            print("jl 1f")
            print("push 0")
            print("jmp 2f")
            print("1:")
            print("push 1")
            print("2:")
        elif op_type == ":and":
            print("cmp rax, 0")
            print("je 1f")
            print("cmp rbx, 0")
            print("je 1f")
            print("push 1")
            print("jmp 2f")
            print("1:")
            print("push 0")
            print("2:")

    def emit_ret(self, n):
        self.emit_expression(n)
        print("pop rax")
        print("jmp {}_epilogue".format(self.current_fun_name))

    def emit_asslcl(self, n):
        lcl_no = n[0]
        self.emit_expression(n[1])
        print("pop rax")
        print("mov qword ptr [rbp - {}], rax".format(0x28 - lcl_no * 8))

    def emit_statement(self, n):
        statement_type = n[0]
        if statement_type == "ret":
            self.emit_ret(n[1])
        elif statement_type == "asslcl":
            self.emit_asslcl(n[1:])
        elif statement_type == "if":
            self.current_if_no += 1
            self.emit_expression(n[1])
            print("pop rax")
            print("cmp rax, 0")
            print("je {}_else_{}".format(self.current_fun_name, self.current_if_no))
            for statement in n[2]:
                self.emit_statement(statement)
            print("{}_else_{}:".format(self.current_fun_name, self.current_if_no))
        elif statement_type == "whl":
            self.current_whl_no += 1
            print("{}_whl_{}_cond:".format(self.current_fun_name, self.current_whl_no))
            self.emit_expression(n[1])
            print("pop rax")
            print("cmp rax, 0")
            print("je {}_whi_{}_end".format(self.current_fun_name, self.current_whl_no))
            print("{}_whl_{}_body:".format(self.current_fun_name, self.current_whl_no))
            for statement in n[2]:
                self.emit_statement(statement)
            print("jmp {}_whl_{}_cond".format(self.current_fun_name, self.current_whl_no))
            print("{}_whi_{}_end:".format(self.current_fun_name, self.current_whl_no))

    def emit_fundef(self, n):
        self.current_fun_name = n[0]
        print("{}:".format(self.current_fun_name))
        self.emit_fun_prologue()
        for statement in n[1]:
            self.emit_statement(statement)
        print("{}_epilogue:".format(self.current_fun_name))
        self.emit_fun_epilogue()
        self.current_fun_name = ""

    def emit_prologue(self):
        print(".intel_syntax noprefix")
        print(".globl _main")
        print("_main = main")

    def emit_fun_prologue(self):
        print("push rbp")
        print("mov rbp, rsp")
        print("sub rsp, 0x28")

    def emit_fun_epilogue(self):
        print("mov rsp, rbp")
        print("pop rbp")
        print("ret")

    def gen(self, n):
        self.emit_prologue()
        node_type = n[0]
        self.emit_fundef(n[1:])

    def __init__(self):
        self.current_if_no = 0
        self.current_whl_no = 0
        self.current_fun_name = ""
