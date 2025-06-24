from .nos_logicos import Symbol, Not, And, Or, Implies, Equivalent, Xor, V, F

class RegrasLogicas:
    def __init__(self):
        self.regras = [
            ("Regra 1 (Condicional ↔ Disjunção)", self.regra_1),
            ("Regra 2 (Contraposição)", self.regra_2),
            ("Regra 3 (Bicondicional ↔ Conjunção de Condicionais)", self.regra_3),
            ("Regra 4 (Bicondicional ↔ Disjunção de Conjunções)", self.regra_4),
            ("Regra 5 (Bicondicional ↔ negação do XOR)", self.regra_5),
            ("Regra 6 (Dupla negação)", self.regra_6),
            ("Regra 7 (De Morgan para Conjunção)", self.regra_7),
            ("Regra 8 (De Morgan para Disjunção)", self.regra_8),
            ("Regra 9 (Comutatividade da Conjunção)", self.regra_9),
            ("Regra 10 (Comutatividade da Disjunção)", self.regra_10),
            ("Regra 11 (Comutatividade da Bicondicional)", self.regra_11),
            ("Regra 12 (Associatividade da Conjunção)", self.regra_12),
            ("Regra 13 (Associatividade da Disjunção)", self.regra_13),
            ("Regra 14 (Associatividade da Bicondicional)", self.regra_14),
            ("Regra 15 (Distributividade da Conjunção sobre Disjunção)", self.regra_15),
            ("Regra 16 (Distributividade da Disjunção sobre Conjunção)", self.regra_16),
            ("Regra 17 (Idempotência da Conjunção)", self.regra_17),
            ("Regra 18 (Idempotência da Disjunção)", self.regra_18),
            ("Regra 19 (Identidade da Conjunção)", self.regra_19),
            ("Regra 20 (Identidade da Disjunção)", self.regra_20),
            ("Regra 21 (Dominação da Conjunção)", self.regra_21),
            ("Regra 22 (Dominação da Disjunção)", self.regra_22),
            ("Regra 23 (Contradição da Conjunção)", self.regra_23),
            ("Regra 24 (Tautologia da Disjunção)", self.regra_24),
            ("Regra 25 (Absorção da Conjunção)", self.regra_25),
            ("Regra 26 (Absorção da Disjunção)", self.regra_26),
            ("Regra 27 (Definição do OU Exclusivo)", self.regra_27),
            ("Regra 28 (Exportação)", self.regra_28),
            ("Regra 29 (Importação)", self.regra_29),
        ]

    def regra_1(self, exp):
        """exp: p → q ≡ ¬p ∨ q (Condicional ↔ Disjunção)"""
        if isinstance(exp, Implies):
            return Or(Not(exp.a), exp.b)
        if isinstance(exp, Or) and len(exp.args) == 2:
            a, b = exp.args
            if isinstance(a, Not) and not isinstance(b, Not) and a.arg != b:
                return Implies(a.arg, b)
            if isinstance(b, Not) and not isinstance(a, Not) and b.arg != a:
                return Implies(b.arg, a)
        return exp

    def regra_2(self, exp):
        """exp: p → q ≡ ¬q → ¬p (Contraposição)"""
        if isinstance(exp, Implies):
            return Implies(Not(exp.b), Not(exp.a))
        if (isinstance(exp, Implies) and
            isinstance(exp.a, Not) and
            isinstance(exp.b, Not)):
            return Implies(exp.b.arg, exp.a.arg)
        return exp

    def regra_3(self, exp):
        """exp: p ↔ q ≡ (p → q) ∧ (q → p)"""
        if isinstance(exp, Equivalent):
            return And(Implies(exp.a, exp.b), Implies(exp.b, exp.a))
        if (isinstance(exp, And) and len(exp.args) == 2 and
            all(isinstance(arg, Implies) for arg in exp.args)):
            imp1, imp2 = exp.args
            if imp1.a == imp2.b and imp1.b == imp2.a:
                return Equivalent(imp1.a, imp1.b)
        return exp

    def regra_4(self, exp):
        """exp: p ↔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q)"""
        if isinstance(exp, Equivalent):
            return Or(And(exp.a, exp.b), And(Not(exp.a), Not(exp.b)))
        if (isinstance(exp, Or) and len(exp.args) == 2 and
            isinstance(exp.args[0], And) and isinstance(exp.args[1], And)):
            a1, a2 = exp.args[0].args
            b1, b2 = exp.args[1].args
            if ((isinstance(b1, Not) and isinstance(b2, Not) and
                 a1 == b1.arg and a2 == b2.arg) or
                (isinstance(a1, Not) and isinstance(a2, Not) and
                 b1 == a1.arg and b2 == a2.arg)):
                return Equivalent(a1, a2)
        return exp

    def regra_5(self, exp):
        """exp: p ↔ q ≡ ¬(p ⊻ q)"""
        if isinstance(exp, Equivalent):
            return Not(Xor(exp.a, exp.b))
        if isinstance(exp, Not) and isinstance(exp.arg, Xor):
            return Equivalent(exp.arg.a, exp.arg.b)
        return exp

    def regra_6(self, exp):
        """exp: ¬¬p ≡ p"""
        if isinstance(exp, Not) and isinstance(exp.arg, Not):
            return exp.arg.arg
        if not isinstance(exp, Not):
            return Not(Not(exp))
        return exp

    def regra_7(self, exp):
        """exp: ¬(p ∧ q) ≡ ¬p ∨ ¬q (De Morgan para Conjunção)"""
        if isinstance(exp, Not) and isinstance(exp.arg, And):
            return Or(*[Not(arg) for arg in exp.arg.args])
        if (isinstance(exp, Or) and
            all(isinstance(arg, Not) for arg in exp.args)):
            return Not(And(*[arg.arg for arg in exp.args]))
        return exp

    def regra_8(self, exp):
        """exp: ¬(p ∨ q) ≡ ¬p ∧ ¬q (De Morgan para Disjunção)"""
        if isinstance(exp, Not) and isinstance(exp.arg, Or):
            return And(*[Not(arg) for arg in exp.arg.args])
        if (isinstance(exp, And) and
            all(isinstance(arg, Not) for arg in exp.args)):
            return Not(Or(*[arg.arg for arg in exp.args]))
        return exp

    def regra_9(self, exp):
        """exp: p ∧ q ≡ q ∧ p (Comutatividade da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2:
            a, b = exp.args
            return And(b, a)
        return exp

    def regra_10(self, exp):
        """exp: p ∨ q ≡ q ∨ p (Comutatividade da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            a, b = exp.args
            return Or(b, a)
        return exp

    def regra_11(self, exp):
        """exp: p ↔ q ≡ q ↔ p (Comutatividade da Bicondicional)"""
        if isinstance(exp, Equivalent):
            return Equivalent(exp.b, exp.a)
        return exp

    def regra_12(self, exp):
        """exp: (p ∧ q) ∧ r ≡ p ∧ (q ∧ r) (Associatividade da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2:
            if isinstance(exp.args[0], And):
                a, b = exp.args[0].args
                r = exp.args[1]
                return And(a, And(b, r))
            if isinstance(exp.args[1], And):
                a = exp.args[0]
                b, r = exp.args[1].args
                return And(And(a, b), r)
        return exp

    def regra_13(self, exp):
        """exp: (p ∨ q) ∨ r ≡ p ∨ (q ∨ r) (Associatividade da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            if isinstance(exp.args[0], Or):
                a, b = exp.args[0].args
                r = exp.args[1]
                return Or(a, Or(b, r))
            if isinstance(exp.args[1], Or):
                a = exp.args[0]
                b, r = exp.args[1].args
                return Or(Or(a, b), r)
        return exp

    def regra_14(self, exp):
        """exp: (p ↔ q) ↔ r ≡ p ↔ (q ↔ r) (Associatividade da Bicondicional)"""
        if isinstance(exp, Equivalent):
            if isinstance(exp.a, Equivalent):
                a = exp.a.a
                b = exp.a.b
                r = exp.b
                return Equivalent(a, Equivalent(b, r))
            if isinstance(exp.b, Equivalent):
                a = exp.a
                b = exp.b.a
                r = exp.b.b
                return Equivalent(Equivalent(a, b), r)
        return exp

    def regra_15(self, exp):
        """exp: p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r) (Distributividade da Conjunção sobre Disjunção)"""
        if isinstance(exp, And) and isinstance(exp.args[1], Or):
            p = exp.args[0]
            q, r = exp.args[1].args
            return Or(And(p, q), And(p, r))
        if isinstance(exp, Or) and len(exp.args) == 2:
            if all(isinstance(arg, And) for arg in exp.args):
                and1, and2 = exp.args
                if and1.args[0] == and2.args[0]:
                    p = and1.args[0]
                    q = and1.args[1]
                    r = and2.args[1]
                    return And(p, Or(q, r))
        return exp

    def regra_16(self, exp):
        """exp: p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r) (Distributividade da Disjunção sobre Conjunção)"""
        if isinstance(exp, Or) and isinstance(exp.args[1], And):
            p = exp.args[0]
            q, r = exp.args[1].args
            return And(Or(p, q), Or(p, r))
        if isinstance(exp, And) and len(exp.args) == 2:
            if all(isinstance(arg, Or) for arg in exp.args):
                or1, or2 = exp.args
                if or1.args[0] == or2.args[0]:
                    p = or1.args[0]
                    q = or1.args[1]
                    r = or2.args[1]
                    return Or(p, And(q, r))
        return exp

    def regra_17(self, exp):
        """exp: p ∧ p ≡ p (Idempotência da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2 and exp.args[0] == exp.args[1]:
            return exp.args[0]
        if not isinstance(exp, And):
            return And(exp, exp)
        return exp

    def regra_18(self, exp):
        """exp: p ∨ p ≡ p (Idempotência da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2 and exp.args[0] == exp.args[1]:
            return exp.args[0]
        if not isinstance(exp, Or):
            return Or(exp, exp)
        return exp

    def regra_19(self, exp):
        """exp: p ∧ V ≡ p (Identidade da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2:
            p, q = exp.args
            if isinstance(q, V):
                return p
            if isinstance(p, V):
                return q
        if not isinstance(exp, And):
            return And(exp, V())
        return exp

    def regra_20(self, exp):
        """exp: p ∨ F ≡ p (Identidade da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            p, q = exp.args
            if isinstance(q, F):
                return p
            if isinstance(p, F):
                return q
        if not isinstance(exp, Or):
            return Or(exp, F())
        return exp

    def regra_21(self, exp):
        """exp: p ∧ F ≡ F (Dominação da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2:
            p, q = exp.args
            if isinstance(p, F) or isinstance(q, F):
                return F()
        if exp == F():
            return exp
        return exp

    def regra_22(self, exp):
        """exp: p ∨ V ≡ V (Dominação da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            p, q = exp.args
            if isinstance(p, V) or isinstance(q, V):
                return V()
        if exp == V():
            return exp
        return exp

    def regra_23(self, exp):
        """exp: p ∧ ¬p ≡ F (Contradição: Conjunção de um termo com sua negação)"""
        if isinstance(exp, And) and len(exp.args) == 2:
            a, b = exp.args
            if (isinstance(a, Not) and b == a.arg) or (isinstance(b, Not) and a == b.arg):
                return F()
        if exp == F():
            return exp
        return exp

    def regra_24(self, exp):
        """exp: p ∨ ¬p ≡ V (Tautologia: Disjunção de um termo com sua negação)"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            a, b = exp.args
            if (isinstance(a, Not) and b == a.arg) or (isinstance(b, Not) and a == b.arg):
                return V()
        if exp == V():
            return exp
        return exp

    def regra_25(self, exp):
        """exp: p ∧ (p ∨ q) ≡ p (Absorção da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2:
            p, or_exp = exp.args
            if isinstance(or_exp, Or) and p in or_exp.args:
                return p
        return exp

    def regra_26(self, exp):
        """exp: p ∨ (p ∧ q) ≡ p (Absorção da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            p, and_exp = exp.args
            if isinstance(and_exp, And) and p in and_exp.args:
                return p
        return exp

    def regra_27(self, exp):
        """exp: p ⊻ q ≡ (p ∨ q) ∧ ¬(p ∧ q) (Definição do OU Exclusivo)"""
        if isinstance(exp, Xor):
            return And(Or(exp.a, exp.b), Not(And(exp.a, exp.b)))
        if (isinstance(exp, And) and len(exp.args) == 2 and
            isinstance(exp.args[0], Or) and
            isinstance(exp.args[1], Not) and
            isinstance(exp.args[1].arg, And)):
            or_exp = exp.args[0]
            and_exp = exp.args[1].arg
            if set(or_exp.args) == set(and_exp.args):
                a, b = or_exp.args
                return Xor(a, b)
        return exp

    def regra_28(self, exp):
        """exp: (p ∧ q) → r ≡ p → (q → r) (Exportação)"""
        if isinstance(exp, Implies) and isinstance(exp.a, And):
            p, q = exp.a.args
            r = exp.b
            return Implies(p, Implies(q, r))
        return exp

    def regra_29(self, exp):
        """exp: p → (q → r) ≡ (p ∧ q) → r (Importação)"""
        if (isinstance(exp, Implies) and
            isinstance(exp.b, Implies)):
            p, q = exp.a, exp.b.a
            r = exp.b.b
            return Implies(And(p, q), r)
        return exp