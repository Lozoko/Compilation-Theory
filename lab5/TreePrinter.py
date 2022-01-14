from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @classmethod
    def printWithIndent(cls, element, indents):
        for _ in range(indents):
            print("|    ",end="")
        print(element)

    @addToClass(AST.Start)
    def printTree(self, indent=0):
        self.lines.printTree(indent)

    @addToClass(AST.Stop)
    def printTree(self, indent=0):
        pass

    @addToClass(AST.Lines)
    def printTree(self, indent=0):
        self.line.printTree(indent)
        self.nextLine.printTree(indent)

    @addToClass(AST.IdxAssign)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent('=', indent)
        TreePrinter.printWithIndent(self.ID, indent+1)
        self.expression.printTree(indent+1)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent(self.value, indent)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent(self.value, indent)

    @addToClass(AST.Id)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent(self.name, indent)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent(self.string, indent)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass    
        # fill in the body

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.IdxOneDimensionTableAssign)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent('=', indent)
        TreePrinter.printWithIndent("VECTOR1D", indent+1)
        TreePrinter.printWithIndent(self.ID, indent+2)
        self.expression1.printTree(indent+2)
        self.expression2.printTree(indent+1)

    @addToClass(AST.IdxTwoDimensionTableAssign)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent('=', indent)
        TreePrinter.printWithIndent("VECTOR2D", indent + 1)
        TreePrinter.printWithIndent(self.ID, indent+2)
        self.expression1.printTree(indent + 2)
        self.expression2.printTree(indent + 2)
        self.expression3.printTree(indent + 1)

    @addToClass(AST.IdxTwoDimensionTableAssignBySlicing)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent('=', indent)
        TreePrinter.printWithIndent("VECTOR2D", indent + 1)
        TreePrinter.printWithIndent(self.ID, indent + 2)
        self.expression1.printTree(indent + 2)
        TreePrinter.printWithIndent(":", indent + 2)
        self.expression2.printTree(indent + 2)
        self.expression3.printTree(indent + 2)
        TreePrinter.printWithIndent(":", indent + 2)
        self.expression4.printTree(indent + 2)
        self.expression5.printTree(indent + 1)

    @addToClass(AST.IdxOpAssign)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent(self.op, indent)
        TreePrinter.printWithIndent(self.ID, indent + 1)
        self.expression.printTree(indent + 1)

    @addToClass(AST.Zeros)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("zeros", indent)
        self.expression.printTree(indent + 1)

    @addToClass(AST.Ones)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("ones", indent)
        self.expression.printTree(indent + 1)

    @addToClass(AST.Eye)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("eye", indent)
        self.expression.printTree(indent + 1)

    @addToClass(AST.Zeros2)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("zeros", indent)
        self.expression1.printTree(indent + 1)
        self.expression2.printTree(indent + 1)

    @addToClass(AST.Ones2)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("ones", indent)
        self.expression1.printTree(indent + 1)
        self.expression2.printTree(indent + 1)

    @addToClass(AST.Eye2)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("eye", indent)
        self.expression1.printTree(indent + 1)
        self.expression2.printTree(indent + 1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("VECTOR2D", indent)
        self.matrixInside.printTree(indent+1)

    @addToClass(AST.MatrixInside)
    def printTree(self, indent=0):
        self.table.printTree(indent)
        self.matrixInside.printTree(indent)

    @addToClass(AST.Table)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("VECTOR1D", indent)
        self.values.printTree(indent + 1)

    @addToClass(AST.Values)
    def printTree(self, indent=0):
        self.expression.printTree(indent)
        self.values.printTree(indent)

    @addToClass(AST.MatrixExpression)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent(self.op, indent)
        self.expression1.printTree(indent + 1)
        self.matrixExpression2.printTree(indent + 1)

    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("TRANSPOSE", indent)
        self.expression.printTree(indent + 1)

    @addToClass(AST.IfxIf)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("IF", indent)
        self.condition.printTree(indent + 1)
        TreePrinter.printWithIndent("THEN", indent)
        self.line.printTree(indent + 1)

    @addToClass(AST.IfxIfElse)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("IF", indent)
        self.condition.printTree(indent + 1)
        TreePrinter.printWithIndent("THEN", indent)
        self.line1.printTree(indent + 1)
        TreePrinter.printWithIndent("ELSE", indent)
        self.line2.printTree(indent + 1)

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent(self.op, indent)
        self.expression1.printTree(indent + 1)
        self.expression2.printTree(indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("RETURN", indent)
        self.expression.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("WHILE", indent)
        self.condition.printTree(indent + 1)
        self.line.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("FOR", indent)
        TreePrinter.printWithIndent(self.ID, indent+1)
        TreePrinter.printWithIndent("RANGE", indent+1)
        self.expression1.printTree(indent+2)
        self.expression2.printTree(indent+2)
        self.line.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("PRINT", indent)
        self.printMany.printTree(indent + 1)

    @addToClass(AST.PrintMany)
    def printTree(self, indent=0):
        self.printOne.printTree(indent)
        self.printMany.printTree(indent)

    @addToClass(AST.PrintManyTable)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent(self.printID, indent)
        self.printTable.printTree(indent)
        self.printMany.printTree(indent)

    @addToClass(AST.PrintTable)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent(self.printID, indent)
        self.printTable.printTree(indent)

    @addToClass(AST.PrintTriangle)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("PRINT", indent)
        TreePrinter.printWithIndent(self.string, indent+1)
        #TreePrinter.printWithIndent(self.expression, indent+1)
        self.expression.printTree(indent+1)

    @addToClass(AST.Negation)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent('-', indent)
        self.expression.printTree(indent+1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("BREAK", indent)

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        TreePrinter.printWithIndent("CONTINUE", indent)


