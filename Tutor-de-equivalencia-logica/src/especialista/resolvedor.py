"""
Módulo resolvedor: motor de transformação de expressões lógicas.
"""
from .regras import RegrasLogicas
from src.utils import verificar_equivalencia, normalizar_expr
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

@lru_cache(maxsize=15000)  
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

    def _calcular_limite_explosao(self, expr_inicio, expr_fim):
        """Calcula limite inteligente para prevenir explosão de tamanho"""
        tamanho_inicial = len(str(expr_inicio))
        tamanho_objetivo = len(str(expr_fim))
        tamanho_base = max(tamanho_inicial, tamanho_objetivo)
        

        if tamanho_base <= 20:       
            fator_explosao = 8       
        elif tamanho_base <= 50:     
            fator_explosao = 6        
        elif tamanho_base <= 100:     
            fator_explosao = 5     
        else:                         
            fator_explosao = 4       
        
        limite = int(tamanho_base * fator_explosao)
        
        
        limite = min(limite, 600)     
        limite = max(limite, 80)      
        
        return limite

    def buscar_equivalencia(
        self, 
        expr_inicial, 
        expr_objetivo, 
        max_iteracoes=12, 
        max_estados=50000
    ):
        equivalente, _ = verificar_equivalencia(expr_inicial, expr_objetivo)
        if not equivalente:
            print("As expressões não são logicamente equivalentes.")
            return False, None

        if expr_inicial == expr_objetivo:
            return True, [(expr_inicial, "Expressao inicial")]

        print("--- Iniciando busca direta (do início para o objetivo) ---")
        caminho_direto = self._busca_simples(expr_inicial, expr_objetivo, 
                                            max_iteracoes, max_estados, "direta")
        if caminho_direto:
            print("Caminho encontrado na busca direta!")
            return True, caminho_direto

        print("\n--- Busca direta não encontrou caminho. Iniciando busca reversa (do objetivo para o início) ---")
        caminho_reverso = self._busca_simples(expr_objetivo, expr_inicial, 
                                             max_iteracoes, max_estados, "reversa")
        if caminho_reverso:
            print("Caminho encontrado na busca reversa!")
            return True, caminho_reverso
        
        print("\nNenhum caminho encontrado em ambas as direções.")
        return False, None

    def _reconstruir_caminho(self, pais, estado_final):
        caminho = []
        estado_atual = estado_final
        
        while estado_atual is not None:
            pai, regra = pais.get(estado_atual, (None, None))
            caminho.append((estado_atual, regra))
            estado_atual = pai
        
        caminho.reverse()
        if caminho:
            caminho[0] = (caminho[0][0], "Expressao inicial")
        return caminho

    def _busca_simples(
        self, 
        expr_inicio, 
        expr_fim, 
        max_iteracoes, 
        max_estados,
        label
    ):
        memoria = {expr_inicio}
        pais = {expr_inicio: (None, None)}
    
        limite_tamanho = self._calcular_limite_explosao(expr_inicio, expr_fim)
        print(f"Limite anti-explosão para {label}: {limite_tamanho} caracteres")
        
        heap = []
        contador = 0
        expr_fim_norm = normalizar_expr(expr_fim)
        inicio_norm = normalizar_expr(expr_inicio)
        heapq.heappush(heap, (-similaridade_cacheada(inicio_norm, expr_fim_norm), contador, expr_inicio))

        for iteracao in range(max_iteracoes):
            proximo_heap = []
            estados_podados = 0 
            transformacoes_totais = 0 
            
            if not heap:
                print(f"Iteracao {iteracao + 1} ({label}): Fila vazia, busca encerrada.")
                break

            for _ in range(min(len(heap), max_estados)):
                if not heap:
                    break
                _, _, expr_corrente = heapq.heappop(heap)
                
                for nome_regra, regra_func in self.regras:
                    try:
                        nova_expr = aplicar_regra_recursiva(expr_corrente, regra_func)
                        
                        if nova_expr == expr_corrente:
                            continue
                        
                        transformacoes_totais += 1

                      
                        tamanho_nova = len(str(nova_expr))
                        if tamanho_nova > limite_tamanho:
                            estados_podados += 1
                            continue 

                        if nova_expr == expr_fim:
                            print(f"Iteracao {iteracao+1} ({label}): caminho encontrado!")
                            if estados_podados > 0:
                                print(f"Total de podas por explosão: {estados_podados}")
                            pais[nova_expr] = (expr_corrente, nome_regra)
                            return self._reconstruir_caminho(pais, nova_expr)
                        
                        if nova_expr not in memoria:
                            pais[nova_expr] = (expr_corrente, nome_regra)
                            memoria.add(nova_expr)
                            contador += 1
                            nova_norm = normalizar_expr(nova_expr)
                            prioridade = -similaridade_cacheada(nova_norm, expr_fim_norm)
                            heapq.heappush(proximo_heap, (prioridade, contador, nova_expr))
                    
                    except Exception:
                        continue

            heap = proximo_heap
            
     
            debug_info = f"Iteracao {iteracao + 1} ({label}): Fila={len(heap)}, Memoria={len(memoria)}"
            
            if estados_podados > 0:
                taxa_poda = (estados_podados / max(transformacoes_totais, 1)) * 100
                debug_info += f", Podados={estados_podados} ({taxa_poda:.1f}%)"
            
            debug_info += f", Cache_hits={similaridade_cacheada.cache_info().hits}"
            print(debug_info)
        
        return None