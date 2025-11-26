class Node():
    def __init__(self, type, id):
        self.type = type
        self.id = id

class Start(Node):
    def __init__(self):
        self.inputs = 0
        self.outputs = 1

class End(Node):
    def __init__(self):
        self.inputs = 1
        self.outputs = 0

class Not(Node):
    def __init__(self):
        self.inputs = 1
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

class ImpA(Node):
    def __init__(self):
        self.inputs = 2
        self.outputs = 1

class ImpB(Node):
    def __init__(self):
        self.inputs = 2
        self.outputs = 1

def comp_and(input_a, input_b):
    if input_a == input_b == True:
        return True
    else:
        return False

def comp_not(input_a):
    if input_a == False:
        return True
    else:
        return False

def comp_or(input_a, input_b):
    return comp_not(comp_and(comp_not(input_a), comp_not(input_b)))

def comp_nand(input_a, input_b):
    return comp_not(comp_and(input_a, input_b))

def comp_xor(input_a, input_b):
    return comp_and(comp_nand(input_a, input_b), comp_or(input_a, input_b))

def comp_nor(input_a, input_b):
    return comp_not(comp_or(input_a, input_b))

def comp_nxor(input_a, input_b):
    return comp_not(comp_xor(input_a, input_b))

def comp_impa(input_a, input_b):
    return comp_nor(comp_not(input_a), input_b)

def comp_impb(input_a, input_b):
    return comp_nor(input_a, comp_not(input_b))

def truth_table():
    return comp_and(a,a), comp_and(a,b), comp_and(b,a), comp_and(b,b),\
        comp_not(a), comp_not(b),\
            

a = True
b = False

print(comp_impa(a, a))