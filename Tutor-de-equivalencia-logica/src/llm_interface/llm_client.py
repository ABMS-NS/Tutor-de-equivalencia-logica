"""
Cliente para comunicação com múltiplas APIs de LLM (Gemini e OpenRouter).
"""

import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configuração do Cliente Gemini ---
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    else:
        print("Aviso: Chave da API Gemini não encontrada no .env. Funções do Gemini estarão desabilitadas.")
except Exception as e:
    print(f"Erro ao configurar a API Gemini: {e}")

# --- Configuração do Cliente OpenRouter ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if OPENROUTER_API_KEY:
    openrouter_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    # Headers opcionais para ranking no OpenRouter
    openrouter_headers = {
        "HTTP-Referer": os.getenv("YOUR_SITE_URL", ""),
        "X-Title": os.getenv("YOUR_SITE_NAME", ""),
    }
else:
    openrouter_client = None
    print("Aviso: Chave da API OpenRouter não encontrada no .env. Funções do OpenRouter estarão desabilitadas.")


# --- Constantes de Prompts ---

PROMPT_SISTEMA_DICAS_GEMINI = """
Você é um tutor de lógica proposicional amigável e encorajador.
Seu objetivo é ajudar o aluno a aprender, não dar a resposta diretamente.
Forneça dicas contextuais e graduais. Se o aluno errar, explique o conceito por trás do erro de forma simples.
Se o aluno pedir a resposta, negue educadamente e ofereça uma pista.
Mantenha as respostas curtas e focadas na dúvida do aluno.
"""

def obter_dica_gemini(pergunta, resposta_aluno=""): 
    """
    Obtém uma dica do Gemini para uma questão de lógica.

    Args:
        pergunta (str): O enunciado da questão que o aluno está tentando resolver.
        resposta_aluno (str, optional): A tentativa de resposta do aluno.

    Returns:
        str: A dica gerada pelo modelo ou uma mensagem de erro.
    """
    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError("A chave da API do Google Gemini não está configurada. Defina a variável de ambiente GEMINI_API_KEY.")

    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=PROMPT_SISTEMA_DICAS_GEMINI
        )

        prompt_completo = f"A questão é: '{pergunta}'."
        if resposta_aluno:
            prompt_completo += f" Minha tentativa de resposta foi: '{resposta_aluno}'. Por favor, me dê uma dica."
        else:
            prompt_completo += " Por favor, me dê uma dica para começar."

        response = model.generate_content(prompt_completo)
        return response.text
    except Exception as e:
        return f"Erro ao chamar a API Gemini: {e}"


def avaliar_traducao_logica(enunciado, resposta_aluno, gabarito):
    """
    Avalia se a tradução da linguagem natural para a lógica proposicional feita pelo aluno
    é fidedigna e idêntica ao gabarito, considerando fidelidade ao enunciado e à estrutura lógica.
    Retorna 'Correto!' se estiver correta, ou 'Incorreto!' e uma explicação breve do erro.

    Args:
        enunciado (str): A sentença em linguagem natural.
        resposta_aluno (str): A fórmula lógica proposta pelo aluno.
        gabarito (str): A fórmula lógica correta (gabarito).

    Returns:
        str: 'Correto!' se a tradução for fiel e idêntica, ou 'Incorreto! <explicação>' caso contrário.
    """
    if not os.environ.get("OPENROUTER_API_KEY"):
        return "Erro: Cliente OpenRouter não configurado. Verifique a chave da API."

    prompt = f"""
    Você é um avaliador especialista em lógica proposicional. Avalie a tradução do aluno para lógica simbólica.
    Compare a resposta do aluno com o gabarito e o enunciado. Considere:
    - A tradução deve ser fiel ao enunciado e idêntica ao gabarito (mesma estrutura e operadores).
    - Pequenas variações de notação são aceitáveis apenas se não alterarem o sentido lógico.
    - Se a tradução do aluno estiver correta e idêntica ao gabarito, responda apenas: 'Correto!'.
    - Se estiver incorreta, responda: 'Incorreto!' e, em UMA frase curta, explique o principal erro da tradução (ex: operador errado, proposição trocada, estrutura diferente, etc).

    Enunciado: "{enunciado}"
    Resposta do Aluno: "{resposta_aluno}"
    Gabarito: "{gabarito}"
    """

    try:
        completion = openrouter_client.chat.completions.create(
            extra_headers=openrouter_headers,
            model="mistralai/devstral-small:free",
            messages=[
                {"role": "system", "content": "Você é um especialista em lógica proposicional. Avalie traduções de linguagem natural para lógica simbólica. Responda apenas 'Correto!' ou 'Incorreto!' seguido de uma explicação breve."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=50
        )
        resposta = completion.choices[0].message.content.strip()
        if resposta.startswith("Correto!"):
            return "Correto!"
        elif resposta.startswith("Incorreto!"):
            return resposta
        else:
            print(f"Resposta inesperada do modelo de avaliação: '{resposta}'")
            return "Incorreto! Tradução não corresponde ao gabarito."
    except Exception as e:
        return f"Erro ao chamar a API OpenRouter: {e}"
    
# Adicione após a função obter_dica_gemini (linha 134):

PROMPT_SISTEMA_EXPLICACAO_GEMINI = """
Você é um tutor especializado em lógica proposicional. 
Sua função é explicar de forma didática e detalhada os resultados das avaliações.
Seja claro, educativo e incentive o aprendizado. Use exemplos quando necessário.
Explique erros de forma construtiva e sugira correções específicas.
"""

def obter_explicacao_avaliacao(prompt_avaliacao):
    """
    Obtém uma explicação detalhada da avaliação do Gemini.
    
    Args:
        prompt_avaliacao (str): O prompt completo com dados da avaliação
        
    Returns:
        str: A explicação gerada pelo modelo ou uma mensagem de erro.
    """
    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError("A chave da API do Google Gemini não está configurada.")

    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=PROMPT_SISTEMA_EXPLICACAO_GEMINI
        )
        
        response = model.generate_content(prompt_avaliacao)
        return response.text
    except Exception as e:
        return f"Erro ao chamar a API Gemini: {e}"
    
if __name__ == "__main__":
    # Exemplo de teste com S1 e S2
    enunciado = "Verifique se as duas sentenças seguintes (S1 e S2) são equivalentes:\nS1: Se chove ou neva, então o chão fica molhado.\nS2: Se o chão está seco, então não choveu e não nevou."
    resposta_aluno = "S1: (p ∨ q) → r | S2: ¬r → (¬p ∧ ¬q)"
    gabarito = "S1: (p ∨ q) → r | S2: ¬r → (¬p ∧ ¬q)"
    print("Testando avaliação de tradução lógica com S1 e S2...")
    resultado = avaliar_traducao_logica(enunciado, resposta_aluno, gabarito)
    print("Saída do modelo:")
    print(resultado)