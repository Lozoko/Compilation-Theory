import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
from operator import *
import sys

sys.setrecursionlimit(10000)
operators = {'+': add, '-': sub, '*': mul, '/': truediv, '==': eq, '!=': ne, '>': gt, '<': lt, '<=': le, '>=': ge,
             '+=': iadd, '-=': isub, '*=': imul, '/=': itruediv}


class Interpreter(object):
    def __init__(self):
        self.globalMemory = MemoryStack(Memory("global"))

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Node)
    def visit(self, node):
        pass

    @when(AST.Start)
    def visit(self, node):
        #print("start")
        node.lines.accept(self)

    @when(AST.Stop)
    def visit(self, node):
        pass

    @when(AST.Lines)
    def visit(self, node):
        #print("lines")
        node.line.accept(self)
        node.nextLine.accept(self)

    @when(AST.IdxAssign)
    def visit(self, node):
        #print("IdxAssign")
        exp = node.expression.accept(self)
        if type(node.expression) is AST.Id:
            exp = self._get_id_value_from_memory(exp)
        if not self.globalMemory.set(node.ID, exp):
            self.globalMemory.insert(node.ID, exp)

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.Id)
    def visit(self, node):
        return node.name

    @when(AST.String)
    def visit(self, node):
        return node.string

    @when(AST.BinExpr)
    def visit(self, node):
        #print("binexpr")
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        if type(node.left) is AST.Id:
            r1 = self._get_id_value_from_memory(r1)
        if type(node.right) is AST.Id:
            r2 = self._get_id_value_from_memory(r2)
        return operators[node.op](r1, r2)

    @when(AST.Error)
    def visit(self, node):
        pass

    @when(AST.IdxOneDimensionTableAssign)
    def visit(self, node):
        #print("IdxOneDimensionTableAssign")
        table = self.globalMemory.get(node.ID)
        exp1 = node.expression1.accept(self)
        if type(node.expression1) is AST.Id:
            exp1 = self._get_id_value_from_memory(exp1)
        exp2 = node.expression2.accept(self)
        if type(node.expression2) is AST.Id:
            exp2 = self._get_id_value_from_memory(exp2)
        table[exp1] = exp2
        self.globalMemory.set(node.ID, table)

    @when(AST.IdxTwoDimensionTableAssign)
    def visit(self, node):
        #print("IdxTwoDimensionTableAssign")
        table = self.globalMemory.get(node.ID)
        exp1 = node.expression1.accept(self)
        if type(node.expression1) is AST.Id:
            exp1 = self._get_id_value_from_memory(exp1)
        exp2 = node.expression2.accept(self)
        if type(node.expression2) is AST.Id:
            exp2 = self._get_id_value_from_memory(exp2)
        exp3 = node.expression3.accept(self)
        if type(node.expression3) is AST.Id:
            exp3 = self._get_id_value_from_memory(exp3)
        table[exp1][exp2] = exp3
        self.globalMemory.set(node.ID, table)

    @when(AST.IdxTwoDimensionTableAssignBySlicing)
    def visit(self, node):
        #print("IdxTwoDimensionTableAssignBySlicing")
        table = self.globalMemory.get(node.ID)
        exp1 = node.expression1.accept(self)
        if type(node.expression1) is AST.Id:
            exp1 = self._get_id_value_from_memory(exp1)
        exp2 = node.expression2.accept(self)
        if type(node.expression2) is AST.Id:
            exp2 = self._get_id_value_from_memory(exp2)
        exp3 = node.expression3.accept(self)
        if type(node.expression3) is AST.Id:
            exp3 = self._get_id_value_from_memory(exp3)
        exp4 = node.expression4.accept(self)
        if type(node.expression4) is AST.Id:
            exp4 = self._get_id_value_from_memory(exp4)
        exp5 = node.expression5.accept(self)
        if type(node.expression5) is AST.Id:
            exp5 = self._get_id_value_from_memory(exp5)
        for i in range(exp1, exp2):
            for j in range(exp3, exp4):
                table[i][j] = exp5
        self.globalMemory.set(node.ID, table)

    @when(AST.IdxOpAssign)
    def visit(self, node):
        #print("IdxOpAssign")
        value = self.globalMemory.get(node.ID)
        exp = node.expression.accept(self)
        if type(node.expression) is AST.Id:
            exp = self._get_id_value_from_memory(exp)
        value = operators[node.op](value, exp)
        self.globalMemory.set(node.ID, value)

    @when(AST.Zeros)
    def visit(self, node):
        exp = node.expression.accept(self)
        if type(node.expression) is AST.Id:
            exp = self._get_id_value_from_memory(exp)
        return [[0 for _ in range(exp)] for j in range(exp)]

    @when(AST.Ones)
    def visit(self, node):
        exp = node.expression.accept(self)
        if type(node.expression) is AST.Id:
            exp = self._get_id_value_from_memory(exp)
        return [[1 for _ in range(exp)] for j in range(exp)]

    @when(AST.Eye)
    def visit(self, node):
        exp = node.expression.accept(self)
        if type(node.expression) is AST.Id:
            exp = self._get_id_value_from_memory(exp)
        return [[1 if i == j else 0 for i in range(exp)] for j in range(exp)]

    @when(AST.Zeros2)
    def visit(self, node):
        exp1 = node.expression1.accept(self)
        if type(node.expression1) is AST.Id:
            exp1 = self._get_id_value_from_memory(exp1)
        exp2 = node.expression2.accept(self)
        if type(node.expression2) is AST.Id:
            exp2 = self._get_id_value_from_memory(exp2)
        return [[0 for _ in range(exp2)] for j in range(exp1)]

    @when(AST.Ones2)
    def visit(self, node):
        exp1 = node.expression1.accept(self)
        if type(node.expression1) is AST.Id:
            exp1 = self._get_id_value_from_memory(exp1)
        exp2 = node.expression2.accept(self)
        if type(node.expression2) is AST.Id:
            exp2 = self._get_id_value_from_memory(exp2)
        return [[1 for _ in range(exp2)] for j in range(exp1)]

    @when(AST.Eye2)
    def visit(self, node):
        exp1 = node.expression1.accept(self)
        if type(node.expression1) is AST.Id:
            exp1 = self._get_id_value_from_memory(exp1)
        exp2 = node.expression2.accept(self)
        if type(node.expression2) is AST.Id:
            exp2 = self._get_id_value_from_memory(exp2)
        return [[1 if i == j else 0 for i in range(exp2)] for j in range(exp1)]

    @when(AST.Matrix)
    def visit(self, node):
        #print("Matrix")
        if type(node.matrixInside) is AST.MatrixInside:
            return node.matrixInside.accept(self)
        else:
            return [node.matrixInside.accept(self)]

    @when(AST.MatrixInside)
    def visit(self, node):
        #print("MatrixInside")
        tab = node.table.accept(self)
        if type(node.table) is AST.Id:
            tab = self._get_id_value_from_memory(tab)
        matrix = [tab]
        if type(node.matrixInside) is not AST.MatrixInside:
            matrix.append(node.matrixInside.accept(self))
        else:
            matrix.extend(node.matrixInside.accept(self))
        return matrix

    @when(AST.Table)
    def visit(self, node):
        #print("table")
        if type(node.values) is AST.Values:
            return node.values.accept(self)
        else:
            return [node.values.accept(self)]

    @when(AST.Values)
    def visit(self, node):
        #print("Values")
        exp = node.expression.accept(self)
        if type(node.expression) is AST.Id:
            exp = self._get_id_value_from_memory(exp)
        table = [exp]
        if type(node.values) is AST.Values:
            table.extend(node.values.accept(self))
        else:
            exp = node.values.accept(self)
            if type(node.values) is AST.Id:
                exp = self._get_id_value_from_memory(exp)
            table.append(exp)
        return table

    @when(AST.MatrixExpression)
    def visit(self, node):
        #print("matrixExpression")
        exp = node.expression1.accept(self)
        if type(node.expression1) is AST.Id:
            exp = self._get_id_value_from_memory(exp)
        op = node.op
        matrixExp = node.matrixExpression2.accept(self)
        if type(node.matrixExpression2) is AST.Id:
            matrixExp = self._get_id_value_from_memory(matrixExp)
        if type(exp[0]) is list:
            tmp = [[0 for _ in range(len(exp[i]))] for i in range(len(exp))]
            if op == ".+":
                for i in range(len(exp)):
                    for j in range(len(exp[i])):
                        tmp[i][j] = exp[i][j] + matrixExp[i][j]
            elif op == ".-":
                for i in range(len(exp)):
                    for j in range(len(exp[i])):
                        tmp[i][j] = exp[i][j] - matrixExp[i][j]
            elif op == ".*":
                for i in range(len(exp)):
                    for j in range(len(exp[i])):
                        tmp[i][j] = exp[i][j] * matrixExp[i][j]
            elif op == "./":
                for i in range(len(exp)):
                    for j in range(len(exp[i])):
                        tmp[i][j] = exp[i][j] / matrixExp[i][j]
        else:
            tmp = [0 for _ in range(len(exp))]
            if op == ".+":
                for i in range(len(exp)):
                        tmp[i] = exp[i] + matrixExp[i]
            elif op == ".-":
                for i in range(len(exp)):
                        tmp[i] = exp[i] - matrixExp[i]
            elif op == ".*":
                for i in range(len(exp)):
                        tmp[i] = exp[i] * matrixExp[i]
            elif op == "./":
                for i in range(len(exp)):
                        tmp[i] = exp[i] / matrixExp[i]
        return tmp

    @when(AST.Transpose)
    def visit(self, node):
        #print("Transpose")
        tab = node.expression.accept(self)
        if type(node.expression) is AST.Id:
            tab = self._get_id_value_from_memory(tab)
        new_tab = [[tab[i][j] for i in range(len(tab))] for j in range(len(tab[0]))]
        return new_tab

    @when(AST.IfxIf)
    def visit(self, node):
        #print("IfxIf")
        cond = node.condition.accept(self)
        if cond:
            node.line.accept(self)

    @when(AST.IfxIfElse)
    def visit(self, node):
        #print("IfxIfElse")
        cond = node.condition.accept(self)
        if cond:
            node.line1.accept(self)
        else:
            node.line2.accept(self)

    @when(AST.Condition)
    def visit(self, node):
        #print("Condition")
        exp1 = node.expression1.accept(self)
        exp2 = node.expression2.accept(self)
        if type(node.expression1) is AST.Id:
            exp1 = self._get_id_value_from_memory(exp1)
        if type(node.expression2) is AST.Id:
            exp2 = self._get_id_value_from_memory(exp2)
        return operators[node.op](exp1, exp2)

    @when(AST.Return)
    def visit(self, node):
        #print("Return")
        exp = node.expression.accept(self)
        if type(node.expression) is AST.Id:
            exp = self._get_id_value_from_memory(exp)
        return exp

    @when(AST.While)
    def visit(self, node):
        #print("While")
        cond = node.condition.accept(self)
        while cond:
            try:
                node.line.accept(self)
                cond = node.condition.accept(self)
            except ContinueException:
                cond = node.condition.accept(self)
            except BreakException:
                return
    @when(AST.For)
    def visit(self, node):
        #print("For")
        exp1 = node.expression1.accept(self)
        exp2 = node.expression2.accept(self)
        if type(node.expression1) is AST.Id:
            exp1 = self._get_id_value_from_memory(exp1)
        if type(node.expression2) is AST.Id:
            exp2 = self._get_id_value_from_memory(exp2)
        self.globalMemory.insert(node.ID, exp1)
        for i in range(exp1, exp2):
            self.globalMemory.set(node.ID, i)
            try:
                node.line.accept(self)
            except ContinueException:
                continue
            except BreakException:
                return

    @when(AST.Negation)
    def visit(self, node):
        #print("Negation")
        exp = node.expression.accept(self)
        if type(node.expression) is AST.Id:
            exp = self._get_id_value_from_memory(exp)
        return -exp

    @when(AST.Break)
    def visit(self, node):
        #print("Break")
        raise BreakException

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException

    @when(AST.Print)
    def visit(self, node):
        #print("print")
        if type(node.printMany) is not AST.PrintMany and type(node.printMany) is not AST.PrintManyTable \
                and type(node.printMany) is not AST.PrintTable:
            value = node.printMany.accept(self)
            if type(node.printMany) is AST.Id:
                value = self._get_id_value_from_memory(value)
            print(value)
        else:
            node.printMany.accept(self)

    @when(AST.PrintMany)
    def visit(self, node):
        #print("printOne")
        value = node.printOne.accept(self)
        if type(node.printOne) is AST.Id:
            value = self._get_id_value_from_memory(value)
        print(value)
        if type(node.printMany) is not AST.PrintMany and type(node.printMany) is not AST.PrintManyTable \
                and type(node.printMany) is not AST.PrintTable:
            value = node.printMany.accept(self)
            if type(node.printMany) is AST.Id:
                value = self._get_id_value_from_memory(value)
            print(value)
        else:
            node.printMany.accept(self)

    @when(AST.PrintManyTable)
    def visit(self, node):
        #print("printOneTable")
        value = self._get_id_value_from_memory(node.printID)
        indexes = node.printTable.accept(self)
        if len(indexes) == 1:
            print(value[indexes[0]])
        elif len(indexes) == 2:
            print(value[indexes[0]][indexes[1]])
        if type(node.printMany) is not AST.PrintMany and type(node.printMany) is not AST.PrintManyTable \
                and type(node.printMany) is not AST.PrintTable:
            value = node.printMany.accept(self)
            if type(node.printMany) is AST.Id:
                value = self._get_id_value_from_memory(value)
            print(value)
        else:
            node.printMany.accept(self)

    @when(AST.PrintTriangle)
    def visit(self, node):
        #print("PrintTriangle")
        if type(node.expression) is str:
            exp = self._get_id_value_from_memory(node.expression)
        else:
            exp = node.expression.accept(self)
        if type(node.expression) is AST.Id:
            exp = self._get_id_value_from_memory(exp)
        print(node.string[1:len(node.string) - 1] * exp)


    @when(AST.PrintTable)
    def visit(self, node):
        #print("printTable")
        value = self._get_id_value_from_memory(node.printID)
        indexes = node.printTable.accept(self)
        if len(indexes) == 1:
            print(value[indexes[0]])
        elif len(indexes) == 2:
            print(value[indexes[0]][indexes[1]])

    def _get_id_value_from_memory(self, ID):
        value = self.globalMemory.get(ID)
        return value
