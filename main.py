from parser import Parser

from demos import BasicProgram
from lexer import Lexer


def main():
    # program = BasicProgram()
    # program.run()
    # TODO: Add filename from CLI
    filename = "main.uva"

    lexer = Lexer()
    parser = Parser()

    lexer.set_file(filename)
    stack = lexer.lex()

    parser.load_stack(stack)
    ast = parser.parse()


if __name__ == "__main__":
    main()
