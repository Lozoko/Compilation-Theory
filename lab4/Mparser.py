from lab4.scanner import Scanner
import AST
import TreePrinter


class Mparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()
        self.error_occured = False

    tokens = Scanner.tokens

    precedence = (
        ('nonassoc', 'IFS'),
        ("nonassoc", 'ELSE'),
        ('right', '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
        ('left', 'UNEQUAL', 'EQUAL'),
        ('left', '<', '>', 'LESSEQUAL', 'GREATEREQUAL'),
        ("left", '+', '-'),
        ("left", 'DOTADD', 'DOTSUB'),
        ("left", '*', '/'),
        ("left", 'DOTMUL', 'DOTDIV')

    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        else:
            print("Unexpected end of input")

    # dict for ids
    IDs = {}
    # var for return
    return_value = None

    def p_start(self, p):
        """start : LINE"""
        p[0] = AST.Start(p[1])
        # p[0].printTree()
        p[0].line_no = self.scanner.lexer.lineno

        #poczatkowa tablica

    def p_line(self, p):
        """LINE : IDX ';' LINE
                | IFX LINE
                | WHILEX LINE
                | FORX LINE
                | RETURNX ';' LINE
                | PRINTX ';' LINE
                | BLOCK LINE
                | EMPTY"""
        if len(p) == 4:
            p[0] = AST.Lines(p[1], p[3])
        elif len(p) == 3:
            p[0] = AST.Lines(p[1], p[2])
            # tworzymy nowe tablice
        else:
            p[0] = AST.Stop()
        p[0].line_no = self.scanner.lexer.lineno

    def p_oneline(self, p):
        """ONELINE : IDX ';'
                    | IFX
                    | WHILEX
                    | FORX
                    | RETURNX ';'
                    | PRINTX ';' """
        p[0] = p[1]
        # if len(p)==2:
        #     # tworzymy nowe tablice
        p[0].line_no = self.scanner.lexer.lineno


    def p_block(self, p):
        """BLOCK : '{' LINE '}' """
        p[0] = p[2]
        # tworzymy nowe tablice
        p[0].line_no = self.scanner.lexer.lineno


    def p_empty(self, p):
        """EMPTY :"""

    # idx
    def p_idx_assign(self, p):
        """IDX : ID '=' EXPRESSION
               | ID '=' MATRIX
               | ID '=' TABLE
               | ID '[' EXPRESSION ']' '=' EXPRESSION
               | ID '[' EXPRESSION ',' EXPRESSION ']' '=' EXPRESSION"""
        if len(p) == 4:
            p[0] = AST.IdxAssign(p[1], p[3])
        elif len(p) == 7:
            p[0] = AST.IdxOneDimensionTableAssign(p[1], p[3], p[6])
        elif len(p) == 9:
            p[0] = AST.IdxTwoDimensionTableAssign(p[1], p[3], p[5], p[8])
        p[0].line_no = self.scanner.lexer.lineno

    def p_idx_opassign(self, p):
        """IDX : ID ADDASSIGN EXPRESSION
               | ID ADDASSIGN MATRIX
               | ID ADDASSIGN TABLE
               | ID '[' EXPRESSION ']' ADDASSIGN EXPRESSION
               | ID '[' EXPRESSION ',' EXPRESSION ']' ADDASSIGN EXPRESSION
               | ID SUBASSIGN EXPRESSION
               | ID SUBASSIGN MATRIX
               | ID SUBASSIGN TABLE
               | ID '[' EXPRESSION ']' SUBASSIGN EXPRESSION
               | ID '[' EXPRESSION ',' EXPRESSION ']' SUBASSIGN EXPRESSION
               | ID MULASSIGN EXPRESSION
               | ID MULASSIGN MATRIX
               | ID MULASSIGN TABLE
               | ID '[' EXPRESSION ']' MULASSIGN EXPRESSION
               | ID '[' EXPRESSION ',' EXPRESSION ']' MULASSIGN EXPRESSION
               | ID DIVASSIGN EXPRESSION
               | ID DIVASSIGN MATRIX
               | ID DIVASSIGN TABLE
               | ID '[' EXPRESSION ']' DIVASSIGN EXPRESSION
               | ID '[' EXPRESSION ',' EXPRESSION ']' DIVASSIGN EXPRESSION """

        # if p[2] == "ADDASSIGN": IDs[p[1]] += p[3]
        # elif p[2] == "SUBASSIGN": IDs[p[1]] -= p[3]
        # elif p[2] == "MULASSIGN": IDs[p[1]] *= p[3]
        # elif p[2] == "DIVASSIGN": IDs[p[1]] /= p[3]
        p[0] = AST.IdxOpAssign(p[1], p[2], p[3])
        p[0].line_no = self.scanner.lexer.lineno

    # MACIERZE
    def p_zerosx(self, p):
        """ZEROSX : ZEROS '(' EXPRESSION ')'"""
        # p[0] = zeros(p[3])
        p[0] = AST.Zeros(p[3])
        p[0].line_no = self.scanner.lexer.lineno

    def p_onesx(self, p):
        """ONESX : ONES '(' EXPRESSION ')'"""
        # p[0] = ones(p[3])
        p[0] = AST.Ones(p[3])
        p[0].line_no = self.scanner.lexer.lineno

    def p_eyex(self, p):
        """EYEX : EYE '(' EXPRESSION ')'"""
        # p[0] = eye(p[3])
        p[0] = AST.Eye(p[3])
        p[0].line_no = self.scanner.lexer.lineno

    def p_matrix(self, p):
        """MATRIX : '[' MATRIXINSIDE ']'
                    | MATRIXEXPR
                    | ZEROSX
                    | ONESX
                    | EYEX"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST.Matrix(p[2])
        p[0].line_no = self.scanner.lexer.lineno

    def p_matrixinside(self, p):
        """MATRIXINSIDE : TABLE ',' MATRIXINSIDE
                        | TABLE"""
        if len(p) == 4:
            p[0] = AST.MatrixInside(p[1], p[3])
        elif len(p) == 2:
            p[0] = p[1]
        p[0].line_no = self.scanner.lexer.lineno

    def p_table(self, p):
        """TABLE : '[' VALUES ']'"""
        p[0] = AST.Table(p[2])
        p[0].line_no = self.scanner.lexer.lineno

    def p_values(self, p):
        """VALUES :  EXPRESSION ',' VALUES
                | EXPRESSION"""
        if len(p) == 4:
            p[0] = AST.Values(p[1], p[3])
        elif len(p) == 2:
            p[0] = p[1]
        p[0].line_no = self.scanner.lexer.lineno

    # def zeros(self, dim):
    #     return [[0 for _ in range(dim)] for _ in range(dim)]
    #
    #
    # def ones(self, dim):
    #     return [[1 for _ in range(dim)] for _ in range(dim)]
    #
    #
    # def eye(self, dim):
    #     return [[1 if x==y else 0 for x in range(dim)]for y in range(dim)]

    def p_matrixop(self, p):
        """MATRIXEXPR : EXPRESSION DOTADD MATRIXEXPR
                   | EXPRESSION DOTSUB MATRIXEXPR
                   | EXPRESSION DOTMUL MATRIXEXPR
                   | EXPRESSION DOTDIV MATRIXEXPR
                   | EXPRESSION "'"
                   | EMPTY """

        if len(p) == 4:
            p[0] = AST.MatrixExpression(p[1], p[2], p[3])
        elif len(p) == 3:
            p[0] = AST.Transpose(p[1])
        elif len(p) == 2:
            p[0] = p[1]
        p[0].line_no = self.scanner.lexer.lineno

    # IF
    def p_ifx_if(self, p):
        """IFX :    IF '(' CONDITION ')' ONELINE %prec IFS
                |   IF '(' CONDITION ')' BLOCK %prec IFS
                |   IF '(' CONDITION ')' ONELINE ELSE ONELINE
                |   IF '(' CONDITION ')' ONELINE ELSE BLOCK
                |   IF '(' CONDITION ')' BLOCK ELSE ONELINE
                |   IF '(' CONDITION ')' BLOCK ELSE BLOCK """
        if len(p) == 6:
            p[0] = AST.IfxIf(p[3], p[5])
            # tworzymy nowa tablice
        elif len(p) == 8:
            p[0] = AST.IfxIfElse(p[3], p[5], p[7])
            # tworzymy 2 nowe tablice if i else
        p[0].line_no = self.scanner.lexer.lineno

    # LOOP (do lini dochodzą brake, continue i loopif)
    def p_loopline(self, p):
        """LOOPLINE : IDX ';' LOOPLINE
                    | WHILEX LOOPLINE
                    | FORX LOOPLINE
                    | RETURNX ';' LOOPLINE
                    | PRINTX ';' LOOPLINE
                    | LOOPBLOCK LOOPLINE
                    | EMPTY
                    | LOOPIFX LOOPLINE
                    | BREAKX ';' LOOPLINE
                    | CONTINUEX ';' LOOPLINE"""
        if len(p) == 4:
            p[0] = AST.Lines(p[1], p[3])
        elif len(p) == 3:
            p[0] = AST.Lines(p[1], p[2])
            # tworzymy nowe tablice
        else:
            p[0] = AST.Stop()
        p[0].line_no = self.scanner.lexer.lineno

    def p_oneloopline(self, p):
        """ONELOOPLINE : IDX ';'
                        | WHILEX
                        | FORX
                        | RETURNX ';'
                        | PRINTX ';'
                        | LOOPIFX
                        | BREAKX ';'
                        | CONTINUEX ';' """
        p[0] = p[1]
        # if len(p)==2:
        #     # tworzymy nowe tablice
        p[0].line_no = self.scanner.lexer.lineno

    def p_breakx(self, p):
        """BREAKX : BREAK """
        p[0] = AST.Break()
        p[0].line_no = self.scanner.lexer.lineno

    def p_continuex(self, p):
        """CONTINUEX : CONTINUE """
        p[0] = AST.Continue()
        p[0].line_no = self.scanner.lexer.lineno

    def p_loopblock(self, p):
        """LOOPBLOCK : '{' LOOPLINE '}'"""
        p[0] = p[2]
        # tworzymy nowe tablice
        p[0].line_no = self.scanner.lexer.lineno

    def p_loopifx_if(self, p):
        """LOOPIFX :    IF '(' CONDITION ')' ONELOOPLINE %prec IFS
                    |   IF '(' CONDITION ')' LOOPBLOCK %prec IFS
                    |   IF '(' CONDITION ')' ONELOOPLINE ELSE ONELOOPLINE
                    |   IF '(' CONDITION ')' ONELOOPLINE ELSE LOOPBLOCK
                    |   IF '(' CONDITION ')' LOOPBLOCK ELSE ONELOOPLINE
                    |   IF '(' CONDITION ')' LOOPBLOCK ELSE LOOPBLOCK """
        if len(p) == 6:
            p[0] = AST.IfxIf(p[3], p[5])
            # tworzymy nowa tablice
        elif len(p) == 8:
            p[0] = AST.IfxIfElse(p[3], p[5], p[7])
            # tworzymy 2 nowe tablice
        p[0].line_no = self.scanner.lexer.lineno

    # WHILE
    def p_whilex(self, p):
        """WHILEX : WHILE '(' CONDITION ')' ONELOOPLINE
                    | WHILE '(' CONDITION ')' LOOPBLOCK"""
        p[0] = AST.While(p[3], p[5])
        # tworzymy nowe tablice
        p[0].line_no = self.scanner.lexer.lineno

    # FOR
    def p_forx(self, p):
        """FORX : FOR ID '=' EXPRESSION ':' EXPRESSION ONELOOPLINE
                | FOR ID '=' EXPRESSION ':' EXPRESSION LOOPBLOCK"""
        p[0] = AST.For(p[2], p[4], p[6], p[7])
        # tworzymy nowe tablice
        p[0].line_no = self.scanner.lexer.lineno

    # C ONDITION
    def p_condition(self, p):
        """CONDITION : EXPRESSION EQUAL EXPRESSION
                        | EXPRESSION UNEQUAL EXPRESSION
                        | EXPRESSION LESSEQUAL EXPRESSION
                        | EXPRESSION GREATEREQUAL EXPRESSION
                        | EXPRESSION '>' EXPRESSION
                        | EXPRESSION '<' EXPRESSION """
        p[0] = AST.Condition(p[1], p[2], p[3])
        p[0].line_no = self.scanner.lexer.lineno

    # PRINT
    def p_printx(self, p):
        """PRINTX : PRINT PRINTMANY """
        p[0] = AST.Print(p[2])
        p[0].line_no = self.scanner.lexer.lineno

    def p_printmany(self, p):
        """PRINTMANY : STRINGX ',' PRINTMANY
                    |  EXPRESSION ',' PRINTMANY
                    |  STRINGX
                    |  EXPRESSION """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST.PrintMany(p[1], p[3])
        p[0].line_no = self.scanner.lexer.lineno

    def p_stringx(self, p):
        """STRINGX :  STRING """
        p[0] = AST.String(p[1])
        p[0].line_no = self.scanner.lexer.lineno

    # return
    def p_returnx_return(self, p):
        """RETURNX : RETURN EXPRESSION """
        global return_value
        return_value = p[2]
        p[0] = AST.Return(p[2])
        p[0].line_no = self.scanner.lexer.lineno

    # expression
    def p_expression_number(self, p):
        """EXPRESSION : NUMBER"""
        p[0] = AST.IntNum(p[1])
        p[0].line_no = self.scanner.lexer.lineno

    def p_expression_float(self, p):
        """EXPRESSION : FLOATNUMBER"""
        p[0] = AST.FloatNum(p[1])
        p[0].line_no = self.scanner.lexer.lineno

    def p_expression_id(self, p):
        """EXPRESSION : ID"""
        p[0] = AST.Id(p[1])
        p[0].line_no = self.scanner.lexer.lineno

    def p_expression_sum(self, p):
        """EXPRESSION : EXPRESSION '+' EXPRESSION
                      | EXPRESSION '-' EXPRESSION"""
        p[0] = AST.BinExpr(p[2], p[1], p[3])
        p[0].line_no = self.scanner.lexer.lineno

    def p_expression_mul(self, p):
        """EXPRESSION : EXPRESSION '*' EXPRESSION
                      | EXPRESSION '/' EXPRESSION"""
        p[0] = AST.BinExpr(p[2], p[1], p[3])
        p[0].line_no = self.scanner.lexer.lineno

    def p_expression_group(self, p):
        """EXPRESSION : '(' EXPRESSION ')'"""
        p[0] = p[2]
        p[0].line_no = self.scanner.lexer.lineno

    def p_expression_unarynegation(self, p):
        """EXPRESSION : '-' EXPRESSION"""
        p[0] = AST.Negation(p[2])
        p[0].line_no = self.scanner.lexer.lineno
