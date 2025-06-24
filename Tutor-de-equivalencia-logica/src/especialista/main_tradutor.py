"""
Arquivo principal para executar o tradutor de linguagem natural para lógica proposicional.
"""

# Importa a classe principal do módulo do tradutor.
# O ponto (.) indica que o 'tradutorspacy.py' está no mesmo diretório.
from .tradutorspacy import Lista_Frases

def iniciar_traducao():
    """
    Função que gerencia a interface de linha de comando para o tradutor.
    """
    print("=" * 60)
    print("      TRADUTOR DE LINGUAGEM NATURAL PARA LÓGICA")
    print("=" * 60)
    print("Digite uma ou mais sentenças em uma única linha.")
    print("Para sair, digite 'sair' ou pressione Ctrl+C.")
    print("-" * 60)

    while True:
        try:
            # Pede ao usuário para inserir o texto a ser traduzido
            texto_natural = input("Digite a sentença: ")

            # Condição para encerrar o programa
            if texto_natural.strip().lower() == 'sair':
                print("Encerrando o tradutor.")
                break
            
            # Garante que a entrada não está vazia
            if not texto_natural.strip():
                continue

            # Cria a instância de Lista_Frases.
            # O construtor (__init__) da classe já executa toda a lógica
            # de tradução e impressão dos resultados.
            Lista_Frases(texto_natural)
            print("-" * 60)

        except (KeyboardInterrupt, EOFError):
            # Lida com o encerramento pelo usuário (Ctrl+C)
            print("\nTradução encerrada.")
            break

if __name__ == "__main__":
    iniciar_traducao()