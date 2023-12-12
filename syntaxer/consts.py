from utils.lexem import Lexem
from utils.lextypes import LexemType


OPEN_BRACE = Lexem(LexemType.Delimiter, "{")
CLOSE_BRACE = Lexem(LexemType.Delimiter, "}")
OPEN_BRACKET = Lexem(LexemType.Delimiter, "(")
CLOSE_BRACKET = Lexem(LexemType.Delimiter, ")")
COMMA = Lexem(LexemType.Delimiter, ",")
COLON = Lexem(LexemType.Delimiter, ":")
SEMICOLON = Lexem(LexemType.Delimiter, ";")

END = Lexem(LexemType.KeyWord, "end")
ELSE = Lexem(LexemType.KeyWord, "else")
TO = Lexem(LexemType.KeyWord, "to")
STEP = Lexem(LexemType.KeyWord, "step")
NEXT = Lexem(LexemType.KeyWord, "next")
