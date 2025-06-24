"""
Módulo resolvedor: motor de transformação de expressões lógicas.
"""
from typing import List, Tuple, Any, Optional
from .regras import RegrasLogicas
from src.utils import verificar_equivalencia

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

def similaridade(expr1, expr2):
    """Calcula a similaridade entre duas expressões."""
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
    
    nos1 = coletar_nos(expr1)
    nos2 = coletar_nos(expr2)
    return len(nos1 & nos2)

class Resolvedor:
    def __init__(self):
        self.regras_sistema = RegrasLogicas()
        self.regras = self.regras_sistema.regras

    def buscar_equivalencia(
        self, 
        expr_inicial: Any, 
        expr_objetivo: Any, 
        max_iteracoes: int = 10, 
        max_estados: int = 5000
    ) -> Tuple[bool, Optional[List[Tuple[Any, str]]]]:
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

        # 1. Tenta a busca direta (do início para o objetivo)
        print("--- Iniciando busca direta (do início para o objetivo) ---")
        caminho_direto = self._busca_simples(expr_inicial, expr_objetivo, max_iteracoes, max_estados, "frente")
        if caminho_direto:
            print("Caminho encontrado na busca direta!")
            return True, caminho_direto

        # 2. Se a busca direta falhar, tenta a busca reversa (do objetivo para o início)
        print("\n--- Busca direta não encontrou caminho. Iniciando busca reversa (do objetivo para o início) ---")
        caminho_reverso = self._busca_simples(expr_objetivo, expr_inicial, max_iteracoes, max_estados, "tras")
        if caminho_reverso:
            print("Caminho encontrado na busca reversa! Reconstruindo para exibição...")
            
            # Reconstrói o caminho na ordem correta (inicial -> objetivo)
            # para garantir que as regras fiquem alinhadas com as transformações.
            caminho_final = []
            
            # O primeiro passo é a expressão inicial (o último item encontrado no caminho reverso).
            caminho_final.append((caminho_reverso[-1][0], "Expressao inicial"))
            
            # Itera de trás para frente no caminho reverso para montar o caminho final.
            # A regra para cada passo é a regra do passo *seguinte* no caminho reverso.
            for i in range(len(caminho_reverso) - 2, -1, -1):
                expr_passo_atual = caminho_reverso[i][0]
                regra_que_gerou_passo_anterior = caminho_reverso[i + 1][1]
                caminho_final.append((expr_passo_atual, regra_que_gerou_passo_anterior))
                
            return True, caminho_final

        print("\nNenhum caminho encontrado em ambas as direções.")
        return False, None

    def _busca_simples(
        self, 
        expr_inicio: Any, 
        expr_fim: Any, 
        max_iteracoes: int, 
        max_estados: int,
        label: str
    ) -> Optional[List[Tuple[Any, str]]]:
        """
        Realiza uma busca em largura best-first de um ponto a outro.
        """
        memoria = {expr_inicio}
        # O caminho inicial já contém o primeiro passo
        caminhos = {expr_inicio: [(expr_inicio, "Expressao inicial")]}
        fila = [expr_inicio]

        for iteracao in range(max_iteracoes):
            proxima_fila = []
            if not fila:
                print(f"Iteracao {iteracao + 1} ({label}): Fila vazia, busca encerrada.")
                break

            for expr_corrente in fila:
                for nome_regra, regra_func in self.regras:
                    nova_expr = aplicar_regra_recursiva(expr_corrente, regra_func)

                    if nova_expr != expr_corrente and nova_expr not in memoria:
                        novo_caminho = caminhos[expr_corrente] + [(nova_expr, nome_regra)]
                        
                        if nova_expr == expr_fim:
                            print(f"Iteracao {iteracao+1} ({label}): caminho encontrado!")
                            return novo_caminho # Sucesso!

                        caminhos[nova_expr] = novo_caminho
                        memoria.add(nova_expr)
                        proxima_fila.append(nova_expr)
            
            # Ordena pela similaridade e limita o tamanho da fila (Best-First Search)
            proxima_fila.sort(key=lambda e: similaridade(e, expr_fim), reverse=True)
            fila = proxima_fila[:max_estados]

            print(f"Iteracao {iteracao + 1} ({label}): " +
                  f"Fila={len(fila)}, Memoria={len(memoria)}")
        
        print(f"Busca ({label}) atingiu o limite de iterações ({max_iteracoes}) sem encontrar solução.")
        return None