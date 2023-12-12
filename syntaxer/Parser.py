from syntaxer.InspectedQueue import InspectedQueue
import syntaxer.exceptions as exc
import syntaxer.consts as const
from utils.lextypes import LexemType


class Parser:
    def __init__(self, tokens: InspectedQueue):
        self.tokens: InspectedQueue = tokens

        self.numtypes: list[LexemType] = [LexemType.Float, LexemType.HexNumber,
                                          LexemType.BinNumber,
                                          LexemType.OctNumber,
                                          LexemType.DecNumber]

    def parse(self):
        self.P()

    def is_D(self) -> bool:
        return self.tokens.inspect().typ == LexemType.Identifier and \
                self.tokens.inspect_next().typ != LexemType.Assigment

    def is_A(self) -> bool:
        return self.tokens.inspect().typ == LexemType.Identifier

    def is_Q(self) -> bool:
        return self.tokens.inspect().typ == LexemType.EqualationOperator

    def is_P(self) -> bool:
        return self.tokens.inspect().typ == LexemType.AdditionOperator

    def is_L(self) -> bool:
        return self.tokens.inspect().typ == LexemType.MultiplicationOperator

    # program grammar rules
    def rule_P(self):
        if self.tokens.inspect() == const.OPEN_BRACE:
            self.tokens.get()
            try:
                while self.tokens.inspect() != const.CLOSE_BRACE:
                    if self.is_D():
                        self.rule_D()
                    else:
                        self.rule_O()
            except IndexError:
                raise exc.ProgramSyntaxError("Expected a delimiter \"}\" at "
                                             "ending of program")
            self.tokens.get()

            if not self.tokens.is_empty():
                raise exc.ProgramSyntaxError("Find a lexem after ending of "
                                             "program")

        else:
            raise exc.ProgramSyntaxError("Expected a delimiter \"{\" at "
                                         "beginning of program")

    # description grammar rules
    def rule_D(self):
        if self.tokens.get().typ == LexemType.Identifier:

            while self.tokens.inspect() == const.COMMA:
                self.tokens.get()
                if self.tokens.get().typ != LexemType.Identifier:
                    raise exc.DescriptionSyntaxError("Expected a identifier")

            if self.tokens.get() != const.COLON:
                raise exc.DescriptionSyntaxError("Expected a delimiter \":\"")

            if self.tokens.get().typ == LexemType.Type:
                if self.tokens.get() != const.SEMICOLON:
                    raise exc.DescriptionSyntaxError("Expected a delimiter "
                                                     "\";\"")

            else:
                raise exc.DescriptionSyntaxError("Expected a type")

        else:
            raise exc.DescriptionSyntaxError("Expected a identifier")

    # operator grammar rules
    def rule_O(self):
        if self.is_A():
            self.rule_A()
            self.check_semicolon()

        elif self.tokens.inspect().typ == LexemType.KeyWord:
            match self.tokens.get().container:

                case "begin":

                    self.rule_O()
                    while self.tokens.inspect() != const.END:
                        self.rule_O()

                        if self.tokens.is_empty():
                            raise exc.OperatorSyntaxError("Expected a keyword "
                                                          "\"end\"")
                    self.tokens.get()
                    self.check_semicolon()

                case "if":

                    if self.tokens.get() == const.OPEN_BRACKET:
                        self.rule_E()

                        if self.tokens.get() == const.CLOSE_BRACKET:
                            self.rule_O()
                            if self.tokens.inspect() == const.ELSE:
                                self.tokens.get()
                                self.rule_O()
                        else:
                            raise exc.OperatorSyntaxError("Expected a "
                                                          "delimiter \")\"")
                    else:
                        raise exc.OperatorSyntaxError("Expected a delimiter "
                                                      "\"(\"")

                case "for":

                    if self.is_A():
                        self.rule_A()
                        if self.tokens.get() == const.TO:
                            self.rule_E()
                        else:
                            raise exc.OperatorSyntaxError("Expected a keyword "
                                                          "\"to\"")

                    elif self.tokens.get() == const.STEP:
                        self.rule_E()

                    else:
                        raise exc.OperatorSyntaxError("Expected a keyword "
                                                      "\"step\" or assigment")

                    self.rule_O()

                    if self.tokens.get() != const.NEXT:
                        raise exc.OperatorSyntaxError("Expected a keyword "
                                                      "\"next\"")

                    self.check_semicolon()

                case "while":

                    if self.tokens.get() == const.OPEN_BRACKET:
                        self.rule_E()

                        if self.tokens.get() == const.CLOSE_BRACKET:
                            self.rule_O()

                        else:
                            raise exc.OperatorSyntaxError("Expected a "
                                                          "delimiter \")\"")

                    else:
                        raise exc.OperatorSyntaxError("Expected a delimiter "
                                                      "\"(\"")

                case "readln":

                    if self.tokens.get().typ != LexemType.Identifier:
                        raise exc.OperatorSyntaxError("Expected a identifier")

                    while self.tokens.inspect() == const.COMMA:
                        self.tokens.get()

                        if self.tokens.get().typ != LexemType.Identifier:
                            raise exc.OperatorSyntaxError("Expected a "
                                                          "identifier")

                    self.check_semicolon()

                case "writeln":

                    self.rule_E()
                    while self.tokens.inspect() == const.COMMA:
                        self.tokens.get()
                        self.rule_E()

                    self.check_semicolon()

        else:
            raise exc.OperatorSyntaxError("Expected a keyword or identifier")

    def check_semicolon(self):
        if self.tokens.get() != const.SEMICOLON:
            raise exc.OperatorSyntaxError("Expected a delimiter \";\" at the "
                                          "end of line")

    # assignment grammar rules
    def rule_A(self):
        if self.tokens.get().typ == LexemType.Identifier:
            if self.tokens.get().typ == LexemType.Assigment:
                self.rule_E()

            else:
                raise exc.AssigmentSyntaxError("Expected an assignment "
                                               "operator")

        else:
            raise exc.AssigmentSyntaxError("Expected a identifier")

    # expression grammar rules
    def rule_E(self):
        self.rule_C()

        while self.is_Q():
            self.tokens.get()
            self.rule_C()

    # operand grammar rules
    def rule_C(self):
        self.rule_F()

        while self.is_P():
            self.tokens.get()
            self.rule_F()

    # term grammar rules
    def rule_F(self):
        self.rule_M()

        while self.is_L():
            self.tokens.get()
            self.rule_M()

    # factor grammar rules
    def rule_M(self):
        if self.tokens.inspect() == const.OPEN_BRACKET:
            self.tokens.get()
            self.rule_E()

            if self.tokens.get() != const.CLOSE_BRACKET:
                raise exc.ExpressionSyntaxError("Expected a delimiter \")\"")

        elif self.tokens.inspect().typ in self.numtypes or \
                self.tokens.inspect().typ == LexemType.Boolean or \
                self.tokens.inspect().typ == LexemType.Identifier:
            self.tokens.get()

        elif self.tokens.inspect().typ == LexemType.UnaryOperator:
            self.tokens.get()
            self.rule_M()

        else:
            raise exc.ExpressionSyntaxError("Wrong expression syntax")
