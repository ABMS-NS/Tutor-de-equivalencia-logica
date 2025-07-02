from src.especialista.nos_logicos import Symbol, Not, And, Or, Implies, Equivalent, Xor, V, F

class RegrasLogicas:
    def __init__(self):
        self.regras = [
            ("Regra 1 (Condicional ↔ Disjunção)", self.regra_1),
            ("Regra 2 (Contraposição)", self.regra_2),
            ("Regra 3 (Bicondicional ↔ Conjunção de Condicionais)", self.regra_3),
            ("Regra 4 (Bicondicional ↔ Disjunção de Conjunções)", self.regra_4),
            ("Regra 5 (Bicondicional ↔ Negação do XOR)", self.regra_5),
            ("Regra 6 (Dupla Negação)", self.regra_6),
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
            ("Regra 23 (Contradição)", self.regra_23),
            ("Regra 24 (Tautologia)", self.regra_24),
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
        
        if isinstance(exp, Or):
            nots = [arg.arg for arg in exp.args if isinstance(arg, Not)]
            others = [arg for arg in exp.args if not isinstance(arg, Not)]
            
            if len(nots) == 1 and others:
                consequent = Or(*others) if len(others) > 1 else others[0]
                return Implies(nots[0], consequent)
        return exp

    def regra_2(self, exp):
        """exp: p → q ≡ ¬q → ¬p (Contraposição)"""
        if isinstance(exp, Implies):
            a, b = exp.a, exp.b
            if isinstance(a, Not) and isinstance(b, Not):
                return Implies(b.arg, a.arg)
            else:
                return Implies(Not(b), Not(a))
        return exp

    def regra_3(self, exp):
        """exp: p ↔ q ≡ (p → q) ∧ (q → p) (Bicondicional ↔ Conjunção de Condicionais)"""
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
            conjunto_a, conjunto_b = exp.args
            if isinstance(conjunto_a.args[0], Not):
                conjunto_a, conjunto_b = conjunto_b, conjunto_a
            if len(conjunto_a.args) == 2 and len(conjunto_b.args) == 2:
                p1, q1 = conjunto_a.args
                p2, q2 = conjunto_b.args
                if isinstance(p2, Not) and isinstance(q2, Not):
                    sorted_pq1 = sorted([str(p1), str(q1)])
                    sorted_pq2 = sorted([str(p2.arg), str(q2.arg)])
                    if sorted_pq1 == sorted_pq2:
                        return Equivalent(p1, q1)
        return exp

    def regra_5(self, exp):
        """exp: p ↔ q ≡ ¬(p ⊻ q) (Bicondicional ↔ Negação do XOR)"""
        if isinstance(exp, Equivalent):
            return Not(Xor(exp.a, exp.b))
        if isinstance(exp, Not) and isinstance(exp.arg, Xor):
            return Equivalent(exp.arg.a, exp.arg.b)
        return exp

    def regra_6(self, exp):
        """exp: ¬¬p ≡ p (Dupla Negação)"""
        if isinstance(exp, Not) and isinstance(exp.arg, Not):
            return exp.arg.arg
        return exp

    def regra_7(self, exp):
        """exp: ¬(p ∧ q ∧ ...) ≡ ¬p ∨ ¬q ∨ ... (De Morgan para Conjunção)"""
        if isinstance(exp, Not) and isinstance(exp.arg, And):
            return Or(*[Not(arg) for arg in exp.arg.args])
        if isinstance(exp, Or) and all(isinstance(arg, Not) for arg in exp.args):
            return Not(And(*[arg.arg for arg in exp.args]))
        return exp

    def regra_8(self, exp):
        """exp: ¬(p ∨ q ∨ ...) ≡ ¬p ∧ ¬q ∧ ... (De Morgan para Disjunção)"""
        if isinstance(exp, Not) and isinstance(exp.arg, Or):
            return And(*[Not(arg) for arg in exp.arg.args])
        if isinstance(exp, And) and all(isinstance(arg, Not) for arg in exp.args):
            return Not(Or(*[arg.arg for arg in exp.args]))
        return exp

    def regra_9(self, exp):
        """exp: p ∧ q ∧ ... ≡ q ∧ p ∧ ... (Comutatividade da Conjunção)"""
        if isinstance(exp, And) and len(exp.args) > 1:
            argumentos_ordenados = sorted(exp.args, key=str)
            if list(exp.args) != argumentos_ordenados:
                return And(*argumentos_ordenados)
        return exp

   
    def regra_10(self, exp):
        """exp: p ∨ q ∨ ... ≡ q ∨ p ∨ ... (Comutatividade da Disjunção)"""
        if isinstance(exp, Or) and len(exp.args) > 1:
            argumentos_ordenados = sorted(exp.args, key=str)
            if list(exp.args) != argumentos_ordenados:
                return Or(*argumentos_ordenados)
        return exp

   
    def regra_11(self, exp):
        """exp: p ↔ q ≡ q ↔ p (Comutatividade da Bicondicional)"""
        if isinstance(exp, Equivalent):
            a, b = exp.a, exp.b
            if str(a) != str(b): 
               
                return Equivalent(b, a)
        return exp

    def regra_12(self, exp):
        """exp: (p ∧ q) ∧ r ... ≡ p ∧ q ∧ r ... (Associatividade da Conjunção)"""
        if not isinstance(exp, And): return exp
        novos_argumentos = []
        houve_mudanca = False
        for arg in exp.args:
            if isinstance(arg, And):
                novos_argumentos.extend(arg.args)
                houve_mudanca = True
            else:
                novos_argumentos.append(arg)
        return And(*novos_argumentos) if houve_mudanca else exp

    def regra_13(self, exp):
        """exp: (p ∨ q) ∨ r ... ≡ p ∨ q ∨ r ... (Associatividade da Disjunção)"""
        if not isinstance(exp, Or): return exp
        novos_argumentos = []
        houve_mudanca = False
        for arg in exp.args:
            if isinstance(arg, Or):
                novos_argumentos.extend(arg.args)
                houve_mudanca = True
            else:
                novos_argumentos.append(arg)
        return Or(*novos_argumentos) if houve_mudanca else exp

    def regra_14(self, exp):
        """exp: (p ↔ q) ↔ r ≡ p ↔ (q ↔ r) (Associatividade da Bicondicional)"""
        if isinstance(exp, Equivalent) and isinstance(exp.a, Equivalent):
            p, q = exp.a.a, exp.a.b
            r = exp.b
            return Equivalent(p, Equivalent(q, r))
        return exp

    def regra_15(self, exp):
        """exp: p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r) (Distributividade da Conjunção sobre Disjunção)"""
        
        if isinstance(exp, Or) and len(exp.args) > 1 and all(isinstance(t, And) for t in exp.args):
           
            listas_dos_termos = [sorted(arg.args, key=str) for arg in exp.args]
            
           
            fatores_comuns = listas_dos_termos[0][:]
            for lista in listas_dos_termos[1:]:
                fatores_comuns = [f for f in fatores_comuns if f in lista]
            
            if fatores_comuns:
                novos_disjuntos = []
                for lista in listas_dos_termos:
                    termos_restantes = [t for t in lista if t not in fatores_comuns]
                    if termos_restantes:
                        novos_disjuntos.append(termos_restantes[0] if len(termos_restantes) == 1 else And(*termos_restantes))
                
                if novos_disjuntos:
                    conjuntos_finais = fatores_comuns[:]
                    conjuntos_finais.append(novos_disjuntos[0] if len(novos_disjuntos) == 1 else Or(*sorted(novos_disjuntos, key=str)))
                    return conjuntos_finais[0] if len(conjuntos_finais) == 1 else And(*conjuntos_finais)
                
        if isinstance(exp, And):
            termo_or = next((arg for arg in exp.args if isinstance(arg, Or)), None)
            if termo_or:
                outros_termos = [arg for arg in exp.args if arg is not termo_or]
                if outros_termos:
                    novos_disjuntos = [And(*(outros_termos + [termo])) for termo in termo_or.args]
                    return Or(*novos_disjuntos)
        return exp

    def regra_16(self, exp):
        """exp: p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r) (Distributividade da Disjunção sobre Conjunção)"""
        if isinstance(exp, And) and len(exp.args) > 1 and all(isinstance(t, Or) for t in exp.args):
            listas_dos_termos = [sorted(arg.args, key=str) for arg in exp.args]
            fatores_comuns = listas_dos_termos[0][:]
            for lista in listas_dos_termos[1:]:
                fatores_comuns = [f for f in fatores_comuns if f in lista]
            if fatores_comuns:
                novos_conjuntos = []
                for lista in listas_dos_termos:
                    termos_restantes = [t for t in lista if t not in fatores_comuns]
                    if termos_restantes:
                        novos_conjuntos.append(termos_restantes[0] if len(termos_restantes) == 1 else Or(*termos_restantes))
                if novos_conjuntos:
                    conjuntos_finais = fatores_comuns[:]
                    conjuntos_finais.append(novos_conjuntos[0] if len(novos_conjuntos) == 1 else And(*sorted(novos_conjuntos, key=str)))
                    return conjuntos_finais[0] if len(conjuntos_finais) == 1 else Or(*conjuntos_finais)

        if isinstance(exp, Or):
            termo_and = next((arg for arg in exp.args if isinstance(arg, And)), None)
            if termo_and:
                outros_termos = [arg for arg in exp.args if arg is not termo_and]
                if outros_termos:
                    novos_conjuntos = [Or(*(outros_termos + [termo])) for termo in termo_and.args]
                    return And(*novos_conjuntos)
        return exp

    def regra_17(self, exp):
        """exp: p ∧ p ∧ q ≡ p ∧ q (Idempotência da Conjunção)"""
        if isinstance(exp, And):
            args_unicos = []
            for arg in exp.args:
                if arg not in args_unicos:
                    args_unicos.append(arg)
            
            if len(args_unicos) < len(exp.args):
                if len(args_unicos) == 1:
                    return args_unicos[0]
                return And(*args_unicos)
        return exp

    def regra_18(self, exp):
        """exp: p ∨ p ∨ q ≡ p ∨ q (Idempotência da Disjunção)"""
        if isinstance(exp, Or):
            args_unicos = []
            for arg in exp.args:
                if arg not in args_unicos:
                    args_unicos.append(arg)
            
            if len(args_unicos) < len(exp.args):
                if len(args_unicos) == 1:
                    return args_unicos[0]
                return Or(*args_unicos)
        return exp

    def regra_19(self, exp):
        """exp: p ∧ V ≡ p (Identidade da Conjunção)"""
        if isinstance(exp, And):
            novos_argumentos = [arg for arg in exp.args if not isinstance(arg, V)]
            if len(novos_argumentos) < len(exp.args):
                if not novos_argumentos: return V()
                return novos_argumentos[0] if len(novos_argumentos) == 1 else And(*novos_argumentos)
        return exp

    def regra_20(self, exp):
        """exp: p ∨ F ≡ p (Identidade da Disjunção)"""
        if isinstance(exp, Or):
            novos_argumentos = [arg for arg in exp.args if not isinstance(arg, F)]
            if len(novos_argumentos) < len(exp.args):
                if not novos_argumentos: return F()
                return novos_argumentos[0] if len(novos_argumentos) == 1 else Or(*novos_argumentos)
        return exp

    def regra_21(self, exp):
        """exp: p ∧ F ∧ q ≡ F (Dominação da Conjunção)"""
        if isinstance(exp, And) and any(isinstance(arg, F) for arg in exp.args):
            return F()
        return exp

    def regra_22(self, exp):
        """exp: p ∨ V ∨ q ≡ V (Dominação da Disjunção)"""
        if isinstance(exp, Or) and any(isinstance(arg, V) for arg in exp.args):
            return V()
        return exp

    def regra_23(self, exp):
        """exp: p ∧ ¬p ∧ q ≡ F (Contradição)"""
        if isinstance(exp, And):
            visto = set()
            for arg in exp.args:
                if isinstance(arg, Not):
                    key = (arg.arg, 'neg')
                    comp = (arg.arg, 'pos')
                else:
                    key = (arg, 'pos')
                    comp = (arg, 'neg')
                
                if comp in visto:
                    return F()
                visto.add(key)
        return exp

    def regra_24(self, exp):
        """exp: p ∨ ¬p ∨ q ≡ V (Tautologia)"""
        if isinstance(exp, Or):
            visto = set()
            for arg in exp.args:
                if isinstance(arg, Not):
                    key = (arg.arg, 'neg')
                    comp = (arg.arg, 'pos')
                else:
                    key = (arg, 'pos')
                    comp = (arg, 'neg')
                
                if comp in visto:
                    return V()
                visto.add(key)
        return exp

    def regra_25(self, exp):
        """exp: p ∧ (p ∨ q) ∧ r ≡ p ∧ r (Absorção da Conjunção)"""
        if not isinstance(exp, And): 
            return exp
        
        termos_absorventes = [arg for arg in exp.args if not isinstance(arg, Or)]
        if not termos_absorventes: 
            return exp
        
        argumentos_finais = termos_absorventes[:]
        houve_mudanca = False
        
        for arg in exp.args:
            if isinstance(arg, Or):
                tem_intersecao = any(termo in arg.args for termo in termos_absorventes)
                if not tem_intersecao:
                    argumentos_finais.append(arg)
                else:
                    houve_mudanca = True
        
        if houve_mudanca:
            if len(argumentos_finais) == 1: 
                return argumentos_finais[0]
            return And(*argumentos_finais)
        return exp

    def regra_26(self, exp):
        """exp: p ∨ (p ∧ q) ∨ r ≡ p ∨ r (Absorção da Disjunção)"""
        if not isinstance(exp, Or): 
            return exp
        
        termos_absorventes = [arg for arg in exp.args if not isinstance(arg, And)]
        if not termos_absorventes: 
            return exp

        argumentos_finais = termos_absorventes[:]
        houve_mudanca = False
        
        for arg in exp.args:
            if isinstance(arg, And):
                tem_intersecao = any(termo in arg.args for termo in termos_absorventes)
                if not tem_intersecao:
                    argumentos_finais.append(arg)
                else:
                    houve_mudanca = True
        
        if houve_mudanca:
            if len(argumentos_finais) == 1: 
                return argumentos_finais[0]
            return Or(*argumentos_finais)
        return exp

    def regra_27(self, exp):
        """exp: p ⊻ q ≡ (p ∨ q) ∧ ¬(p ∧ q) (Definição do OU Exclusivo)"""
        if isinstance(exp, Xor):
            return And(Or(exp.a, exp.b), Not(And(exp.a, exp.b)))
        if (isinstance(exp, And) and len(exp.args) == 2 and
            isinstance(exp.args[0], Or) and len(exp.args[0].args) == 2 and
            isinstance(exp.args[1], Not) and
            isinstance(exp.args[1].arg, And) and len(exp.args[1].arg.args) == 2):
            expressao_or = exp.args[0]
            expressao_and = exp.args[1].arg
            or_sorted = sorted([str(arg) for arg in expressao_or.args])
            and_sorted = sorted([str(arg) for arg in expressao_and.args])
            if or_sorted == and_sorted:
                 a, b = expressao_or.args
                 return Xor(a, b)
        return exp

    def regra_28(self, exp):
        """exp: (p ∧ q ∧ ...) → r ≡ p → (q → (... → r)) (Exportação)"""
        if isinstance(exp, Implies) and isinstance(exp.a, And) and len(exp.a.args) > 1:
            primeiro, *resto = exp.a.args
            r = exp.b
            expressao_resto = resto[0] if len(resto) == 1 else And(*resto)
            return Implies(primeiro, Implies(expressao_resto, r))
        return exp

    def regra_29(self, exp):
        """exp: p → (q → (... → r)) ≡ (p ∧ q ∧ ...) → r (Importação)"""
        if isinstance(exp, Implies) and isinstance(exp.b, Implies):
            premissas = [exp.a]
            expressao_atual = exp.b
            while isinstance(expressao_atual, Implies):
                premissas.append(expressao_atual.a)
                expressao_atual = expressao_atual.b
            
            premissas_finais = []
            for p in premissas:
                if isinstance(p, And):
                    premissas_finais.extend(p.args)
                else:
                    premissas_finais.append(p)
            
            return Implies(And(*premissas_finais), expressao_atual)
        return exp

def get_regras_formatadas():
    """
    Retorna uma lista de dicionários com as regras lógicas formatadas para exibição didática.
    Cada item contém: nome, formula, explicacao e exemplo(caso necessário)
    """
    return [
        {
            "nome": "Regra 1 (Condicional ↔ Disjunção)",
            "formula": "p → q ≡ ¬p ∨ q",
            "explicacao": "Uma condicional pode ser reescrita como uma disjunção: se p implica q, isso é equivalente a dizer que ou não p, ou q é verdadeiro.",
        },
        {
            "nome": "Regra 2 (Contraposição)",
            "formula": "p → q ≡ ¬q → ¬p",
            "explicacao": "A contrapositiva de uma condicional é logicamente equivalente à condicional original.",
        },
        {
            "nome": "Regra 3 (Bicondicional ↔ Conjunção de Condicionais)",
            "formula": "p ↔ q ≡ (p → q) ∧ (q → p)",
            "explicacao": "Um bicondicional é verdadeiro quando ambos os condicionais são verdadeiros.",
        },
        {
            "nome": "Regra 4 (Bicondicional ↔ Disjunção de Conjunções)",
            "formula": "p ↔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q)",
            "explicacao": "O bicondicional é verdadeiro quando ambos são verdadeiros ou ambos são falsos.",
        },
        {
            "nome": "Regra 5 (Bicondicional ↔ Negação do XOR)",
            "formula": "p ↔ q ≡ ¬(p ⊻ q)",
            "explicacao": "O bicondicional é verdadeiro quando p e q têm o mesmo valor lógico.",
        },
        {
            "nome": "Regra 6 (Dupla Negação)",
            "formula": "¬¬p ≡ p",
            "explicacao": "Negar duas vezes uma proposição retorna ao valor original.",
        },
        {
            "nome": "Regra 7 (De Morgan para Conjunção)",
            "formula": "¬(p ∧ q ∧ ...) ≡ ¬p ∨ ¬q ∨ ...",
            "explicacao": "A negação de uma conjunção é equivalente à disjunção das negações.",
        },
        {
            "nome": "Regra 8 (De Morgan para Disjunção)",
            "formula": "¬(p ∨ q ∨ ...) ≡ ¬p ∧ ¬q ∧ ...",
            "explicacao": "A negação de uma disjunção é equivalente à conjunção das negações.",
        },
        {
            "nome": "Regra 9 (Comutatividade da Conjunção)",
            "formula": "p ∧ q ∧ ... ≡ q ∧ p ∧ ...",
            "explicacao": "A ordem dos fatores não altera o produto na conjunção.",
        },
        {
            "nome": "Regra 10 (Comutatividade da Disjunção)",
            "formula": "p ∨ q ∨ ... ≡ q ∨ p ∨ ...",
            "explicacao": "A ordem dos fatores não altera a soma na disjunção.",
        },
        {
            "nome": "Regra 11 (Comutatividade da Bicondicional)",
            "formula": "p ↔ q ≡ q ↔ p",
            "explicacao": "A ordem dos termos em um bicondicional não altera seu valor lógico.",
        },
        {
            "nome": "Regra 12 (Associatividade da Conjunção)",
            "formula": "(p ∧ q) ∧ r ... ≡ p ∧ q ∧ r ...",
            "explicacao": "A forma como os termos são agrupados na conjunção não altera o resultado.",
        },
        {
            "nome": "Regra 13 (Associatividade da Disjunção)",
            "formula": "(p ∨ q) ∨ r ... ≡ p ∨ q ∨ r ...",
            "explicacao": "A forma como os termos são agrupados na disjunção não altera o resultado.",
        },
        {
            "nome": "Regra 14 (Associatividade da Bicondicional)",
            "formula": "(p ↔ q) ↔ r ≡ p ↔ (q ↔ r)",
            "explicacao": "A forma como os termos são agrupados em um bicondicional não altera seu valor lógico.",
        },
        {
            "nome": "Regra 15 (Distributividade da Conjunção sobre Disjunção)",
            "formula": "p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)",
            "explicacao": "A conjunção distribui sobre a disjunção da mesma forma que a multiplicação distribui sobre a adição.",
        },
        {
            "nome": "Regra 16 (Distributividade da Disjunção sobre Conjunção)",
            "formula": "p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)",
            "explicacao": "A disjunção distribui sobre a conjunção da mesma forma que a adição distribui sobre a multiplicação.",
        },
        {
            "nome": "Regra 17 (Idempotência da Conjunção)",
            "formula": "p ∧ p ∧ q ≡ p ∧ q",
            "explicacao": "Repetir o mesmo fator na conjunção não altera o resultado.",
        },
        {
            "nome": "Regra 18 (Idempotência da Disjunção)",
            "formula": "p ∨ p ∨ q ≡ p ∨ q",
            "explicacao": "Repetir o mesmo termo na disjunção não altera o resultado.",
        },
        {
            "nome": "Regra 19 (Identidade da Conjunção)",
            "formula": "p ∧ V ≡ p",
            "explicacao": "A conjunção com o elemento neutro V (verdade) não altera o valor da proposição.",
        },
        {
            "nome": "Regra 20 (Identidade da Disjunção)",
            "formula": "p ∨ F ≡ p",
            "explicacao": "A disjunção com o elemento neutro F (falsidade) não altera o valor da proposição.",
        },
        {
            "nome": "Regra 21 (Dominação da Conjunção)",
            "formula": "p ∧ F ∧ q ≡ F",
            "explicacao": "A presença de F (falsidade) em uma conjunção a torna falsa.",
        },
        {
            "nome": "Regra 22 (Dominação da Disjunção)",
            "formula": "p ∨ V ∨ q ≡ V",
            "explicacao": "A presença de V (verdade) em uma disjunção a torna verdadeira.",
        },
        {
            "nome": "Regra 23 (Contradição)",
            "formula": "p ∧ ¬p ∧ q ≡ F",
            "explicacao": "Uma contradição sempre resulta em falsidade.",
        },
        {
            "nome": "Regra 24 (Tautologia)",
            "formula": "p ∨ ¬p ∨ q ≡ V",
            "explicacao": "Uma tautologia sempre resulta em verdade.",
        },
        {
            "nome": "Regra 25 (Absorção da Conjunção)",
            "formula": "p ∧ (p ∨ q) ∧ r ≡ p ∧ r",
            "explicacao": "A conjunção de p com a disjunção de p e q é equivalente a p e r.",
        },
        {
            "nome": "Regra 26 (Absorção da Disjunção)",
            "formula": "p ∨ (p ∧ q) ∨ r ≡ p ∨ r",
            "explicacao": "A disjunção de p com a conjunção de p e q é equivalente a p ou r.",
        },
        {
            "nome": "Regra 27 (Definição do OU Exclusivo)",
            "formula": "p ⊻ q ≡ (p ∨ q) ∧ ¬(p ∧ q)",
            "explicacao": "O OU exclusivo é verdadeiro quando p ou q são verdadeiros, mas não ambos.",
        },
        {
            "nome": "Regra 28 (Exportação)",
            "formula": "(p ∧ q ∧ ...) → r ≡ p → (q → (... → r))",
            "explicacao": "A exportação permite transformar uma condicional com conjunção de premissas em uma cadeia de condicionais aninhados.",
            "exemplo": "Exemplo: (p ∧ q) → r ≡ p → (q → r)"
        },
        {
            "nome": "Regra 29 (Importação)",
            "formula": "p → (q → (... → r)) ≡ (p ∧ q ∧ ...) → r",
            "explicacao": "A importação faz o caminho inverso da exportação, agrupando premissas de condicionais aninhados em uma única conjunção.",
            "exemplo": "Exemplo: p → (q → r) ≡ (p ∧ q) → r"
        },                
    ]   