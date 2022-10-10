from antlr4 import *

from gen.TablParser import TablParser
from gen.TablVisitor import TablVisitor
from gen.tablLexer import TablLexer



if __name__ == '__main__':
    inputStream = FileStream("sample.txt")
    lexer = TablLexer(inputStream)
    stream = CommonTokenStream(lexer)
    parser = TablParser(stream)
    tree = parser.rules()
    print(tree)
    visitor = TablVisitor()
    visitor.visit(tree)
