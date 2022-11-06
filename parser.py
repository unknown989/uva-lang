from lang_ast import *
from lang_types import *


class Parser:
    def __init__(self):
        self.ast: AST = AST()
        self.stack: list = list()
        self.scope: Scope = Scope("global_scope", [], [])

    def load_stack(self, stack: list):
        self.stack = stack

    def parse(self):
        if not self.stack:
            print("No stack was loaded, use load_stack(stack: list) to load it.")
            return None
    