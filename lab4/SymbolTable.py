#!/usr/bin/python
from collections import defaultdict


class Symbol(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class VariableSymbol(Symbol):

    def __init__(self, name, type, value):
        super(VariableSymbol, self).__init__(name, type)
        self.value = value

    def __repr__(self):
        return f"{self.type} {self.name} = {self.value}"


class SymbolTable(object):
    current_table = None

    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = defaultdict(lambda: None)
        self.children = defaultdict(lambda: None)
        self.current_table = self

    #

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    #

    def get(self, name):  # get variable symbol or fundef from <name> entry
        return self.symbols[name]

    #

    def getParentScope(self):
        return self.parent

    #

    def pushScope(self, name):
        self.children[name] = SymbolTable(self, name)

    #

    def popScope(self):
        current_table = self.parent
    #
