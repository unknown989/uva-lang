from pprint import pprint

from lang_ast import *
from lang_types import Tokens


class Lexer:
    def __init__(self):
        self.stack = []
        self.file_content = ""

        self.curr_index = 0

    def set_file(self, filename: str):
        with open(filename, "r") as f:
            self.file_content = f.read()

    def get_char(self):
        self.curr_index += 1
        return self.file_content[self.curr_index-1]
    # Variable Parsing var a : ... = ...

    def parse_variable(self):
        tmp = ""
        variable_name = ""
        variable_type = ""
        variable_value = ""
        while True:
            if len(self.file_content) <= self.curr_index:
                break
            c = self.get_char()

            if c == ';':
                break

            if c.isspace():
                c = self.get_char()

            if c.isalnum() and not variable_name:
                tmp += c

            elif c.isalpha() and not variable_type:
                tmp += c

            elif not variable_value and variable_type and variable_name:
                tmp += c

            if c == ':':
                variable_name = tmp
                tmp = ""
            if c == '=':
                variable_type = tmp
                tmp = ""
            if variable_type:
                variable_value = tmp
                tmp = ""

        variable_basic_node = {"token_type": Tokens.TKN_VAR, "var_name": variable_name,
                               "var_type": variable_type, "var_value": variable_value}
        return variable_basic_node

    # Call expresiions parsing func(...)
    def parse_call(self):
        tmp = ""
        while True:
            if len(self.file_content) <= self.curr_index:
                break
        return

    # Binary Operations parsing + - / *...
    def parse_op(self, starting_index):

        """tmp = ""
        op = ""
        left = ""
        right = ""
        self.curr_index = starting_index
        # TODO: many binary operations
        while True:
            if len(self.file_content) <= self.curr_index:
                break

            c = self.get_char()

            if c.isspace():
                c = self.get_char()

            if c == ";":
                right = tmp
                break

            if c.isalnum():
                tmp += c

            if c in ["+", "-", "/", "*"]:
                op = c
                left = tmp
                tmp = ""
                """
        #print(f"{left} {op} {right}")
        return None

    # Return statement parsing return ...

    def parse_return(self):
        tmp = ""
        return_index = self.curr_index
        while True:
            if len(self.file_content) <= self.curr_index:
                break

            c = self.get_char()

            if c == "+" or c == "-" or c == "*" or c == "/":  # Do more operations
                print(self.curr_index)
                self.parse_op(return_index)

            if c.isspace():
                continue
            if c == '}':
                break

    # Function parsing func foo(...){...}
    def parse_function(self):
        function_name = ""
        function_params = []
        function_body = []
        should_get_params = False
        should_get_body = False
        tmp = ""
        while True:
            # TODO: Parse function body :)
            if len(self.file_content) <= self.curr_index:
                break

            c = self.get_char()
            if should_get_params:
                arg_name = ""
                arg_type = ""
                tmp = ""
                while True:
                    if len(self.file_content) <= self.curr_index:
                        break

                    if c.isspace():
                        c = self.get_char()

                    if c.isalpha() and not arg_name:
                        tmp += c

                    elif c.isalpha() and not arg_type:
                        tmp += c

                    if c == ':':
                        arg_name = tmp
                        tmp = ""

                    if c == ',':
                        arg_type = tmp
                        tmp = ""
                        arg_basic_node = {
                            "token_type": Tokens.TKN_FUNCTION_ARG, "arg_name": arg_name, "arg_type": arg_type}
                        function_params.append(arg_basic_node)
                        arg_name = arg_type = ""

                    if c == ')':
                        if not arg_name:
                            should_get_params = False
                            break
                        arg_type = tmp
                        tmp = ""
                        arg_basic_node = {
                            "token_type": Tokens.TKN_FUNCTION_ARG, "arg_name": arg_name, "arg_type": arg_type}
                        function_params.append(arg_basic_node)
                        arg_name = arg_type = ""
                        should_get_params = False
                        break

                    c = self.get_char()
            if should_get_body:
                local_stack = []
                tmp = ""

                while True:
                    if len(self.file_content) <= self.curr_index:
                        break

                    c = self.get_char()

                    if c.isspace():
                        c = self.get_char()

                    if c.isalpha():
                        tmp += c

                    if tmp == "var":
                        a = self.parse_variable()
                        local_stack.append(a)
                        tmp = ""

                    if tmp == "return":
                        a = self.parse_return()
                        local_stack.append(a)

                    # Add function calls

                    if c == "}":
                        break

            if c.isspace():
                c = self.get_char()

            if c.isalnum():
                tmp += c

            if c == '(' and not should_get_body:
                if not should_get_params:
                    should_get_params = True
                function_name = tmp
                tmp = ""
            if c == ')':
                should_get_params = False
                tmp = ""
            if c == '{':
                should_get_body = True
                tmp = ""
            if c == '}':
                should_get_body = False
                break
        function_basic_node = {"token_type": Tokens.TKN_FUNCTION, "function_name": function_name,
                               "function_body": function_body, "function_params": function_params}
        return function_basic_node

    def lex(self):
        token_str = ""
        while True:
            if len(self.file_content) <= self.curr_index:
                break

            c = self.get_char()

            if c.isspace():
                c = self.get_char()
                token_str = ""

            if c.isalnum():
                token_str += c

            if token_str == "var":  # Concerning the 'var'
                node = self.parse_variable()
                self.stack.append(node)
            if token_str == "function":  # Concerning the 'function'
                node = self.parse_function()
                self.stack.append(node)
        # pprint(self.stack)
        return self.stack
