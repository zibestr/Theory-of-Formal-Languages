from enum import Enum


class LexemType(Enum):
    HexNumber = 1
    DecNumber = 2
    OctNumber = 3
    BinNumber = 4
    Delimiter = 5
    Assigment = 6
    KeyWord = 7
    Identifier = 8
    Float = 9
    Type = 10
    EqualationOperator = 11
    AdditionOperator = 12
    MultiplicationOperator = 13
    UnaryOperator = 14
    Boolean = 15
