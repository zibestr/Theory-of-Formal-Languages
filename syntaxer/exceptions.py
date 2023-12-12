class ProgramSyntaxError(SyntaxError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DescriptionSyntaxError(SyntaxError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class OperatorSyntaxError(SyntaxError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class AssigmentSyntaxError(SyntaxError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class ExpressionSyntaxError(SyntaxError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)