class Expr:
    """
    Classe base para todas as expressões lógicas.
    """
   
class Symbol(Expr):
    def __init__(self, nome):
        self.nome = nome

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.nome == other.nome

    def __hash__(self):
        return hash(("symbol", self.nome))

    def __repr__(self):
        return self.nome

class Not(Expr):
    def __init__(self, arg):
        self.arg = arg

    def __eq__(self, other):
        return isinstance(other, Not) and self.arg == other.arg

    def __hash__(self):
        return hash(("not", self.arg))

    def __repr__(self):
        return f"¬{self.arg}"

class And(Expr):
    def __init__(self, *args):
        # Preserva ordem original para aplicação explícita de regras
        self.args = tuple(args)
        self._hash = hash(("and", self.args))

    def __eq__(self, other):
        # Igualdade sintática (preserva ordem)
        return isinstance(other, And) and self.args == other.args
    
    def __hash__(self):
        return self._hash

    def __repr__(self):
        return "(" + " ∧ ".join(map(str, self.args)) + ")"

class Or(Expr):
    def __init__(self, *args):
        # Preserva ordem original para aplicação explícita de regras
        self.args = tuple(args)
        self._hash = hash(("or", self.args))

    def __eq__(self, other):
        # Igualdade sintática (preserva ordem)
        return isinstance(other, Or) and self.args == other.args

    def __hash__(self):
        return self._hash

    def __repr__(self):
        return "(" + " ∨ ".join(map(str, self.args)) + ")"

class Implies(Expr):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self._hash = hash(("implies", a, b))

    def __eq__(self, other):
        return isinstance(other, Implies) and self.a == other.a and self.b == other.b

    def __hash__(self):
        return self._hash

    def __repr__(self):
        return f"({self.a} → {self.b})"

class Equivalent(Expr):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self._hash = hash(("equiv", a, b))

    def __eq__(self, other):
        return isinstance(other, Equivalent) and self.a == other.a and self.b == other.b

    def __hash__(self):
        return self._hash

    def __repr__(self):
        return f"({self.a} ↔ {self.b})"

class Xor(Expr):
    def __init__(self, a, b):
        # Preserva ordem original para aplicação explícita de regras
        self.a = a
        self.b = b
        self._hash = hash(("xor", a, b))

    def __eq__(self, other):
        # Igualdade sintática (preserva ordem)
        return isinstance(other, Xor) and self.a == other.a and self.b == other.b


    def __hash__(self):
        return self._hash

    def __repr__(self):
        return f"({self.a} ⊻ {self.b})"

class V(Expr):
    _instance = None
    # Singleton para representar a constante lógica V (verdade)
    # Evita criação de instâncias várias vezes
    def __new__(cls): 
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __eq__(self, other):
        return isinstance(other, V)


    def __hash__(self):
        return hash("V")

    def __repr__(self):
        return "V"

class F(Expr):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __eq__(self, other):
        return isinstance(other, F)

    def __hash__(self):
        return hash("F")

    def __repr__(self):
        return "F"