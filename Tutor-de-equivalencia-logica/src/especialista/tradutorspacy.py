#CASO OCORRA ALGUM ERRO DE PRINT NO TERMINAL, PODE SER NORMAL, APENAS POR CAUSA DE UTF-8 OU ALGO DO TIPO
#MAS AO EXIBIR EM ALGUM EDITOR DE TEXTO OU NAVEGADOR, VAI ESTAR FORMATADO NORMALMENTE

#O símbolo ";" na linguagem natural muitas vezes separa duas ideias ou eventos que precisam ser avaliados de maneira independente
#, indicando que há duas partes distintas
import spacy
import unicodedata
import re

nlp = spacy.load("pt_core_news_md")
exclusivo = [", mas não ambos", "ou então"]

operadores_associativos = ["∧", "∨"]

operadores_nao_associativos = ["⊻", "→", "↔"]

pontuacao_final = ["?", ".", "!", ";"]

frase_sem_parenteses = ["p ∨ q", "¬ p ∨ q", "p ∨ ¬ q", "¬ p ∨ ¬ q", "p ∧ q", "¬ p ∧ q", "p ∧ ¬ q", "¬ p ∧ ¬ q"]

#Variável utilizada na criação dos átomos no método de tradução
letra_minuscula = 96 + 15# com isso, começa no "p" e assim segue, p, q, r, s...

class Contador():
    def __init__(self, valor = 0):
        self.valor = valor

    def incrementar(contador):
        contador.valor += 1

class Frase():
    def __init__(self, frase):
        self.frase = limpar_texto(frase) #Existe uma coisa chamada de espaços não quebráveis, que são meio
        #que aleatórios e podem vir principalmente de textos copiados, então por precaução, já faço
        #esse tratamento acima no frase.replace("\xa0", " ")
        self.frase_doc = nlp(self.frase)        
        self.frase_tokenizada = [token.text for token in self.frase_doc]
        #self.frase_doc = [] #Não lembro a serventia disso, mas vou deixar aqui
        self.condicional_salva = None
        self.ultimo_simbolo = None
        self.condicao_atual = None #Saber a condicao atual que vai ser adicionada a frase logica para ser comparada aos outros simbolos
        self.chamar_parenteses = False #bool que vai ditar aonde os parenteses serão chamados!
        self.virgula_parenteses = False #bool para controlar quando o parentese foi chamado através de uma vírgula
        self.parenteses = False #bool pra saber se o parentese foi usado ou não ao atribuir algo para o frase.ultimo_simbolo
        self.frase_dividida = [""]
        self.frase_dividida_normalizada = []
        self.letra_frase_dividida = []
        self.frase_logica = []
        self.resultado = None
        self.tipo = 0 #Indica o tipo da frase que está sendo traduzida, para tratamentos futuros.
        #self.argumentos_logica = ["A"] #A, B, por exemplo. Lembrar que só está sendo aplicado no tipo 1 até o momento.
        #self.argumentos_divididos_logica = [[]]
        #self.cos_bool = 0 #Saber se pode ativar ou não a aproximação por cossenos

    


class Lista_Frases(Frase):

    def __init__(self, texto):
        self.texto = limpar_texto(texto)
        self.frase = []

        texto_len = len(texto)
        sentenca = ""

        print(self.texto)

        for char in texto:
            sentenca += char

            if char in pontuacao_final:
                #print(f"SENTENÇA QUE VAI É: {sentenca.encode('utf-8').decode('utf-8')}")
                #sentenca = sentenca.encode('utf-8').decode('utf-8')
                f1 = Frase(sentenca.strip())
                self.frase.append(f1)
                sentenca = ""
                natural_para_proposicional(f1)

        cont_char = 97 + 15 #Letra p pela tabela ascii

        for frase in self.frase:
            i = 0

            if frase.tipo == 1: #Quando a implicação é ao contrário, "O unicórnio é mágico se tem chifre"
                implicacao = 0
                while True:
                    print("Tamo no while")
                    if frase.frase_logica[implicacao] == "→": #Joga a implicação pro final da frase e depois joga o que estava
                        del frase.frase_logica[implicacao]    #antes da implicação para o fim de frase.
                        frase.frase_logica.append("→")
                        break
                    elif frase.frase_logica[implicacao] in pontuacao_final:
                        print("Erro, implicação invalida")
                    else: 
                        implicacao += 1

                print(frase.frase_logica)

                item = 0
                while item != implicacao:
                    if(frase.frase_logica[0].isalpha()):
                        #frase.frase_dividida_normalizada.append(frase.frase_dividida_normalizada[0])
                        frase.frase_dividida.append(frase.frase_dividida[0])
                        #frase.letra_frase_dividida.append(frase.letra_frase_dividida[0])

                        #del frase.frase_dividida_normalizada[0]
                        del frase.frase_dividida[0]
                        #del frase.letra_frase_dividida[0]

                    frase.frase_logica.append(frase.frase_logica[0])
                    del frase.frase_logica[0]

                    item += 1


                iterator = 0
                cont_char_2 = 97 + 15
                # while iterator < len(frase.frase_logica):
                #     if frase.frase_logica[iterator].isalpha():
                #         frase.frase_logica[iterator] = chr(cont_char_2)
                #         cont_char_2 += 1
                #     iterator += 1

        

            while i < len(frase.frase_dividida):
                doc = nlp(frase.frase_dividida[i])
                frase.frase_dividida[i] = " ".join(
                    [token.text for token in doc if token.pos_ not in {"ADV", "PUNCT", "CCONJ"}]
                ) 

                doc = nlp(frase.frase_dividida[i])
                
                frase.frase_dividida_normalizada.append(
                    nlp(" ".join([token.lemma_.lower() for token in doc if not token.is_stop]))
                ) #Já salva com o tipo de dado do spacy

                frase.letra_frase_dividida.append(cont_char)
                cont_char += 1

                i+= 1

        i = len(self.frase) - 1
        while i >= 0:

            j = len(self.frase[i].frase_dividida_normalizada) - 1
            while j >= 0:

                comparador = self.frase[i].frase_dividida_normalizada[j]
                
                #print(f"comparador: {comparador}, type : {type(comparador)}")
                
                x = i
                y = j - 1
                while x >= 0:
                    while y >= 0:
                        #print(f"Atual : {self.frase[x].frase_dividida_normalizada[y]}, tipo : {type(self.frase[x].frase_dividida_normalizada[y])}")       
                        if comparador.similarity(self.frase[x].frase_dividida_normalizada[y]) >= 0.95:
                            self.frase[i].frase_dividida_normalizada[j] = self.frase[x].frase_dividida_normalizada[y]
                            self.frase[i].frase_dividida[j] = self.frase[x].frase_dividida[y]
                            self.frase[i].letra_frase_dividida[j] = self.frase[x].letra_frase_dividida[y]

                        y -= 1 # Percorre a linha da direita para a esquerda
                    x -= 1 # Passa para a linha acima
                    if x >= 0:
                        y = len(self.frase[x].frase_dividida_normalizada) - 1 # Reseta a coluna para o final da linha acima
                j -= 1
            i -= 1

        print("Entrando no teste")
        i = 0
        n = len(self.frase) - 1

        while i < n:
            y = len(self.frase[i].frase_logica)
            x = 0
            substituir = 0
            while x < y:
                if self.frase[i].frase_logica[x].isalpha():
                    self.frase[i].frase_logica[x] = chr(self.frase[i].letra_frase_dividida[substituir])
                    substituir += 1
                
                x += 1
            i += 1

        print("Inicio do texto")
        print("-----------------------------------------------")
        for sentenca in self.frase:
            print(sentenca.frase)
                
            for i in sentenca.frase_logica:
                print(i, end = " ")
            print("\n")

            cont = 0

            print("")
            while cont < len(sentenca.frase_dividida):
                print(f"{chr(sentenca.letra_frase_dividida[cont])}: {sentenca.frase_dividida[cont]}\n")
                print(f"{chr(sentenca.letra_frase_dividida[cont])}: {sentenca.frase_dividida_normalizada[cont]}\n")
                cont += 1
            print("")
            print("-----------------------------------------------")

            # for i in sentenca.frase_dividida:
            #     print(f"{chr(96 + 16 + cont)}: {i}")
            #     cont += 1
            # print("")
            # print("")

class Conferir():
    def __init__(self):
        self.indice = None
        self.cos = None

def conferir(frase, frase_conferir):

    lista = []
    frase1 = nlp(frase_conferir)

    for indice, item in enumerate(frase.frase_conferir):
        frase2 = nlp(item)
        
        cos = frase1.similarity(frase2)
        if(cos >= 0.8):
            obj = Conferir()
            obj.indice = indice
            obj.cos = cos
            lista.append(obj)

        if(lista):
            # Encontrando o objeto com o maior valor de 'cos'
            obj_maior_cos = max(lista, key=lambda obj: obj.cos)
            return obj_maior_cos

        else: return None

def trata_virgula(frase):
    print("VIRGULAAAAAAAAAAA")
    print(frase.frase_logica)

    print(frase.ultimo_simbolo)
    print(frase.condicao_atual)
    print(f"CHAMAR PARENTESES = {frase.chamar_parenteses}")
    print(f"VIRGULA PARENTESES = {frase.virgula_parenteses}")
    #frase.frase_logica = list(frase.frase_logica)
    #Associativos == ^ e v
    #!Associativos == ->, <-> e _v_

    # a ^ b v (->) (a ^ b) v c ^ d

    if frase.condicao_atual == None or frase.ultimo_simbolo == None:
        frase.virgula_parenteses = False

    elif frase.condicao_atual in operadores_associativos and frase.ultimo_simbolo in operadores_associativos and frase.condicao_atual != frase.ultimo_simbolo:

        print("Simbolos diferentes")

        print(f"frase antes {frase.frase_logica}")

        if frase.chamar_parenteses == True:

            frase.frase_logica.append(")")
            n = len(frase.frase_logica) - 2 #-2 para não contar com o ")" que eu acabo de fazer o append
            while n >= 0:
                print(f"N = {n}")
                if n == 0:
                    frase.frase_logica.insert(0, "(")
                
                elif frase.frase_logica[n] == ")":
                    while frase.frase_logica[n] != "(":
                        n -= 1
                    continue

                elif frase.frase_logica[n].isalpha() or frase.frase_logica[n] == "¬":
                    pass

                elif frase.frase_logica[n] != frase.ultimo_simbolo:
                    frase.frase_logica.insert(n + 1, "(")
                    break

                n -= 1
            frase.ultimo_simbolo = None
            frase.condicao_atual = None
            frase.parenteses = True
            frase.chamar_parentese = False

        elif frase.virgula_parenteses == True:
            print("TA AONDE NAO DEVIAAAAAAAAAA")

            n = len(frase.frase_logica) - 2 #-2 para não contar com o ")" que eu acabo de fazer o append
            while n >= 0:
                #print(f"N = {n}")
                if n == 0:
                    break
                
                elif frase.frase_logica[n] == ")":
                    while frase.frase_logica[n] != "(":
                        n -= 1
                    continue

                elif frase.frase_logica[n].isalpha() or frase.frase_logica[n] == "¬":
                    pass

                elif frase.frase_logica[n] != frase.ultimo_simbolo:
                    frase.frase_logica.insert(n + 1, "(")
                    frase.frase_logica.append(")")
                    break

                n -= 1

            frase.frase_logica.append(")")
            n = len(frase.frase_logica) - 2 #-2 para não contar com o ")" que eu acabo de fazer o append
            while n >= 0:
                #print(f"N = {n}")
                if n == 0:
                    frase.frase_logica.insert(0, "(")
                
                elif frase.frase_logica[n] == ")":
                    while frase.frase_logica[n] != "(":
                        n -= 1
                    continue

                elif frase.frase_logica[n].isalpha() or frase.frase_logica[n] == "¬":
                    pass

                elif frase.frase_logica[n] != frase.ultimo_simbolo:
                    frase.frase_logica.insert(n + 1, "(")
                    break

                n -= 1

            frase.virgula_parenteses = False

        elif frase.chamar_parenteses == False:
            frase.chamar_parenteses = True

        print(f"frase depois {frase.frase_logica}")

    elif frase.condicao_atual in operadores_associativos and frase.ultimo_simbolo in operadores_associativos and frase.condicao_atual == frase.ultimo_simbolo:
        print("SIMBOLOS IGUAIS")
        print(frase.frase_logica)

        print(frase.ultimo_simbolo)
        print(frase.condicao_atual)
        print(f"CHAMAR PARENTESES = {frase.chamar_parenteses}")
        print(f"VIRGULA PARENTESES = {frase.virgula_parenteses}")

        if frase.virgula_parenteses == True:
            n = len(frase.frase_logica) - 2 #-2 para não contar com o ")" que eu acabo de fazer o append
            while n >= 0:
                #print(f"N = {n}")
                if n == 0:
                    break
                
                elif frase.frase_logica[n] == ")":
                    while frase.frase_logica[n] != "(":
                        n -= 1
                    continue

                elif frase.frase_logica[n].isalpha() or frase.frase_logica[n] == "¬":
                    pass

                elif frase.frase_logica[n] != frase.ultimo_simbolo:
                    frase.frase_logica.insert(n + 1, "(")
                    frase.frase_logica.append(")")
                    break

                n -= 1

            frase.frase_logica.append(")")

            n = len(frase.frase_logica) - 2 #-2 para não contar com o ")" que eu acabo de fazer o append

            while n >= 0:
                #print(f"N = {n}")
                if n == 0:
                    frase.frase_logica.insert(0, "(")
                
                elif frase.frase_logica[n] == ")":
                    while frase.frase_logica[n] != "(":
                        n -= 1
                    continue

                elif frase.frase_logica[n].isalpha() or frase.frase_logica[n] == "¬":
                    pass

                elif frase.frase_logica[n] == frase.ultimo_simbolo:
                    frase.frase_logica.insert(n + 1, "(")
                    break

                n -= 1
            
            frase.virgula_parenteses = False
            print(f"fraseeeee {frase.frase_logica}")

    elif frase.condicao_atual in operadores_associativos and frase.ultimo_simbolo in operadores_nao_associativos:
        frase.condicao_atual = None
        frase.ultimo_simbolo = frase.ultimo_simbolo
        frase.chamar_parenteses = True

    
    elif frase.condicao_atual in operadores_nao_associativos and frase.ultimo_simbolo in operadores_associativos:
        
        frase.frase_logica.append(")")
        n = len(frase.frase_logica) - 2 #-2 para não contar com o ")" que eu acabo de fazer o append

        while n >= 0:
            print(f"n = {n}")
            if n == 0:
                frase.frase_logica.insert(0, "(")

            elif frase.frase_logica[n] == ")":
                while frase.frase_logica[n] != "(":
                    n -= 1    
                continue        

            elif frase.frase_logica[n].isalpha() or frase.frase_logica[n] == "¬":
                pass

            elif frase.frase_logica[n] != frase.ultimo_simbolo:
                frase.frase_logica.insert(n + 1, "(")
                break

            n -= 1
        frase.ultimo_simbolo = None
        frase.condicao_atual = None
        frase.parenteses = True


    elif frase.condicao_atual in operadores_nao_associativos and frase.ultimo_simbolo in operadores_nao_associativos and frase.condicao_atual != frase.ultimo_simbolo:
        pass #ainda não sei o que fazer com isso

    elif frase.condicao_atual in operadores_nao_associativos and frase.ultimo_simbolo in operadores_nao_associativos and frase.condicao_atual == frase.ultimo_simbolo:
        pass #ainda não sei o que fazer com isso

    #frase.frase_logica = " ".join(frase.frase_logica)

def natural_para_proposicional(frase):

    #frase.frase_doc = nlp(frase.frase)

    #print(f"FRASE.DOC = {frase.frase_doc}")

    #frase.frase_tokenizada = [token.text for token in frase.frase_doc]

    #Essa passagem é por referência, ou seja, qualquer modificação em tokens vai refletir
    #em frase.frase_tokenizada
    #tokens = frase.frase_tokenizada # -> eh esse daqui
    tokens = frase.frase_doc

    print("")
    for token in tokens:
        print(f"{token.text} → {token.dep_} (POS: {token.pos_})")
    print("")

    #global letra_minuscula

    #FOR ABAIXO UTILIZADO PARA FINS DE DEBUG
    #print(tokens)
    #------
    #Esse indice serve para saber a posicao que eu vou adicionar na string que representa a letra minuscula "a", por exemplo, a cada += 1, significa
    #que a mesma está indo para uma outra condicional (ou letra minuscula) na tradução da lógica proposicional
    i = Contador()
    
    #basicamente o que seria um "a - 1" da tabela ascii
    #global letra_minuscula
    letra_minuscula = 96 + 15
    letra_maiuscula = 65 # A na tabela ascii

    #j = Contador()
    j = Contador()

    #controla a #self.argumentos_divididos_logica    
    #k = Contador()
    tokens_len = len(tokens)
    #print(f"Jn = {tokens_len}")
    while j.valor < tokens_len:
        #print(j)
        #if (tokens[j.valor].dep_ == "advmod" and tokens[j.valor + 1].dep_ == "punct") or (tokens[j.valor].dep_ == "punct" and j.valor < tokens_len - 1 and tokens[j.valor + 1].dep_ == "advmod"):
        
        print(f"Len tokens = {len(tokens)}")       
        print(f"J.valor = {j.valor}")
        print(f"len frase.frase_logica = {len(frase.frase_logica)}")
        print(frase.frase_logica)
        
        if j.valor == 0:
            if tokens[0].pos_ == "CCONJ":
                j.valor += 1
                if tokens[1].text == ",":
                    j.valor += 1
        
        if (tokens[j.valor].dep_ == "advmod" and tokens[j.valor + 1].dep_ == "punct"):
            j.valor += 1
            #Pular quando tiver por exemplo
            #"Ora, "
            #"Logo: "
        # elif tokens[j.valor].pos_ == "ADJ" and frase.frase_logica[-1].isalpha:
        #     pass

        elif tokens[j.valor].text.lower() in pontuacao_final:

            letra_minuscula += 1
            
            frase.frase_logica.append(chr(letra_minuscula))
            #frase.argumentos_divididos_logica[k.valor].append(chr(letra_minuscula))

            frase.resultado = ' '.join(frase.frase_logica)

            print("ENTROU NO PONTO FINAL")
            print(f"simbolo atual = {frase.condicao_atual}")
            print(f"ultimo simbolo = {frase.ultimo_simbolo}")
            if not frase.resultado in frase_sem_parenteses:
                if frase.ultimo_simbolo and frase.ultimo_simbolo in operadores_associativos: #frase.condicao_atual != NULL
                    print("ENTROU NO IF DO PONTO FINAL")
                    print(f"frase logica antes = {frase.frase_logica}")
                    frase.frase_logica.append(")")
                    print(f"frase logica depois = {frase.frase_logica}")

                    n = len(frase.frase_logica) - 2 #-2 para não contar com o ")" que eu acabo de fazer o append

                    while n >= 0:
                        

                        if frase.frase_logica[n].isalpha() or frase.frase_logica[n] == "¬":
                            pass
                        
                        elif frase.frase_logica[n] != frase.ultimo_simbolo:
                            frase.frase_logica.insert(n + 1, "(")
                            break

                        n -= 1

                    frase.ultimo_simbolo = None
                    frase.condicao_atual = None

        elif tokens[j.valor].text.lower() == "se":

            if(j.valor + 3) <= tokens_len:
                teste = " ".join([token.text for token in tokens[j.valor:j.valor + 4]]) #GPT ME GEROU ESSE E DISSE QUE AGORA ESTARÁ CORRETO
            else:
                teste = "paia"
            
            if (teste.lower() == "se e somente se"):
                letra_minuscula += 1
                frase.frase_logica.append(chr(letra_minuscula))
                frase.condicao_atual = "↔"
                trata_virgula(frase)
                frase.frase_logica.append("↔")
                j.valor += 3
                frase.frase_dividida.append("")
                i.valor+= 1    
                frase.ultimo_simbolo, frase.parenteses = (None, False) if frase.parenteses == True else ("↔", False)

            elif(tokens[0].text.lower() == "se"):
                frase.condicional_salva = "→"

            else:
                #print("ESSE") #nao foi
                letra_minuscula += 1
                frase.frase_logica.append(chr(letra_minuscula))
                frase.condicao_atual = "→"
                trata_virgula(frase)
                #frase.argumentos_divididos_logica[k.valor].append(chr(letra_minuscula))
                frase.frase_logica.append("→")
                frase.frase_dividida.append("")
                i.valor+= 1                  
                j.valor += 1
                #O tipo da frase vai indicar alguma nuance que a frase possa ter e o software detectar e reorganizar
                #a ordem dos átomos
                frase.tipo = 1
                #frase.argumentos_logica.append("→")
                #letra_maiuscula += 1
                #frase.argumentos_logica.append(chr(letra_maiuscula))
                #frase.argumentos_divididos_logica#.append([])
                #k.valor += 1
                frase.ultimo_simbolo, frase.parenteses = (None, False) if frase.parenteses == True else ("→", False)

        elif tokens[j.valor].text.lower() == "não":
            frase.frase_logica.append("¬")    
            #frase.argumentos_divididos_logica[k.valor].append("¬")
            #print(f"FRASE = {#frase.argumentos_divididos_logica[k.valor]}")

        elif tokens[j.valor].text == ",":
            if frase.condicional_salva != "→":
                if tokens[j.valor + 1].text.lower() in ["logo", "então"]:
                    #print("ESSE")                    
                    letra_minuscula += 1
                    frase.frase_logica.append(chr(letra_minuscula))
                    frase.condicao_atual = "→"
                    trata_virgula(frase)
                    frase.frase_logica.append("→")  
                    frase.frase_dividida.append("")
                    i.valor+= 1                  
                    j.valor += 1
                    frase.ultimo_simbolo, frase.parenteses = (None, False) if frase.parenteses == True else ("→", False)                    

                elif tokens[j.valor + 1].text.lower() == "ou": #No futuro isso pode gerar um bug do caramba, mas por enquanto tamo ae
                    frase.virgula_parenteses = True
                    frase.condicional_salva = "∨"
                    j.valor += 1

                    letra_minuscula += 1
                    frase.frase_logica.append(chr(letra_minuscula))
                    frase.condicao_atual = frase.condicional_salva
                    trata_virgula(frase)   
                    frase.frase_logica.append(frase.condicional_salva)
                    frase.ultimo_simbolo, frase.parenteses = (None, False) if frase.parenteses == True else (frase.condicional_salva, False)
                    frase.condicional_salva = None
                    frase.frase_dividida.append("")
                    i.valor+= 1
                    frase.frase_dividida[i.valor] += tokens[j.valor].text

                elif tokens[j.valor + 1].text.lower() == "e" or tokens[j.valor + 1].pos_ == "ADJ" or tokens[j.valor + 1].pos_ == "VERB":

                    frase.virgula_parenteses = True if tokens[j.valor + 1].text.lower() == "e" else False

                    frase.condicional_salva = "∧"
                    j.valor += 1
                    #if tokens[j.valor + 1].text.lower() == "e":
                    letra_minuscula += 1
                    frase.frase_logica.append(chr(letra_minuscula))
                    frase.condicao_atual = frase.condicional_salva
                    trata_virgula(frase)
                    frase.frase_logica.append(frase.condicional_salva)
                    frase.ultimo_simbolo, frase.parenteses = (None, False) if frase.parenteses == True else (frase.condicional_salva, False)
                    frase.condicional_salva = None
                    # print(f"FRASE_DIVIDIDA = {frase.frase_dividida[i.valor]}")
                    # print(f"FRASE_LOGICA = {frase.frase_logica}")
                    frase.frase_dividida.append("")
                    i.valor+= 1
                    frase.frase_dividida[i.valor] += tokens[j.valor].text
                    #if tokens[j.valor].pos_ == "ADJ" or tokens[j.valor + 1].pos_ == "VERB":
                    #    j.valor += 1

                
                else:
                    letra_minuscula += 1

                    frase.frase_logica.append(chr(letra_minuscula))
                    frase.condicao_atual = "∧"
                    trata_virgula(frase)
                    frase.frase_logica.append("∧") #AQUI
                    frase.ultimo_simbolo, frase.parenteses = (None, False) if frase.parenteses == True else ("∧", False)                    
                    #frase.argumentos_divididos_logica[k.valor].append(chr(letra_minuscula))
                    #frase.argumentos_divididos_logica[k.valor].append("∧")
                    frase.frase_dividida.append("")
                    i.valor+= 1

            else: #elif tokens[j.valor + 1] != "e" and tokens[j.valor + 1] != "ou": Tentar trabalhar com isso aqui
                #if frase.frase_dividida[i.valor]:
                if tokens[j.valor + 1].text.lower() == "ou": #No futuro isso pode gerar um bug do caramba, mas por enquanto tamo ae
                    frase.virgula_parenteses = True
                    frase.condicional_salva = "∨"
                    j.valor += 1
                elif tokens[j.valor + 1].text.lower() == "e" or tokens[j.valor + 1].pos_ == "ADJ" or tokens[j.valor + 1].pos_ == "VERB":
                    frase.virgula_parenteses = True if tokens[j.valor + 1].text.lower() == "e" else False
                    frase.condicional_salva = "∧"
                    j.valor += 1
                    #if tokens[j.valor + 1].text.lower() == "e":
                        
                letra_minuscula += 1
                frase.frase_logica.append(chr(letra_minuscula))
                frase.condicao_atual = frase.condicional_salva
                #print(f"ANTES = {frase.frase_logica}")
                trata_virgula(frase)
                #print(f"DEPOIS = {frase.frase_logica}")
                frase.frase_logica.append(frase.condicional_salva)
                #print("CAIU AQUI MEXMOOOOOOOO")
                print(frase.parenteses)
                frase.ultimo_simbolo, frase.parenteses = (None, False) if frase.parenteses == True else (frase.condicional_salva, False)            
                frase.condicional_salva = None
                # print(f"FRASE_DIVIDIDA = {frase.frase_dividida[i.valor]}")
                # print(f"FRASE_LOGICA = {frase.frase_logica}")
                frase.frase_dividida.append("")
                i.valor+= 1
                frase.frase_dividida[i.valor] += tokens[j.valor].text
                #if tokens[j.valor].pos_ == "ADJ" or tokens[j + 1].pos_ == "VERB":
                #    j.valor += 1

        elif tokens[j.valor].text.lower() == "e":
            letra_minuscula += 1
            frase.frase_logica.append(chr(letra_minuscula))
            frase.condicao_atual = "∧"
            trata_virgula(frase)            
            frase.frase_logica.append("∧") #AQUI
            frase.ultimo_simbolo, frase.parenteses = (None, False) if frase.parenteses == True else ("∧", False) 
            #frase.argumentos_divididos_logica[k.valor].append(chr(letra_minuscula))
            #frase.argumentos_divididos_logica[k.valor].append("∧")
            frase.frase_dividida.append("")
            i.valor+= 1

        elif tokens[j.valor].text.lower() == "ou":
            new_frase = ""
            virgula = False
            if frase.condicional_salva == None and not frase.frase_dividida[0]: #frase dividida == NULL
                cont = 0
                for token in tokens[j.valor + 1:]:
                    if(token.text != "," and token.text.lower() != "ou"):
                        new_frase += token.text + " "
                        cont += 1
                    if token.text.lower() == "ou":
                        j.valor += cont
                        letra_minuscula += 1
                        frase.frase_logica.append(chr(letra_minuscula))
                        frase.frase_dividida[i.valor] += new_frase
                        frase.frase_dividida.append("")
                
                        #frase.argumentos_divididos_logica[k.valor].append(chr(letra_minuscula))
                        i.valor += 1
                        break #coloquei o break para ele não continuar percorrendo a lista depois de finalizar a frase que queriamos
                    if token.text == ',': virgula = True
                if virgula == True: j.valor += 1


            #Verifica se algum dos itens na lista 'exclusivo' está presente na string 'frase.frase'.
            if any(item in frase.frase for item in exclusivo):

                for item in exclusivo:

                    if item in frase.frase:
                        frase.frase = frase.frase.replace(item, "")
                        tokens = nlp(frase.frase)
                        tokens_len = len(tokens) #Aqui eu atualizo o tamanho dos tokens durante a execução do programa

                        #if frase_dividida == null
                        if frase.frase_dividida[i.valor] == "":
                            letra_minuscula += 1
                            frase.frase_logica.append("⊻")
                            
                            #frase.argumentos_divididos_logica[k.valor].append("⊻")
                            frase.frase_logica.append(chr(letra_minuscula))
                            #frase.argumentos_divididos_logica[k.valor].append(chr(letra_minuscula))
                            
                            new_frase = ""

                            cont = 0
                            if(tokens[j.valor].text.lower() == "ou"):
                                j.valor+= 1

                            for palavra in tokens[j.valor + 1:]:
                                if palavra.text != ",":
                                    new_frase += palavra.text + " "
                                    cont += 1

                                else: break
                            frase.frase_dividida[i.valor] += new_frase
                            j.valor += cont + 2

                        #else:
                        else:    
                            letra_minuscula += 1
                            frase.frase_logica.append(chr(letra_minuscula))
                            frase.frase_logica.append("⊻")
                            
                            #frase.argumentos_divididos_logica[k.valor].append(chr(letra_minuscula))
                            #frase.argumentos_divididos_logica[k.valor].append("⊻")
                            frase.frase_dividida.append("")
                            i.valor+= 1
                            break
                    
            else:
                letra_minuscula += 1
                frase.frase_logica.append(chr(letra_minuscula))

                frase.condicao_atual = "∨"
                trata_virgula(frase)

                frase.frase_logica.append("∨")
                
                frase.ultimo_simbolo, frase.parenteses = (None, False) if frase.parenteses == True else ("∨", False) 

                #frase.argumentos_divididos_logica[k.valor].append(chr(letra_minuscula))
                #frase.argumentos_divididos_logica[k.valor].append("∨")
                frase.frase_dividida.append("")
                i.valor += 1
        else:
            if(frase.frase_dividida[i.valor] == ""):
                frase.frase_dividida[i.valor] += tokens[j.valor].text

            else:
                frase.frase_dividida[i.valor] += " " + tokens[j.valor].text
        j.valor += 1

    # Incrementa a letra_minuscula após o loop
    #Daqui pra baixo é bugado quando ele passa pela frase vazia

    #if:
    #frase.frase_logica garante que a lista não é vazia e 
    if frase.frase_logica and (not frase.frase_logica[-1].isalpha() and frase.frase_logica[-1] != ")"):
        letra_minuscula += 1
        
        frase.frase_logica.append(chr(letra_minuscula))
        frase.argumentos_divididos_logica[k.valor].append(chr(letra_minuscula))

        resultado = ' '.join(frase.frase_logica)
        frase.resultado = resultado
        print(f"frase logica depois de tudo = {frase.frase_logica}")
    
    #Caso a frase seja só um "p", por exemplo!
    elif not frase.frase_logica and frase.frase_dividida[0]:
        letra_minuscula += 1
        frase.frase_logica.append(chr(letra_minuscula))

def limpar_texto(texto):
    # Normaliza caracteres Unicode (NFKC = forma normalizada compatível)
    texto = unicodedata.normalize('NFKC', texto)

    # Remove caracteres de controle invisíveis (ex.: ZWSP, ZWNJ, etc.)
    texto = re.sub(r'[\u200B-\u200D\uFEFF]', '', texto)

    # Substitui múltiplos espaços por um único espaço
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto

def main():

    print("-----------------------------------------------")
    while True:
        try:
            frase = Frase(input(""))
            #print(frase.frase)

            natural_para_proposicional(frase)

            if(frase.tipo == 1):
                print(f"FRASE LOGICA = {frase.frase_logica}")
                frase.argumentos_divididos_logica[0], frase.argumentos_divididos_logica[1] = frase.argumentos_divididos_logica[1], frase.argumentos_divididos_logica[0] 
                #print("ESSE")
                resultado = " → ".join(" ".join(argumento) for argumento in frase.argumentos_divididos_logica)

                resultado_lista = list(resultado)

                #print(resultado_lista)

                cont = -1
                nova_letra = 96 + 15

                for indice, i in enumerate(resultado_lista):

                    if i.isalpha():
                        nova_letra += 1
                        cont += 1

                        if i != chr(nova_letra):
                            letra_atual = ord(i)

                            frase_atual = frase.frase_dividida[cont]

                            resultado_lista[indice] = chr(nova_letra)

                            frase.frase_dividida[cont] = frase.frase_dividida[letra_atual - (96 + 16)]

                            for j in range(indice + 1, len(resultado_lista)):

                                if resultado_lista[j] == chr(nova_letra):
                                    resultado_lista[j] = chr(letra_atual)
                                    frase.frase_dividida[letra_atual - (96 + 16)] = frase_atual

                resultado = "".join(resultado_lista)

                print(f"\n{resultado}\n")

                cont = 0
                for i in frase.frase_dividida:
                    print(f"{chr(96 + 16 + cont)}: {i}")
                    cont += 1
                print("")

            else:
                print("")
                for i in frase.frase_logica:
                    print(i, end = " ")
                print("\n")

                cont = 0
                for i in frase.frase_dividida:
                    print(f"{chr(96 + 16 + cont)}: {i}")
                    cont += 1
                print("")

            print("-----------------------------------------------")
        except EOFError:
            print("Fim da entrada.")
            break

# main()

def main2():
    while True:    
        try:
            print("TESTE")
            texto = Lista_Frases(input(""))
        
        except EOFError:
            print("Fim da entrada.")
            break
# main2()