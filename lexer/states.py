from enum import Enum


class State(Enum):
    H = 1  # Start state
    EQ = 2  # Equalation state
    TY = 3  # Type state
    UN = 4  # Unary state
    ADD = 5  # Addition state
    OR = 6  # Or operation state
    AND = 7  # And operation state
    MUL = 8  # Multiplication state
    LET = 9  # Letter state
    KW = 10  # Keyword state
    ID = 11  # Identifier state
    DIG = 12  # Digit state
    NUM = 13  # Unknown number type state
    BIN = 14  # Binary state
    OCT = 15  # Octal state
    DEC = 16  # Decimal state
    HEX = 17  # Hexadecimal state
    FLT = 18  # Float state
    DEL = 19  # Delimiter state
    ASG = 20  # Assignment state
    COL = 21  # Colon state
    COM = 22  # Comment state
    BOOL = 23  # Boolean state
    ERR = 24  # Fianl state
