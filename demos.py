from lang_ast import *


class BasicProgram:
    """
    Program:

    var a : int = 1;
    var b : int = 2;

    function sum(a: int, b: int){
        debugPrint(a + b);
    }

    function main(){
        sum(a + b);
    }
    """
    def __init__(self):
        self.ast = AST()
        self.global_scope = Scope("Global_Scope", [], [])
        var_a = VariableNode(Types.INT, "a", LiteralNode(1))
        var_b = VariableNode(Types.INT, "b", LiteralNode(2))

        self.global_scope.add_variable(var_a)
        self.global_scope.add_variable(var_b)

        function_sum_body = [
            DebugNode(BinaryOpNode(OutVariableNode(
                "a"), OutVariableNode("b"), BinaryOperations.PLUS)),
        ]

        function_sum = FunctionNode("sum", function_sum_body, [FunctionArgNode(
            "a", Types.INT), FunctionArgNode("b", Types.INT)], self.global_scope)

        function_main = FunctionNode("main", [CallExpressionNode("sum", [FunctionCallArgNode(
            "a", 1), FunctionCallArgNode("b", 2)])], [], self.global_scope)

        self.global_scope.add_function(function_main)
        self.global_scope.add_function(function_sum)

        expressions = [var_a, var_b, function_sum, function_main]

        program = Program(expressions, self.global_scope)

        program.traverse_and_print(0)
        self.ast.append(program)

    def run(self):
        for node in self.ast.nodes:
            if "Program" in node.name:
                node.run()
                break
