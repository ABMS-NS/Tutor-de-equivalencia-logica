from src.especialista.avaliador import avaliar_passos, avaliar_resposta_final

def main():
    print("="*60)
    print("           AVALIADOR DE PASSOS DE EQUIVALÊNCIA LÓGICA")
    print("="*60)
    print("Informe a expressão inicial (situação de partida):")
    expr_inicial = input("Expressão inicial: ").strip()
    print("Informe a expressão objetivo (meta):")
    expr_objetivo = input("Expressão objetivo: ").strip()
    print("\nDigite cada passo da solução, um por linha, começando pela expressão inicial e terminando na expressão objetivo.")
    print("Quando terminar, digite 'finalizar' e pressione Enter.\n")

    passos = []
    while True:
        linha = input(f"Passo {len(passos)+1}: ").strip()
        if linha.lower() == "finalizar":
            break
        passos.append(linha)

    if len(passos) < 2:
        print("Por favor, forneça pelo menos dois passos (inicial e final).")
        return

    # Permite que o aluno comece com qualquer uma das duas expressões (inicial ou objetivo)
    if not (
        (passos[0] == expr_inicial and passos[-1] == expr_objetivo) or
        (passos[0] == expr_objetivo and passos[-1] == expr_inicial)
    ):
        print("O primeiro e o último passo devem ser, em qualquer ordem, a expressão inicial e a expressão objetivo informadas.")
        return

    passos_ok, erro_passos, _ = avaliar_passos(passos)
    # Sempre compara o último passo com a expressão objetivo (independente da ordem)
    final_ok, erro_final = avaliar_resposta_final(passos[-1], expr_objetivo) or avaliar_resposta_final(passos[-1], expr_inicial)

    print("\nResultado da avaliação:")
    if passos_ok and final_ok:
        print("Solução correta. Todos os passos e a resposta final estão corretos.")
    elif not passos_ok and final_ok:
        print("Solução incorreta: a resposta final está correta, mas há erro nos passos.")
        print(f"Detalhe: {erro_passos}")
    else:
        print("Solução incorreta: a resposta final não é equivalente à correta.")
        if not passos_ok:
            print(f"Além disso, há erro nos passos: {erro_passos}")
        elif erro_final:
            print(f"Detalhe: {erro_final}")

if __name__ == "__main__":
    main()