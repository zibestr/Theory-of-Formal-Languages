from syntaxer.InspectedQueue import InspectedQueue

from utils.lexem import Lexem
from syntaxer.Parser import Parser


def load_lexems_list(filename: str, encoding: str) -> InspectedQueue:
    tokens: InspectedQueue[Lexem] = InspectedQueue()
    with open(filename, "r", encoding=encoding) as tokens_file:
        for line in tokens_file.readlines():
            id_, token_ = line.split()
            tokens.put(Lexem(int(id_), token_))
    return tokens


def main_loop_syntaxer(tokens_filename: str, encoding: str = "utf-8"):
    tokens: InspectedQueue[Lexem] = load_lexems_list(tokens_filename, encoding)
    parser: Parser = Parser(tokens)
    parser.parse()
