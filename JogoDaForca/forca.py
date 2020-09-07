import re
import sys
import os

# Configurações
limiteTentativa = 8

# Limpa o console
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# Recebe a palavra do usuario
def recebePalavra():
    while True:
        palavra = input("Digite uma palavra: ").upper()

        if(verificar(palavra)):
            return palavra
        else:
            print("Palavra invalida")

# Verifica se a palavra ou letra pode esta dentro das regras
def verificar(palavra):
    
    temp = re.search(r"[^A-Z]+", palavra)
    
    if(not temp == None):
        return False
    else:
        return True
    
# Recebe Letra do usuario
def recebeLetra():
    while True:
        letra = input("Digite uma letra: ").upper()

        if(not (len(letra) > 1) and verificar(letra)):
            return letra
        else:
            print("Não é uma letra")

# Estado do jogo (perdeu? ganhou?)
def status(vida, pergunta, resposta):
    
    # Derrota
    if(vida <= 0):
        print("Você perdeu. A resposta é: "+resposta)
        sys.exit()

    # Vitoria
    if(not (pergunta.find(resposta) == -1)):
        print("Você ganhou")
        sys.exit()

# Substitui a letra na palavra (pergunta)
def substitui(pergunta,resposta,letra):

    temp = ""
    for p,r in zip(pergunta,resposta):
        if(r == letra):
            temp += r
        else:
            temp += p

    return temp

if __name__ == '__main__':

    cls()

    # Recebe a palavra
    resposta = recebePalavra()
    print(resposta)

    # Preparação do jogo
    vida = limiteTentativa
    pergunta = ""
    historico = ""
    for i in range(0,len(resposta)):
        pergunta += "-"

    while True:
        
        cls()
        print("Vida: " + str(vida))
        print("Letra usadas:"+historico)
        print(pergunta)

        # Verificar vitoria e derrota
        status(vida, pergunta, resposta)

        # Recebe a letra do usuario
        letra = recebeLetra()

        # Essa letra já foi?
        if(not (historico.find(letra) == -1)):
            # Já foi
            print("Essa letra já foi usado")
        
        # Existe essa letra?
        elif(not (resposta.find(letra) == -1)):
            # Encontrou
            pergunta = substitui(pergunta,resposta,letra)     

        else:
            # Não encotrou, então perde vida
            historico = historico+" "+letra 
            vida = vida - 1

