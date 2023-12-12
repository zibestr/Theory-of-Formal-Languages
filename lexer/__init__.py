from lexer.states import State
from utils.lexem import Lexem

import lexer.consts as const

from re import match
from queue import Queue


def add_token(token: str, type_: int, queue: Queue) -> Queue:
    queue.put(Lexem(type_, token))
    return queue


def eq_1(buffer: str) -> bool:
    return buffer == "!"


def eq_2(buffer: str) -> bool:
    return buffer == "<" or buffer == ">"


def is_kword(word: str) -> bool:
    return word in const.KWORDS


def is_float(number: str) -> bool:
    return match(r"^(\d+[E,e]{1}[+,-]?\d+)|"
                 r"(\d*[.]{1}\d+([E,e]{1}[+,-]?\d+)?)$", number) is not None


def is_decimal(number: str) -> bool:
    return match(r"^\d+[D,d]?$", number) is not None


def is_hex(number: str) -> bool:
    return match(r"^\d{1}[\d,a-f, A-F]+[H, h]{1}$", number) is not None


def is_oct(number: str) -> bool:
    return match(r"^[0-7]+[O, o]{1}$", number) is not None


def is_bin(number: str) -> bool:
    return match(r"^[0,1]+[B, b]{1}$", number) is not None


def main_loop_lexer(filename: str, encoding: str = "utf-8") -> Queue:
    state = State.H  # now state
    lexems: Queue[Lexem] = Queue()  # result of lexing analyzator
    ch = ""  # now proccessed char
    buffer = ""  # last processed char
    word = ""  # last processed chars for kwords and indeficators
    number = ""  # last processed chars for numbers
    is_comment = False  # start comment flag

    with open(filename, "r", encoding=encoding) as program:
        while state != State.ERR:
            match state:

                case State.H:
                    buffer = ch
                    ch = program.read(1)

                    if ch in const.BLANK_SYMBOLS:
                        continue

                    elif ch in const.EQUALATION_SYMBOLS:
                        state = State.EQ

                    elif ch in const.TYPES:
                        state = State.TY

                    elif ch in const.DELIMITERS:
                        state = State.DEL

                    elif ch == "|":
                        state = State.OR

                    elif ch in const.ADD_OPERATORS:
                        state = State.ADD

                    elif ch == "&":
                        state = State.AND

                    elif ch in const.MUL_OPERATORS:
                        state = State.MUL

                    elif ch == ":":
                        state = State.COL

                    elif ch in const.LETTERS:
                        state = State.LET
                        word = ch

                    elif ch in const.DIGITS:
                        state = State.DIG
                        number = ch

                    elif ch == "/":
                        state = State.COM

                    else:
                        state = State.ERR

                    continue

                case State.EQ:
                    buffer = ch
                    ch = program.read(1)

                    if ch == "=":
                        lexems = add_token(buffer + ch, 11, lexems)
                        state = State.H

                    elif ch == " " and eq_2(buffer):
                        lexems = add_token(buffer, 11, lexems)
                        state = State.H

                    elif ch == ";" and eq_1(buffer):
                        state = State.TY

                    elif eq_1(buffer):
                        state = State.UN

                    else:
                        state = State.ERR

                    continue

                case State.TY:
                    if ch == ";":
                        lexems = add_token(buffer, 10, lexems)
                        state = State.DEL

                    else:
                        lexems = add_token(ch, 10, lexems)
                        state = State.H

                    continue

                case State.UN:
                    lexems = add_token(buffer, 14, lexems)

                    if ch == "(":
                        state = State.DEL

                    else:
                        state = State.LET
                        word = ch

                    continue

                case State.COL:
                    buffer = ch
                    ch = program.read(1)

                    if ch == "=":
                        state = State.ASG

                    elif ch == " ":
                        state = State.DEL

                    else:
                        state = State.ERR

                    continue

                case State.DEL:
                    if buffer == ":":
                        lexems = add_token(buffer, 5, lexems)

                    else:
                        lexems = add_token(ch, 5, lexems)

                    state = State.H
                    continue

                case State.OR:
                    buffer = ch
                    ch = program.read(1)

                    if ch == "|":
                        state = State.ADD

                    else:
                        state = State.ERR

                    continue

                case State.ADD:
                    if ch == "|":
                        lexems = add_token(buffer + ch, 12, lexems)

                    else:
                        lexems = add_token(ch, 12, lexems)

                    state = State.H
                    continue

                case State.AND:
                    buffer = ch
                    ch = program.read(1)

                    if ch == "&":
                        state = State.MUL

                    else:
                        state = State.ERR

                    continue

                case State.MUL:
                    if ch == "&":
                        lexems = add_token(buffer + ch, 13, lexems)

                    else:
                        lexems = add_token(ch, 13, lexems)

                    state = State.H
                    continue

                case State.ASG:
                    lexems = add_token(buffer + ch, 6, lexems)
                    state = State.H

                    continue

                case State.LET:
                    buffer = ch
                    ch = program.read(1)

                    if ch in const.BLANK_SYMBOLS or \
                            ch in const.DELIMITERS or ch == ":":
                        state = State.ID

                    elif ch in const.LETTERS or ch in const.DIGITS:
                        word += ch

                    else:
                        state = State.ERR

                    continue

                case State.ID:
                    if is_kword(word):
                        if word == "true" or word == "false":
                            state = State.BOOL

                        else:
                            state = State.KW

                    else:
                        lexems = add_token(word, 8, lexems)
                        word = ""

                        if ch in const.DELIMITERS:
                            state = State.DEL

                        elif ch == ":":
                            state = State.COL

                        else:
                            state = State.H

                    continue

                case State.KW:
                    lexems = add_token(word, 7, lexems)
                    word = ""

                    if ch in const.DELIMITERS:
                        state = State.DEL

                    elif ch == ":":
                        state = State.COL

                    else:
                        state = State.H

                    continue

                case State.DIG:
                    buffer = ch
                    ch = program.read(1)

                    if ch in const.DELIMITERS or ch in const.BLANK_SYMBOLS:
                        state = State.NUM

                    elif ch in const.DIGITS or ch in const.NODECIMAL_SYMBOLS:
                        number += ch

                    else:
                        state = State.ERR

                    continue

                case State.NUM:
                    if is_float(number):
                        state = State.FLT

                    elif is_decimal(number):
                        state = State.DEC

                    elif is_hex(number):
                        state = State.HEX

                    elif is_oct(number):
                        state = State.OCT

                    elif is_bin(number):
                        state = State.BIN

                    else:
                        state = State.ERR
                        number = ""

                    continue

                case State.FLT:
                    lexems = add_token(number, 9, lexems)
                    number = ""

                    if ch in const.DELIMITERS:
                        state = State.DEL

                    else:
                        state = State.H

                    continue

                case State.DEC:
                    lexems = add_token(number, 2, lexems)
                    number = ""

                    if ch in const.DELIMITERS:
                        state = State.DEL

                    else:
                        state = State.H

                    continue

                case State.HEX:
                    lexems = add_token(number, 1, lexems)
                    number = ""

                    if ch in const.DELIMITERS:
                        state = State.DEL

                    else:
                        state = State.H

                    continue

                case State.OCT:
                    lexems = add_token(number, 3, lexems)
                    number = ""

                    if ch in const.DELIMITERS:
                        state = State.DEL

                    else:
                        state = State.H

                    continue

                case State.BIN:
                    lexems = add_token(number, 4, lexems)
                    number = ""

                    if ch in const.DELIMITERS:
                        state = State.DEL

                    else:
                        state = State.H

                    continue

                case State.COM:
                    if not is_comment:
                        buffer = ch
                        ch = program.read(1)

                        if ch == "*":
                            is_comment = True

                        else:
                            state = State.ERR

                    elif is_comment:
                        buffer = ch
                        ch = program.read(1)

                        if ch == "/" and buffer == "*":
                            state = State.H

                    continue

                case State.BOOL:
                    lexems = add_token(word, 15, lexems)
                    word = ""

                    if ch in const.DELIMITERS:
                        state = State.DEL

                    elif ch == ":":
                        state = State.COL

                    else:
                        state = State.H

                    continue

    return lexems


def save_queue(queue: Queue, filename: str, encoding: str = "utf-8") -> None:
    with open(filename, "w", encoding=encoding) as file:
        while not queue.empty():
            file.write(str(queue.get()) + "\n")
