class Expr:
    """
    Classe base para todas as expressões lógicas.
    """
    pass

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
        # Preserva ordem para detectar comutatividade explicitamente
        self.args = list(args)

    def __eq__(self, other):
        # Igualdade estrita respeitando ordem dos argumentos
        return isinstance(other, And) and self.args == other.args

    def __hash__(self):
        return hash(("and", tuple(self.args)))

    def __repr__(self):
        # Representação clara com ∧ entre termos
        return "(" + " ∧ ".join(map(str, self.args)) + ")"

class Or(Expr):
    def __init__(self, *args):
        self.args = list(args)

    def __eq__(self, other):
        return isinstance(other, Or) and self.args == other.args

    def __hash__(self):
        return hash(("or", tuple(self.args)))

    def __repr__(self):
        return "(" + " ∨ ".join(map(str, self.args)) + ")"

class Implies(Expr):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return isinstance(other, Implies) and self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash(("implies", self.a, self.b))

    def __repr__(self):
        return f"({self.a} → {self.b})"

class Equivalent(Expr):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return isinstance(other, Equivalent) and self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash(("equiv", self.a, self.b))

    def __repr__(self):
        return f"({self.a} ↔ {self.b})"

class Xor(Expr):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        # Comutativo como XOR lógico
        return isinstance(other, Xor) and (
            (self.a == other.a and self.b == other.b) or
            (self.a == other.b and self.b == other.a)
        )

    def __hash__(self):
        return hash(("xor", frozenset([self.a, self.b])))

    def __repr__(self):
        return f"({self.a} ⊻ {self.b})"

class V(Expr):
    def __eq__(self, other):
        return isinstance(other, V)

    def __hash__(self):
        return hash("V")

    def __repr__(self):
        return "V"

class F(Expr):
    def __eq__(self, other):
        return isinstance(other, F)

    def __hash__(self):
        return hash("F")

    def __repr__(self):
        return "F"
