"""
Módulo resolvedor: motor de transformação de expressões lógicas.
"""
from .regras import RegrasLogicas
from src.utils import verificar_equivalencia
import heapq
from functools import lru_cache

def aplicar_regra_recursiva(expr, regra_func):
    """Aplica uma regra em toda a árvore da expressão, incluindo aninhamentos."""
    nova_expr = regra_func(expr)
    if nova_expr != expr:
        return nova_expr
    if hasattr(expr, 'args') and expr.args:
        novos_args = [aplicar_regra_recursiva(arg, regra_func) for arg in expr.args]
        if any(na != a for na, a in zip(novos_args, expr.args)):
            return expr.__class__(*novos_args)
    elif hasattr(expr, 'arg'):
        novo_arg = aplicar_regra_recursiva(expr.arg, regra_func)
        if novo_arg != expr.arg:
            return expr.__class__(novo_arg)
    elif hasattr(expr, 'a') and hasattr(expr, 'b'):
        novo_a = aplicar_regra_recursiva(expr.a, regra_func)
        novo_b = aplicar_regra_recursiva(expr.b, regra_func)
        if novo_a != expr.a or novo_b != expr.b:
            return expr.__class__(novo_a, novo_b)
    return expr

@lru_cache(maxsize=10000)
def similaridade_cacheada(expr1, expr2):
    return similaridade(expr1, expr2)

def similaridade(expr1, expr2):
    """Heurística aprimorada: prioriza estrutura e conectivos próximos, depois nós em comum."""

    def subarvore_igual(e1, e2):
        if e1 == e2:
            return 5  
        if type(e1) != type(e2):
            return 0
        score = 0
        if hasattr(e1, 'args') and hasattr(e2, 'args') and len(e1.args) == len(e2.args):
            score += 2
            for a1, a2 in zip(e1.args, e2.args):
                score += subarvore_igual(a1, a2)
        elif hasattr(e1, 'a') and hasattr(e1, 'b') and hasattr(e2, 'a') and hasattr(e2, 'b'):
            score += 2
            score += subarvore_igual(e1.a, e2.a)
            score += subarvore_igual(e1.b, e2.b)
        elif hasattr(e1, 'arg') and hasattr(e2, 'arg'):
            score += 2
            score += subarvore_igual(e1.arg, e2.arg)
        return score

    def coletar_nos(expr):
        nos = set()
        def visitar(e):
            nos.add(str(e))
            if hasattr(e, 'args') and e.args:
                for arg in e.args:
                    visitar(arg)
            elif hasattr(e, 'arg'):
                visitar(e.arg)
            elif hasattr(e, 'a') and hasattr(e, 'b'):
                visitar(e.a)
                visitar(e.b)
        visitar(expr)
        return nos

    score = subarvore_igual(expr1, expr2)
    score += len(coletar_nos(expr1) & coletar_nos(expr2))
    return score

class Resolvedor:
    def __init__(self):
        self.regras_sistema = RegrasLogicas()
        self.regras = self.regras_sistema.regras

    def buscar_equivalencia(
        self, 
        expr_inicial, 
        expr_objetivo, 
        max_iteracoes = 10, 
        max_estados = 50000
    ):
        """
        Busca um caminho de transformação tentando primeiro a busca direta e, se falhar,
        a busca reversa, sempre exibindo o resultado do início para o objetivo.
        """
        equivalente, _ = verificar_equivalencia(expr_inicial, expr_objetivo)
        if not equivalente:
            print("As expressões não são logicamente equivalentes.")
            return False, None

        if expr_inicial == expr_objetivo:
            return True, [(expr_inicial, "Expressao inicial")]

        print("--- Iniciando busca direta (do início para o objetivo) ---")
        caminho_direto = self._busca_simples(expr_inicial, expr_objetivo, max_iteracoes, max_estados, "frente")
        if caminho_direto:
            print("Caminho encontrado na busca direta!")
            return True, caminho_direto

        print("\n--- Busca direta não encontrou caminho. Iniciando busca reversa (do objetivo para o início) ---")
        caminho_reverso = self._busca_simples(expr_objetivo, expr_inicial, max_iteracoes, max_estados, "tras")
        if caminho_reverso:
            print("Caminho encontrado na busca reversa! Reconstruindo para exibição...")
            caminho_final = []
            caminho_final.append((caminho_reverso[-1][0], "Expressao inicial"))
            for i in range(len(caminho_reverso) - 2, -1, -1):
                expr_passo_atual = caminho_reverso[i][0]
                regra_que_gerou_passo_anterior = caminho_reverso[i + 1][1]
                caminho_final.append((expr_passo_atual, regra_que_gerou_passo_anterior))
            return True, caminho_final

        print("\nNenhum caminho encontrado em ambas as direções.")
        return False, None

    def _busca_simples(
        self, 
        expr_inicio, 
        expr_fim, 
        max_iteracoes, 
        max_estados,
        label
    ):
        """
        Busca best-first com heapq e memoização da similaridade.
        """
        memoria = {expr_inicio}
        caminhos = {expr_inicio: [(expr_inicio, "Expressao inicial")]}
        heap = []
        contador = 0
        heapq.heappush(heap, (-similaridade_cacheada(expr_inicio, expr_fim), contador, expr_inicio))

        for iteracao in range(max_iteracoes):
            proximo_heap = []
            if not heap:
                print(f"Iteracao {iteracao + 1} ({label}): Fila vazia, busca encerrada.")
                break

            for _ in range(min(len(heap), max_estados)):
                _, _, expr_corrente = heapq.heappop(heap)
                for nome_regra, regra_func in self.regras:
                    nova_expr = aplicar_regra_recursiva(expr_corrente, regra_func)
                    if nova_expr != expr_corrente and nova_expr not in memoria:
                        novo_caminho = caminhos[expr_corrente] + [(nova_expr, nome_regra)]
                        if nova_expr == expr_fim:
                            print(f"Iteracao {iteracao+1} ({label}): caminho encontrado!")
                            return novo_caminho
                        caminhos[nova_expr] = novo_caminho
                        memoria.add(nova_expr)
                        contador += 1
                        prioridade = -similaridade_cacheada(nova_expr, expr_fim)
                        heapq.heappush(proximo_heap, (prioridade, contador, nova_expr))
            heap = proximo_heap
            print(f"Iteracao {iteracao + 1} ({label}): Fila={len(heap)}, Memoria={len(memoria)}")
        print(f"Busca ({label}) atingiu o limite de iterações ({max_iteracoes}) sem encontrar solução.")
        return None