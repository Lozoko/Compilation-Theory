class NoMemoryOnStackException(Exception):
    pass


class VariableNotExistingException(Exception):
    pass


class ContinueException(Exception):
    pass


class BreakException(Exception):
    pass


class Memory:

    def __init__(self, name):  # memory name
        self.name = name
        self.memory = {}

    def has_key(self, name):  # variable name
        return name in self.memory

    def get(self, name):  # gets from memory current value of variable <name>
        return self.memory[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memory[name] = value


class MemoryStack:

    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.memoryStack = []
        if memory is not None:
            self.memoryStack.append(memory)

    def get(self, name):  # gets from memory stack current value of variable <name>
        if len(self.memoryStack) > 0:
            for i in range(len(self.memoryStack) - 1, -1, -1):
                if self.memoryStack[i].has_key(name):
                    return self.memoryStack[i].get(name)
        else:
            return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        if len(self.memoryStack) > 0:
            self.memoryStack[len(self.memoryStack) - 1].put(name, value)
        else:
            raise NoMemoryOnStackException

    def set(self, name, value):  # sets variable <name> to value <value>
        if len(self.memoryStack) > 0:
            for i in range(len(self.memoryStack) - 1, -1, -1):
                if self.memoryStack[i].has_key(name):
                    self.memoryStack[i].put(name, value)
                    return True
        return False

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.memoryStack.append(memory)

    def pop(self):  # pops the top memory from the stack
        self.memoryStack.pop()
