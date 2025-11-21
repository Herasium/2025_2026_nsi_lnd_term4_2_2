class Node():
    def __init__(self, type, id):
        self.type = type
        self.id = id

class Start(Node):
    def __init__(self):
        self.inputs = 0
        self.outputs = 1

class And(Node):
    def __init__(self):
        self.inputs = 2
        self.outputs = 1

class Or(Node):
    def __init__(self):
        self.inputs = 2
        self.outputs = 1

class Xor(Node):
    def __init__(self):
        self.inputs = 2
        self.outputs = 1

class Nand(Node):
    def __init__(self):
        self.inputs = 2
        self.outputs = 1

class Nxor(Node):
    def __init__(self):
        self.inputs = 2
        self.outputs = 1

class End(Node):
    def __init__(self):
        self.inputs = 1
        self.outputs = 0

class ImpA(Node):
    def __init__(self):
        self.inputs = 2
        self.outputs = 1

class ImpB(Node):
    def __init__(self):
        self.inputs = 2
        self.outputs = 1