"""
Módulo resolvedor: um motor aque aplica regras para transformar uma expressão.
"""
from .regras import RegrasLogicas

def aplicar_regra_recursiva(expr, regra_func):
    """Aplica uma regra em toda a árvore da expressão, incluindo aninhamentos."""
    nova_expr = regra_func(expr)
    if nova_expr != expr:
        return nova_expr
    
    if hasattr(expr, 'args') and expr.args:
        novos_args = [aplicar_regra_recursiva(arg, regra_func) for arg in expr.args]
        if any(na != a for na, a in zip(novos_args, expr.args)):
            return expr.func(*novos_args)
    
    return expr

class Resolvedor:
    def __init__(self):
        self.regras_sistema = RegrasLogicas()
        self.regras = self.regras_sistema.regras

    def buscar_equivalencia(self, expr_inicial, expr_objetivo, max_iteracoes=20):
        """
        Busca um caminho de transformação da expressão inicial para a objetivo.
        Retorna (True, caminho_com_regras) se encontrar.
        Retorna (False, None) se não encontrar.
        """
        if expr_inicial == expr_objetivo:
            return True, [(expr_inicial, "Expressão inicial")]
    
        # Lógica de busca em largura (BFS)
        memoria_trabalho = {expr_inicial}
        caminhos = {expr_inicial: [(expr_inicial, "Expressão inicial")]}
        fila = [expr_inicial]
        
        for _ in range(max_iteracoes):
            if not fila: break
            proxima_fila = []
            for expr in fila:
                for nome_regra, regra_func in self.regras:
                    nova_expr = aplicar_regra_recursiva(expr, regra_func)
                    if nova_expr != expr and nova_expr not in memoria_trabalho:
                        novo_caminho = caminhos[expr] + [(nova_expr, nome_regra)]
                        
                        # Objetivo encontrado! Retorna o sucesso e o caminho.
                        if nova_expr == expr_objetivo:
                            return True, novo_caminho

                        caminhos[nova_expr] = novo_caminho
                        memoria_trabalho.add(nova_expr)
                        proxima_fila.append(nova_expr)
            fila = proxima_fila
        
        # Se o loop terminar, a transformação não foi encontrada.
        return False, None