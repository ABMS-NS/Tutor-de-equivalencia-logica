from sympy import Not, And, Or, Implies, Equivalent, Xor, true, false

class RegrasLogicas:
    def __init__(self):
        self.regras = [
            ("Regra 1 (Condicional → Disjunção)", self.regra_1),
            ("Regra 2 (Disjunção → Condicional)", self.regra_2),
            ("Regra 3 (Contraposição)", self.regra_3),
            ("Regra 4 (Contraposição inversa)", self.regra_4),
            ("Regra 5 (Bicondicional → Conjunção de Condicionais)", self.regra_5),
            ("Regra 6 (Bicondicional → Disjunção de Conjunções)", self.regra_6),
            ("Regra 7 (Bicondicional ↔ negação do XOR)", self.regra_7),
            ("Regra 8 (Dupla negação)", self.regra_8),
            ("Regra 9 (De Morgan para Conjunção)", self.regra_9),
            ("Regra 10 (De Morgan para Disjunção)", self.regra_10),
            ("Regra 11 (Comutatividade da Conjunção)", self.regra_11),
            ("Regra 12 (Comutatividade da Disjunção)", self.regra_12),
            ("Regra 13 (Comutatividade da Bicondicional)", self.regra_13),
            ("Regra 14 (Associatividade da Conjunção)", self.regra_14),
            ("Regra 15 (Associatividade da Disjunção)", self.regra_15),
            ("Regra 16 (Associatividade da Bicondicional)", self.regra_16),
            ("Regra 17 (Distributividade da Conjunção sobre Disjunção)", self.regra_17),
            ("Regra 18 (Distributividade da Disjunção sobre Conjunção)", self.regra_18),
            ("Regra 19 (Idempotência da Conjunção)", self.regra_19),
            ("Regra 20 (Idempotência da Disjunção)", self.regra_20),
            ("Regra 21 (Identidade da Conjunção)", self.regra_21),
            ("Regra 22 (Identidade da Disjunção)", self.regra_22),
            ("Regra 23 (Dominação da Conjunção)", self.regra_23),
            ("Regra 24 (Dominação da Disjunção)", self.regra_24),
            ("Regra 25 (Contradição da Conjunção)", self.regra_25),
            ("Regra 26 (Tautologia da Disjunção)", self.regra_26),
            ("Regra 27 (Absorção da Conjunção)", self.regra_27),
            ("Regra 28 (Absorção da Disjunção)", self.regra_28),
            ("Regra 29 (Definição do OU Exclusivo)", self.regra_29),
            ("Regra 30 (Exportação)", self.regra_30),
            ("Regra 31 (Importação)", self.regra_31),
        ]

    def regra_1(self, exp):
        """exp: p → q ≡ ¬p ∨ q"""
        if isinstance(exp, Implies) and len(exp.args) == 2:
            p, q = exp.args
            return Or(Not(p), q)
        return exp

    def regra_2(self, exp):
        """exp: ¬p ∨ q ≡ p → q"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            a, b = exp.args
            if isinstance(a, Not) and not isinstance(b, Not) and a.args[0] != b:
                return Implies(a.args[0], b)
            if isinstance(b, Not) and not isinstance(a, Not) and b.args[0] != a:
                return Implies(b.args[0], a)
        return exp
    
    def regra_3(self, exp):
        """exp: p → q ≡ ¬q → ¬p"""
        if isinstance(exp, Implies) and len(exp.args) == 2:
            p, q = exp.args
            return Implies(Not(q), Not(p))
        return exp

    def regra_4(self, exp):
        """exp: ¬q → ¬p ≡ p → q"""
        if (isinstance(exp, Implies) and
            isinstance(exp.args[0], Not) and
            isinstance(exp.args[1], Not)):
            return Implies(exp.args[1].args[0], exp.args[0].args[0])
        return exp
    
    def regra_5(self, exp):
        """exp: p ↔ q ≡ (p → q) ∧ (q → p)"""
        if isinstance(exp, Equivalent) and len(exp.args) == 2:
            p, q = exp.args
            return And(Implies(p, q), Implies(q, p))
        return exp

    def regra_6(self, exp):
        """exp: p ↔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q)"""
        if isinstance(exp, Equivalent) and len(exp.args) == 2:
            p, q = exp.args
            return Or(And(p, q), And(Not(p), Not(q)))
        return exp

    def regra_7(self, exp):
        """exp: p ↔ q ≡ ¬(p ⊻ q)"""
        if isinstance(exp, Equivalent) and len(exp.args) == 2:
            p, q = exp.args
            return Not(Xor(p, q))
        return exp

    def regra_8(self, exp):
        """exp: ¬¬p ≡ p"""
        if isinstance(exp, Not) and isinstance(exp.args[0], Not):
            return exp.args[0].args[0]
        return exp

    def regra_9(self, exp):
        """exp: ¬(p ∧ q) ≡ ¬p ∨ ¬q (De Morgan para Conjunção)"""
        if isinstance(exp, Not) and isinstance(exp.args[0], And):
            return Or(*[Not(arg) for arg in exp.args[0].args])
        return exp

    def regra_10(self, exp):
        """exp: ¬(p ∨ q) ≡ ¬p ∧ ¬q (De Morgan para Disjunção)"""
        if isinstance(exp, Not) and isinstance(exp.args[0], Or):
            return And(*[Not(arg) for arg in exp.args[0].args])
        return exp

    def regra_11(self, exp):
        """exp: p ∧ q ≡ q ∧ p (Comutatividade da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2:
            return And(exp.args[1], exp.args[0])
        return exp

    def regra_12(self, exp):
        """exp: p ∨ q ≡ q ∨ p (Comutatividade da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            return Or(exp.args[1], exp.args[0])
        return exp

    def regra_13(self, exp):
        """exp: p ↔ q ≡ q ↔ p (Comutatividade da Bicondicional)"""
        if isinstance(exp, Equivalent) and len(exp.args) == 2:
            return Equivalent(exp.args[1], exp.args[0])
        return exp

    def regra_14(self, exp):
        """exp: (p ∧ q) ∧ r ≡ p ∧ (q ∧ r) (Associatividade da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2 and isinstance(exp.args[0], And):
            a, b = exp.args[0].args
            r = exp.args[1]
            return And(a, And(b, r))
        return exp

    def regra_15(self, exp):
        """exp: (p ∨ q) ∨ r ≡ p ∨ (q ∨ r) (Associatividade da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2 and isinstance(exp.args[0], Or):
            a, b = exp.args[0].args
            r = exp.args[1]
            return Or(a, Or(b, r))
        return exp

    def regra_16(self, exp):
        """exp: (p ↔ q) ↔ r ≡ p ↔ (q ↔ r) (Associatividade da Bicondicional)"""
        if isinstance(exp, Equivalent) and len(exp.args) == 2 and isinstance(exp.args[0], Equivalent):
            a, b = exp.args[0].args
            r = exp.args[1]
            return Equivalent(a, Equivalent(b, r))
        return exp

    def regra_17(self, exp):
        """exp: p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r) (Distributividade da Conjunção sobre Disjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2:
            p, q_or_r = exp.args
            if isinstance(q_or_r, Or) and len(q_or_r.args) == 2:
                q, r = q_or_r.args
                return Or(And(p, q), And(p, r))
        return exp

    def regra_18(self, exp):
        """exp: p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r) (Distributividade da Disjunção sobre Conjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            p, q_and_r = exp.args
            if isinstance(q_and_r, And) and len(q_and_r.args) == 2:
                q, r = q_and_r.args
                return And(Or(p, q), Or(p, r))
        return exp

    def regra_19(self, exp):
        """exp: p ∧ p ≡ p (Idempotência da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2 and exp.args[0] == exp.args[1]:
            return exp.args[0]
        return exp

    def regra_20(self, exp):
        """exp: p ∨ p ≡ p (Idempotência da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2 and exp.args[0] == exp.args[1]:
            return exp.args[0]
        return exp

    def regra_21(self, exp):
        """exp: p ∧ V ≡ p (Identidade da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2:
            p, q = exp.args
            if q == true:
                return p
            if p == true:
                return q
        return exp

    def regra_22(self, exp):
        """exp: p ∨ F ≡ p (Identidade da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            p, q = exp.args
            if q == false:
                return p
            if p == false:
                return q
        return exp

    def regra_23(self, exp):
        """exp: p ∧ F ≡ F (Dominação da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2:
            p, q = exp.args
            if p == false or q == false:
                return false
        return exp

    def regra_24(self, exp):
        """exp: p ∨ V ≡ V (Dominação da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            p, q = exp.args
            if p == true or q == true:
                return true
        return exp

    def regra_25(self, exp):
        """exp: p ∧ ¬p ≡ F (Contradição: Conjunção de um termo com sua negação)"""
        if isinstance(exp, And) and len(exp.args) == 2:
            a, b = exp.args
            if (isinstance(a, Not) and b == a.args[0]) or (isinstance(b, Not) and a == b.args[0]):
                return false
        return exp

    def regra_26(self, exp):
        """exp: p ∨ ¬p ≡ V (Tautologia: Disjunção de um termo com sua negação)"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            a, b = exp.args
            if (isinstance(a, Not) and b == a.args[0]) or (isinstance(b, Not) and a == b.args[0]):
                return true
        return exp

    def regra_27(self, exp):
        """exp: p ∧ (p ∨ q) ≡ p (Absorção da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) == 2:
            p, or_exp = exp.args
            if isinstance(or_exp, Or) and p in or_exp.args:
                return p
            if isinstance(p, Or) and or_exp in p.args:
                return or_exp
        return exp

    def regra_28(self, exp):
        """exp: p ∨ (p ∧ q) ≡ p (Absorção da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) == 2:
            p, and_exp = exp.args
            if isinstance(and_exp, And) and p in and_exp.args:
                return p
            if isinstance(p, And) and and_exp in p.args:
                return and_exp
        return exp

    def regra_29(self, exp):
        """exp: p ⊻ q ≡ (p ∨ q) ∧ ¬(p ∧ q) (Definição do OU Exclusivo)"""
        if isinstance(exp, Xor) and len(exp.args) == 2:
            p, q = exp.args
            return And(Or(p, q), Not(And(p, q)))
        return exp
    
    def regra_30(self, exp):
        """exp: (p ∧ q) → r ≡ p → (q → r) (Exportação)"""
        if isinstance(exp, Implies) and isinstance(exp.args[0], And) and len(exp.args[0].args) == 2:
            p, q = exp.args[0].args
            r = exp.args[1]
            return Implies(p, Implies(q, r))
        return exp

    def regra_31(self, exp):
        """exp: p → (q → r) ≡ (p ∧ q) → r (Importação)"""
        if (isinstance(exp, Implies) and
            isinstance(exp.args[1], Implies) and
            len(exp.args[1].args) == 2):
            p = exp.args[0]
            q, r = exp.args[1].args
            return Implies(And(p, q), r)
        return exp