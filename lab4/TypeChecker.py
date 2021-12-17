#!/usr/bin/python
from lab4 import AST
from SymbolTable import VariableSymbol
from SymbolTable import SymbolTable
from SymbolTable import Symbol
from collections import defaultdict

type_table = defaultdict(lambda: None)
arithm_ops = ['+', '-', '*', '/']
comp_ops = ['==', '!=', '>', '<', '<=', '>=']
ass_ops = ['=', '+=', '-=', '*=', '/=']
mat_ops = ['.+', '.-', '.*', './']

for op in arithm_ops + comp_ops + ass_ops + mat_ops:
    type_table[op] = defaultdict(lambda: None)
    for type in ['int', 'float', 'string', 'matrix', 'table']:
        type_table[op][type] = defaultdict(lambda: None)

for op in arithm_ops + ass_ops:
    type_table[op]['int']['int'] = 'int'
    type_table[op]['int']['float'] = 'float'
    type_table[op]['float']['int'] = 'float'
    type_table[op]['float']['float'] = 'float'

type_table['+']['string']['string'] = 'string'
type_table['*']['string']['int'] = 'string'
type_table['=']['string']['string'] = 'string'

type_table['+=']['string']['string'] = 'string'
type_table['*=']['string']['int'] = 'string'

for op in mat_ops:
    type_table[op]['matrix']['matrix'] = 'matrix'

for comp_op in comp_ops:
    type_table[comp_op]['int']['int'] = 'int'
    type_table[comp_op]['int']['float'] = 'int'
    type_table[comp_op]['float']['int'] = 'int'
    type_table[comp_op]['float']['float'] = 'int'
    type_table[comp_op]['string']['string'] = 'int'
    type_table[comp_op]['matrix']['matrix'] = 'int'



def calculate(op, v1, v2):
    if v1 is None or v2 is None:
        return None
    if op=='+':
        return v1+v2
    elif op=='-':
        return v1-v2
    elif op=='*':
        return v1*v2
    elif op == '/':
        return v1/v2
    else:
        print(f"Unknown operator {op}")
        return None

def evaluate(op,v1,v2):
    if v1 is None or v2 is None:
        return None
    if op == '==':
        return 1 if v1 == v2 else 0
    elif op=='!=':
        return 1 if v1!=v2 else 0
    elif op=='>':
        return 1 if v1>v2 else 0
    elif op=='<':
        return 1 if v1<v2 else 0
    elif op=='>=':
        return 1 if v1>=v2 else 0
    elif op == '<=':
        return 1 if v1<=v2 else 0
    else:
        print(f"Unknown operator {op}")
        return None

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):
    tab = SymbolTable(None, "main_scope")

    def find_var(self,tab, id):
        var = tab.get(id)
        if var is not None:
            return var
        elif tab.getParentScope() is not None:
            return self.find_var(tab.getParentScope(), id)
        else:
            return None

    def visit_Start(self, node):
        self.visit(node.lines)

    def visit_Stop(self, node):
        pass

    def visit_Lines(self,node):
        self.visit(node.line)
        self.visit(node.nextLine)

    def visit_IdxAssign(self, node):
        tmp = self.visit(node.expression)
        if tmp is None:
            return
        type, value = tmp[0], tmp[1]
####
        if type is None or value is None:
            print(f"Line ({node.line_no}): Unknown variable")

        self.tab.put(node.ID, VariableSymbol(node.ID, type, value))

    def visit_IntNum(self, node):
        return 'int', node.value

    def visit_FloatNum(self, node):
        return 'float', node.value

    def visit_Id(self, node):
        var = self.find_var(self.tab.current_table, node.name)
        if var == None:
            print(f"Line ({node.line_no}): {node.name} is undeclared")
            return None, None
        else:
            return var.type, var.value

    def visit_String(self, node):
        return 'string', node.value

    def visit_BinExpr(self, node):
        #                                   # alternative usage,
        #                                   # requires definition of accept method in class Node
        # type1 = self.visit(node.left)     # type1 = node.left.accept(self)
        # type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        # op    = node.op
        # # ...
        # #
        type1, value1 = self.visit(node.left)
        type2, value2 = self.visit(node.right)
        op = node.op
        type = type_table[op][type1][type2]
        if type is None:
            print(f"Line ({node.line_no}): Incompatible types: {type1} {op} {type2} is wrong")
            return None, None
        value = calculate(op, value1, value2)
        return type, value

    def visit_Error(self, node):
        pass

    def visit_IdxOneDimensionTableAssign(self, node):
        error = False
        var = self.find_var(self.tab.current_table, node.ID)
        if var is None:
            return
        type, value = var.type, var.value
        if type != 'table':
            print(f"Line ({node.line_no}): {node.ID} is not a table")
            return
        type1, value1 = self.visit(node.expression1)
        if type1 != 'int':
            print(f"Line ({node.line_no}): index must be an integer")
            error = True
        if value1 is None:
            error = True
        elif value1 > len(value):
            print(f"Line ({node.line_no}): index out of range")
            error = True
        type2, value2 = self.visit(node.expression2)
        if type2 != value[0].type:
            print(f"Line ({node.line_no}): incorrect types {type2}, {value[0].type}")
        if value2 is None:
            error = True

        if not error:
            value[value1] = VariableSymbol(value1, type2, value2)
            self.tab.put(node.ID, VariableSymbol(node.ID, type, value))

    def visit_IdxTwoDimensionTableAssign(self, node):
        error = False
        var = self.find_var(self.tab.current_table, node.ID)
        if var is None:
            return
        type, value = var.type, var.value
        if type != 'matrix':
            print(f"Line ({node.line_no}): {node.ID} is not a matrix")
            return
        type1, value1 = self.visit(node.expression1)
        if type1 != 'int':
            print(f"Line ({node.line_no}): index must be an integer")
            error = True
        if value1 is None:
            error = True
        elif value1 > len(value):
            print(f"Line ({node.line_no}): index out of range")
            error = True

        type2, value2 = self.visit(node.expression2)
        if type2 != 'int':
            print(f"Line ({node.line_no}): index must be an integer")
            error = True
        if value2 is None:
            error = True
        elif value2 > len(value[value1].value):
            print(f"Line ({node.line_no}): index out of range")
            error = True

        type3, value3 = self.visit(node.expression3)
        # if type3 != value[0].value[0].type:
        #     print(f"incorrect types {type3}, {value[0].value[0].type}")
        #     error = True
        if value3 is None:
            error = True

        if not error:
            value[value1].value[value2] = VariableSymbol(value2, type3, value3)
            self.tab.put(node.ID, VariableSymbol(node.ID, type, value))

    def visit_IdxOpAssign(self, node):
        var = self.find_var(self.tab.current_table, node.ID)
        if var is None:
            print(f"Line ({node.line_no}): {node.ID} is undeclared")
            return
        type1, value1 = var.type, var.value
        if type1 is None or value1 is None:
            return

        type2, value2 = self.visit(node.expression3)
        if value2 is None:
            print(f"Line ({node.line_no}): Unknown variable")
            return

        type = type_table[op][type1][type2]
        if type is None:
            print(f"Line ({node.line_no}): Incompatible types: {type1} {op} {type2} is wrong")
            return



        value = calculate(op, value1, value2)

        self.tab.put(node.ID, VariableSymbol(node.ID, type, value))

    def visit_Zeros(self, node):
        type, value = self.visit(node.expression)
        if type != 'int':
            print(f"Line ({node.line_no}): Wrong type: {type}, should be 'int'")
            return None
        if value<1:
            print(f"Line ({node.line_no}): Matrix size should be greater then 0")
            return None
        return 'matrix', [VariableSymbol(j, 'table', [VariableSymbol(i, 'int', 0) for i in range(value)])for j in range(value)]

    def visit_Ones(self, node):
        type, value = self.visit(node.expression)
        if type != 'int':
            print(f"Line ({node.line_no}): Wrong type: {type}, should be 'int'")
            return None
        if value<1:
            print(f"Line ({node.line_no}):Matrix size should be greater then 0")
            return None
        return 'matrix', [VariableSymbol(j, 'table', [VariableSymbol(i, 'int', 1) for i in range(value)])for j in range(value)]

    def visit_Eye(self, node):
        type, value = self.visit(node.expression)
        if type != 'int':
            print(f"Line ({node.line_no}): Wrong type: {type}, should be 'int'")
            return None
        if value<1:
            print(f"Line ({node.line_no}): Matrix size should be greater then 0")
            return None
        return 'matrix', [VariableSymbol(j, 'table', [VariableSymbol(i, 'int', 1)if i==j else VariableSymbol(i, 'int', 0) for i in range(value)])for j in range(value)]

    tmp_matrix = []
    def visit_Matrix(self, node):
        self.visit(node.matrixInside)
        res = self.tmp_matrix[:]
        self.tmp_matrix = []
        return 'matrix', res

    tmp_len=0
    tmp_prev_tab = None
    def visit_MatrixInside(self, node):
        type1, value1 = self.visit(node.table)
        if type1 != 'table':
            print(f"Line ({node.line_no}): Wrong type: {type1}")
            self.tmp_matrix = []
            self.tmp_len = 0
            self.tmp_prev_tab = None
            return

        if self.tmp_len==0:
            self.tmp_len = len(value1)

        if self.tmp_len != len(value1):
            print(f"Line ({node.line_no}): Incorrect sizes of vectors")
            self.tmp_matrix = []
            self.tmp_len = 0
            self.tmp_prev_tab = None
            return
        self.tmp_matrix.append(VariableSymbol(len(self.tmp_matrix), type1, value1))
        tmp = self.visit(node.matrixInside)
        if tmp is None:
            if self.tmp_len != len(self.tmp_prev_tab[1]):
                print(f"Line ({node.line_no}): Incorrect sizes of vectors")
                self.tmp_matrix = []
                self.tmp_len = 0
                self.tmp_prev_tab = None
                return

            self.tmp_matrix.append(VariableSymbol(len(self.tmp_matrix), self.tmp_prev_tab[0], self.tmp_prev_tab[1]))
            self.tmp_len = 0
            self.tmp_prev_tab = None
            return self.tmp_matrix

        self.tmp_prev_tab = tmp

    tmp_table = []
    def visit_Table(self, node):
        self.visit(node.values)
        res = self.tmp_table[:]
        self.tmp_table = []
        return 'table', res


    tmp_prev_val = None
    def visit_Values(self, node):
        type1, value1 = self.visit(node.expression)
        if type1 is None:
            self.tmp_table = []
            self.tmp_prev_val = None
            return None

        self.tmp_table.append(VariableSymbol(len(self.tmp_table), type1, value1))
        tmp = self.visit(node.values)
        if tmp is None:
            self.tmp_table.append(VariableSymbol(len(self.tmp_table), self.tmp_prev_val[0], self.tmp_prev_val[1]))
            self.tmp_prev_val = None
            return self.tmp_table
        self.tmp_prev_val = tmp


    def visit_MatrixExpression(self, node):
        pass

    def visit_Transpose(self, node):
        tmp = self.visit(node.expression)
        if tmp is None:
            return
        type, value = tmp[0], tmp[1]
        if type!='matrix':
            print(f"Line ({node.line_no}): incorrect type")
            return

    def visit_IfxIf(self, node):
        cond = self.visit(node.condition)
        if cond==1:
            tab = SymbolTable(self.tab.current_table, "if")
            self.tab.current_table = tab

            self.visit(node.line)
            if self.tab.getParentScope() is not None:
                self.tab.current_table = self.tab.parent


    def visit_IfxIfElse(self, node):
        cond = self.visit(node.condition)
        if cond==1:
            tab = SymbolTable(self.tab.current_table, "if")
            self.tab.current_table = tab

            self.visit(node.line1)
            if self.tab.getParentScope() is not None:
                self.tab.current_table = self.tab.parent
        else:
            tab = SymbolTable(self.tab.current_table, "if")
            self.tab.current_table = tab

            self.visit(node.line2)
            if self.tab.getParentScope() is not None:
                self.tab.current_table = self.tab.parent


    def visit_Condition(self, node):
        type1, value1 = self.visit(node.expression1)
        type2, value2 = self.visit(node.expression2)
        if type1 is None or type2 is None:
            return None, None
        op = node.op
        type = type_table[op][type1][type2]
        if type is None:
            print(f"Line ({node.line_no}): Incompatible types: {type1} {op} {type2} is wrong")
            return None, None
        value = evaluate(op, value1, value2)
        return type, value

    def visit_Return(self, node):
        return self.visit(node.expression)

    def visit_While(self, node):
        type1, value1 = self.visit(node.condition)
        if type1 is None:
            return
        while value1 == 1:
            tab = SymbolTable(self.tab.current_table, "while")
            self.tab.current_table = tab

            self.visit(node.line)
            if self.tab.getParentScope() is not None:
                self.tab.current_table = self.tab.parent

    def visit_For(self, node):
        type1, value1 = self.visit(node.expression1)
        type2, value2 = self.visit(node.expression2)
        if type1 is None or type2 is None:
            return
        self.tab.put(node.ID, VariableSymbol(node.ID, type, value1))
        for node.ID in range(value1, value2):
            tab = SymbolTable(self.tab.current_table, "for")
            self.tab.current_table = tab

            self.visit(node.line)
            if self.tab.getParentScope() is not None:
                self.tab.current_table = self.tab.parent

    def visit_Negation(self, node):
        self.visit(node.expression)

    def visit_Print(self, node):
        self.visit(node.printMany)

    def visit_PrintMany(self, node):
        self.visit(node.printOne)
        self.visit(node.printMany)

    def visit_Break(self, node):
        pass

    def visit_Continue(self, node):
        pass