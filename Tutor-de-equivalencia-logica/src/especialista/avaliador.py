from src.utils import verificar_equivalencia, formatar_expressao
from src.especialista.parser import parser_expr
from src.especialista.regras import RegrasLogicas
from src.especialista.resolvedor import aplicar_regra_recursiva 

regras = RegrasLogicas()

def processar_entrada_usuario(texto):
    texto = texto.replace(' ', '') 
    try:
        expr = parser_expr(texto)
        return expr, None
    except Exception as e:
        return None, f"Erro ao processar a expressão: {e}"

def avaliar_resposta_final(resposta_aluno, resposta_correta):
    expr_aluno, erro1 = processar_entrada_usuario(resposta_aluno)
    expr_correta, erro2 = processar_entrada_usuario(resposta_correta)
    if erro1 or erro2:
        return False, "Erro ao processar a expressão."
    equivalente, _ = verificar_equivalencia(expr_aluno, expr_correta)
    return equivalente, None if equivalente else "Expressão não equivalente."

def identificar_regra_aplicada(expr_antes, expr_depois):
    regras_aplicadas = []
    for rotulo, func in regras.regras:
        resultado = aplicar_regra_recursiva(expr_antes, func)
        if resultado == expr_depois:
            regras_aplicadas.append(rotulo)
        else:
            # Testa a aplicação reversa da regra
            resultado_reverso = aplicar_regra_recursiva(expr_depois, func)
            if resultado_reverso == expr_antes:
                regras_aplicadas.append(rotulo + " (inversa)")
    return regras_aplicadas
def avaliar_passos(lista_passos, expr_inicial, expr_objetivo):
    """
    lista_passos: [expr1, expr2, expr3, ...] (strings)
    expr_inicial: expressão simbólica inicial (string)
    expr_objetivo: expressão simbólica final (string)
    Retorna (True, detalhes, erros, historico) se todos os passos são válidos e a conclusão é equivalente ao objetivo (em qualquer ordem).
    Se algum passo for inválido, retorna (False, detalhes, lista_de_erros, historico).
    """
    exprs = []
    erros_transicao = []
    historico = []
    for texto in lista_passos:
        expr, erro = processar_entrada_usuario(texto)
        if erro:
            historico.append(f"Erro ao processar: {erro}")
            return False, f"Erro ao processar: {erro}", [f"Erro ao processar: {erro}"], historico
        exprs.append(expr)
    # Verifica se o primeiro e último passo são o inicial e o objetivo (em qualquer ordem)
    if not ((exprs[0] == processar_entrada_usuario(expr_inicial)[0] and exprs[-1] == processar_entrada_usuario(expr_objetivo)[0]) or
            (exprs[0] == processar_entrada_usuario(expr_objetivo)[0] and exprs[-1] == processar_entrada_usuario(expr_inicial)[0])):
        historico.append("O primeiro e o último passo devem ser, em qualquer ordem, a expressão inicial e a expressão objetivo.")
        return False, "O primeiro e o último passo devem ser, em qualquer ordem, a expressão inicial e a expressão objetivo.", ["Passos iniciais/finais inválidos"], historico
    # Avalia cada transição
    transicoes_validas = True
    for i in range(len(exprs) - 1):
        expr_atual = exprs[i]
        expr_prox = exprs[i+1]
        regras_encontradas = identificar_regra_aplicada(expr_atual, expr_prox)
        if not regras_encontradas:
            transicoes_validas = False
            msg = f"Transformação inválida do passo {i+1} para o {i+2}: {formatar_expressao(expr_atual)} → {formatar_expressao(expr_prox)}"
            erros_transicao.append(msg)
            historico.append(msg)
            # Todos os passos seguintes são inválidos
            for j in range(i+1, len(exprs)-1):
                msg2 = f"Passo {j+1} para {j+2} não avaliado devido a erro anterior."
                erros_transicao.append(msg2)
                historico.append(msg2)
            break
        else:
            msg = f"Passo {i+1} → {i+2}: {formatar_expressao(expr_atual)} → {formatar_expressao(expr_prox)} | Regra(s): {', '.join(regras_encontradas)}"
            historico.append(msg)
    if not transicoes_validas:
        historico.append("Há erro(s) em transições de passos.")
        return False, "Há erro(s) em transições de passos.", erros_transicao, historico
    # Se todos os passos são válidos, verifica se a conclusão é equivalente ao objetivo
    equivalente, _ = verificar_equivalencia(exprs[-1], processar_entrada_usuario(expr_objetivo)[0])
    if equivalente:
        historico.append("Demonstração correta! Todas as transições são válidas e a conclusão é equivalente ao objetivo.")
        return True, None, None, historico
    else:
        historico.append("A conclusão não é equivalente ao objetivo.")
        return False, "A conclusão não é equivalente ao objetivo.", ["Conclusão inválida"], historico