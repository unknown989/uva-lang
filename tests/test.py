from enum import Enum
from pprint import pprint


class OP(Enum):
    plus = 0
    sub = 1
    mul = 2
    div = 3


expression = "1 + 2 * 54 - a + 1443"
cursor = 0
tmp = ""


class Variables:
    def __init__(self) -> None:
        self.vars = {}

    def add_variable(self, name: str, value):
        self.vars[name] = value

    def get_variable(self, name):
        return self.vars[name]


stack = Variables()

stack.add_variable("a", 123)


class Node:
    def __init__(self, name: str, data) -> None:
        self.name = name
        self.data = data

    def get_data(self):
        return self.data

    def get_name(self):
        return self.name

    def is_none(self):
        return not self.data

    def run(self):
        raise NotImplementedError()


class Literal(Node):
    def __init__(self, data: int) -> None:
        super().__init__("Literal", data)

    def __repr__(self) -> str:
        return f"{self.data}"

    def __eq__(self, __o: object) -> bool:
        return self.data == __o

    def run(self):
        return self.get_data()


class NumNode(Node):
    def __init__(self, data: Node, operation: OP) -> None:
        super().__init__("NumNode", data)
        self.operation: OP = operation


def get_char() -> str:
    return expression[cursor]


def parse_num() -> dict:
    global tmp, cursor
    left: Node = None
    right: Node = None
    op: str = ""
    while True:
        if cursor >= len(expression):
            if tmp:
                if not left:
                    left = int(tmp.replace(" ", ""))
            break

        char = get_char()

        if char.isspace():
            char = get_char()

        if char.isalnum():
            if char.isalpha():
                varname = ""
                while True:
                    if cursor >= len(expression):
                        break
                    c = get_char()
                    if c.isspace():
                        break
                    varname += c

                    cursor += 1
                tmp += str(stack.get_variable(varname))
            else:
                tmp += char

        if char in ["+", "-", "/", "*"]:
            if not left:
                if tmp:
                    left = Literal(int(tmp.replace(" ", "")))
                    op = char
                    tmp = ""
            if left:
                right = parse_num()
        cursor += 1

    return {"left": left, "right": right, "op": op}


def do_op(op, right, left):
    s = 0
    op = op
    left = left
    right = right

    print(left)
    if right is None:
        return left

    match op:
        case "+":
            s = left.run() + do_op(right["op"], right["right"], right["left"])
        case "*":
            s = left.run() * do_op(right["op"], right["right"], right["left"])
        case "-":
            s = left.run() - do_op(right["op"], right["right"], right["left"])
        case "/":
            s = left.run() / do_op(right["op"], right["right"], right["left"])

    return s


def lex():
    tree = parse_num()

    print(do_op(tree["op"], tree["right"], tree["left"]))


lex()
