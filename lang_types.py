from enum import Enum

class Tokens(Enum):
    TKN_FUNCTION = -1
    TKN_VAR = -2
    TKN_RETURN = -3
    TKN_FUNCTION_ARG = -4


class Types(Enum):
    INT = 0
    STRING = 1
    BOOL = 2
    UNKNOWN = 3

class BinaryOperations(Enum):
    PLUS = 4
    MULTIPLY = 5
    MINUS = 6
    DIVISE = 7
    # Add logic operations like AND OR...

    def get_op_name(op):
        if op == BinaryOperations.PLUS:
            return "+"
        elif op == BinaryOperations.MINUS:
            return "-"
        elif op == BinaryOperations.MULTIPLY:
            return "*"
        elif op == BinaryOperations.DIVISE:
            return "/"
        else:
            return "N/A"