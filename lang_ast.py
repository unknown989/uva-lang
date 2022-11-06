from typing import Optional

from lang_types import BinaryOperations, Types


class ASTNode:
    pass


class VariableNode:
    pass


class Scope:
    pass


class OutVariableNode:
    pass


class FunctionNode:
    pass


class FunctionArgNode:
    pass


class LiteralNode:
    pass


class ReturnNode:
    pass


class BinaryOpNode:
    pass


class CallExpressionNode:
    pass


class ASTNode():
    def __init__(self, name: str, child):
        self.name: str = name
        if child is not None:
            self.child = child  # Should be an ASTNode type

    def get_name(self) -> str:
        return self.name

    def get_child(self):
        return self.child

    def traverse_and_print(self, indent: int):
        return f"{' '*indent}[ {self.name} ]"

    def run(self, local_scope):
        return self.child.run() if self.child is not None else None


class VariableNode(ASTNode):
    def __init__(self, variable_type: Types, variable_name: str, variable_value: ASTNode):
        super().__init__("VariableNode", None)
        self.variable_type: Types = variable_type
        self.variable_name: str = variable_name
        self.variable_value: ASTNode = variable_value

    def traverse_and_print(self, indent: int):
        return f"{' '*indent}[ {self.name} ] {self.variable_name} : {self.variable_type} = {self.variable_value.traverse_and_print(0)}"

    def run(self):
        return self.variable_value.run()


class Scope():
    def __init__(self, name: str, variables: list[VariableNode], functions: list[FunctionNode]):
        self.name = name
        self.variables: list[VariableNode] = variables
        self.functions: list[FunctionNode] = list()

    def add_variable(self, variable: VariableNode):
        self.variables.append(variable)

    def add_function(self, function: FunctionNode):
        self.functions.append(function)

    def remove_function(self, function_name):
        for (index, function) in enumerate(self.functions):
            if function.function_name == function_name:
                self.functions.pop(index)

    def remove_variable(self, variable_name):
        for (index, var) in enumerate(self.variables):
            if var.variable_name == variable_name:
                self.variables.pop(index)

    def get_variable(self, variable_name):
        for var in self.variables:
            if var.variable_name == variable_name:
                return var
        return None

    def get_function(self, function_name):
        for function in self.functions:
            if function.function_name == function_name:
                return function
        return None


class OutVariableNode(ASTNode):
    def __init__(self, variable_name):
        super().__init__("OutVariableNode", None)
        self.variable_name = variable_name

    def run(self, scope: Scope):
        return scope.get_variable(self.variable_name).run()

    def traverse_and_print(self, indent):
        return f"{' '*indent}[ {self.name} ]({self.variable_name})"


class FunctionArgNode(ASTNode):
    def __init__(self, arg_name, arg_type: Types):
        super().__init__("FunctionArgNode", None)
        self.arg_name: str = arg_name
        self.arg_type: Types = arg_type

    def traverse_and_print(self, indent):
        return f"[ {self.name} {self.arg_name} : {self.arg_type} ]"


class FunctionCallArgNode(ASTNode):
    def __init__(self, arg_name, arg_value):
        super().__init__("FunctionCallArgNode", None)
        self.arg_name: str = arg_name
        self.arg_value: str = arg_value

    def traverse_and_print(self, indent):
        return f"[ {self.name} {self.arg_name} : {self.arg_value} ]"

    def run(self):
        pass


class FunctionNode(ASTNode):
    def __init__(self, function_name: str, function_body: list[ASTNode], function_args: list[FunctionArgNode], global_scope):
        super().__init__("FunctionNode", None)
        self.function_name: str = function_name
        self.function_body: list[ASTNode] = function_body
        # TODO: Change to map VV for faster performance
        self.function_args: list[FunctionArgNode] = function_args
        self.local_scope: Scope = global_scope

    def traverse_and_print(self, indent):
        newline = '\n'
        return f"{' '*indent}[ {self.name} {self.function_name}({', '.join([i.traverse_and_print(0) for i in self.function_args])}) ]\n {newline.join([i.traverse_and_print(indent+2) for i in self.function_body])}"

    def run(self, args: list[FunctionCallArgNode] = []):
        for arg in args:
            for farg in self.function_args:
                if farg.arg_name == arg.arg_name:
                    self.local_scope.remove_variable(farg.arg_name)
                    self.local_scope.add_variable(VariableNode(
                        farg.arg_type, farg.arg_name, arg.arg_value))
        return [i.run(self.local_scope) for i in self.function_body]


class LiteralNode(ASTNode):
    def __init__(self, value):
        super().__init__("LiteralNode", None)
        self.value = value

    def traverse_and_print(self, indent: int):
        return f"[{self.name}]: {self.value}"

    def run(self):
        return self.value


class ReturnNode(ASTNode):
    def __init__(self, child):
        super().__init__("ReturnNode", child)

    def run(self, scope):
        return self.child.run(scope)

    def traverse_and_print(self, indent):
        return f"{' '*indent}[ {self.name} ]\n"\
            f"{self.child.traverse_and_print(indent+2)}"


class BinaryOpNode(ASTNode):
    def __init__(self, left_child: ASTNode, right_child: ASTNode, op: BinaryOperations):
        super().__init__("BinaryOpNode", None)
        self.lchild: ASTNode = left_child
        self.rchild: ASTNode = right_child
        self.operation: BinaryOperations = op

    def traverse_and_print(self, indent):
        return f"{' '*indent}[ {self.name} ] : {self.lchild.traverse_and_print(0)} {BinaryOperations.get_op_name(self.operation)} {self.rchild.traverse_and_print(0)}"

    def run(self, scope):
        lv: VariableNode = self.lchild.run(scope)
        rv: VariableNode = self.rchild.run(scope)

        if(self.operation == BinaryOperations.PLUS):
            return lv + rv
        elif(self.operation == BinaryOperations.MINUS):
            return lv - rv
        elif(self.operation == BinaryOperations.MULTIPLY):
            return lv * rv
        elif(self.operation == BinaryOperations.DIVISE):
            return lv / rv
        else:
            return None


class CallExpressionNode(ASTNode):
    def __init__(self, function_name, function_args: list[FunctionCallArgNode]):
        super().__init__("CallExpressionNode", None)
        self.function_name = function_name
        self.function_args = function_args

    def run(self, scope: Scope):
        fct = scope.get_function(self.function_name)
        if not fct:
            print(f"ERROR: invalid function name '{self.function_name}'")
            return
        fct.run()

    def traverse_and_print(self, indent):
        return f"{' '*indent}[ {self.name} ] {self.function_name}({', '.join(i.traverse_and_print(0) for i in self.function_args)})"


class DebugNode(ASTNode):
    def __init__(self, child):
        super().__init__("DebugNode", child)
        self.child = child
    
    def traverse_and_print(self, indent):
        return f"{' '*indent}[ {self.name} ]\n"\
            f"{self.child.traverse_and_print(indent+2)}"
    def run(self,local_scope):
        result = self.child.run(local_scope)
        print(result)
        return result

class AST():
    def __init__(self):
        self.nodes: list[ASTNode] = list()

    def append(self, node: ASTNode):
        self.nodes.append(node)


class ScopedNode(ASTNode):
    def __init__(self, name, children: list[ASTNode], scope):
        super().__init__(f"ScopedNode[{name}]", None)
        self.scope: Scope() = scope
        self.children: list[ASTNode] = children

class Program(ScopedNode):
    def __init__(self, body: list[ASTNode], scope: Scope):
        super().__init__("Program", body, scope)
        self.scope = scope

    def append_child(self, child):
        self.children.append(child)

    def traverse_and_print(self, indent: int):
        print(f"[{self.name}]")
        for i in self.children:
            print(
                f"{' '*indent} {i.traverse_and_print(indent+2)}")

    def run(self):
        main_from_scope = self.scope.get_function("main")
        if not main_from_scope:
            print("ERROR: cannot find function main")
            return

        main_from_scope.run()
