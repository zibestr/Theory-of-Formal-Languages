from dataclasses import dataclass
from utils.lextypes import LexemType


@dataclass
class Lexem:
    typ: LexemType
    container: str

    def __init__(self, type_: int, container: str):
        self.typ = LexemType(type_)
        self.container = container

    def __str__(self) -> str:
        return f"{self.typ.value} {self.container}"

    def __repr__(self) -> str:
        return f"{self.typ} {self.container}"
