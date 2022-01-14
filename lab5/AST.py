
class Node(object):
    def __init__(self):
        self.line_no = None

    def accept(self, visitor):
        return visitor.visit(self)


class Start(Node):
    def __init__(self, lines):
        super().__init__()
        self.lines = lines


class Stop(Node):
    def __init__(self):
        super().__init__()


class Lines(Node):
    def __init__(self, line, nextLine):
        super().__init__()
        self.line = line
        self.nextLine = nextLine


class IdxAssign(Node):
    def __init__(self, ID, expression):
        super().__init__()
        self.ID = ID
        self.expression = expression


class IntNum(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value


class Id(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name


class String(Node):
    def __init__(self, string):
        super().__init__()
        self.string = string


class BinExpr(Node):
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right


# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self):
        super().__init__()
        pass


class IdxOneDimensionTableAssign(Node):
    def __init__(self, ID, expression1, expression2):
        super().__init__()
        self.ID = ID
        self.expression1 = expression1
        self.expression2 = expression2


class IdxTwoDimensionTableAssign(Node):
    def __init__(self, ID, expression1, expression2, expression3):
        super().__init__()
        self.ID = ID
        self.expression1 = expression1
        self.expression2 = expression2
        self.expression3 = expression3


class IdxTwoDimensionTableAssignBySlicing(Node):
    def __init__(self, ID, expression1, expression2, expression3, expression4, expression5):
        super().__init__()
        self.ID = ID
        self.expression1 = expression1
        self.expression2 = expression2
        self.expression3 = expression3
        self.expression4 = expression4
        self.expression5 = expression5


class IdxOpAssign(Node):
    def __init__(self, ID, op, expression):
        super().__init__()
        self.ID = ID
        self.op = op
        self.expression = expression


class Zeros(Node):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression


class Ones(Node):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression


class Eye(Node):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression


class Zeros2(Node):
    def __init__(self, expression1, expression2):
        super().__init__()
        self.expression1 = expression1
        self.expression2 = expression2


class Ones2(Node):
    def __init__(self, expression1, expression2):
        super().__init__()
        self.expression1 = expression1
        self.expression2 = expression2


class Eye2(Node):
    def __init__(self, expression1, expression2):
        super().__init__()
        self.expression1 = expression1
        self.expression2 = expression2


class Matrix(Node):
    def __init__(self, matrixInside):
        super().__init__()
        self.matrixInside = matrixInside


class MatrixInside(Node):
    def __init__(self, table, matrixInside):
        super().__init__()
        self.table = table
        self.matrixInside = matrixInside


class Table(Node):
    def __init__(self, values):
        super().__init__()
        self.values = values


class Values(Node):
    def __init__(self, expression, values):
        super().__init__()
        self.expression = expression
        self.values = values


class MatrixExpression(Node):
    def __init__(self, expression1, op, matrixExpression2):
        super().__init__()
        self.expression1 = expression1
        self.matrixExpression2 = matrixExpression2
        self.op = op


class Transpose(Node):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression


class IfxIf(Node):
    def __init__(self, condition, line):
        super().__init__()
        self.condition = condition
        self.line = line


class IfxIfElse(Node):
    def __init__(self, condition, line1, line2):
        super().__init__()
        self.condition = condition
        self.line1 = line1
        self.line2 = line2


class Condition(Node):
    def __init__(self, expression1, op, expression2):
        super().__init__()
        self.expression1 = expression1
        self.expression2 = expression2
        self.op = op


class Return(Node):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression


class While(Node):
    def __init__(self, condition, line):
        super().__init__()
        self.condition = condition
        self.line = line


class For(Node):
    def __init__(self, ID, expression1, expression2, line):
        super().__init__()
        self.ID = ID
        self.expression1 = expression1
        self.expression2 = expression2
        self.line = line


class Print(Node):
    def __init__(self, printMany):
        super().__init__()
        self.printMany = printMany


class PrintMany(Node):
    def __init__(self, printOne, printMany):
        super().__init__()
        self.printOne = printOne
        self.printMany = printMany


class PrintManyTable(Node):
    def __init__(self, printID, printTable, printMany):
        super().__init__()
        self.printID = printID
        self.printTable = printTable
        self.printMany = printMany


class PrintTable(Node):
    def __init__(self, printID, printTable):
        super().__init__()
        self.printID = printID
        self.printTable = printTable


class PrintTriangle(Node):
    def __init__(self, string, expression):
        super().__init__()
        self.string = string
        self.expression = expression


class Negation(Node):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression


class Break(Node):
    def __init__(self):
        super().__init__()
        pass


class Continue(Node):
    def __init__(self):
        super().__init__()


