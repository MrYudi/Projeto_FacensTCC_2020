# BIBLIOTECA

import sys, pygame, random
import re # Regex
import subprocess # Chama outros scripts do python
from pygame.locals import * # Algumas constante de Teclado

# Verificando erros de inicializacao
check_errors = pygame.init()
if check_errors[1] > 0:
    print("Ops, {0} o Pygame iniciou com algum problema..." . format(check_errors[1]))
    sys.exit(-1)
else:
    print("O Pygame foi inicializado com sucesso!")

#---------------------------------------------
# Configurações
LARGURA_TELA = 500 # Não é recomendado alterar esse campo
ALTURA_TELA = 500 # Não é recomendado alterar esse campo
FONTE = "comicsans" # Não é recomendado alterar esse campo
BASE_IMAGEM = "JogoDaForca\imagem\\" # Local das imagens do jogo da forca
listaPalavra = ["Torrada","Controle","Computador"] # Lista de palavra possiveis
#---------------------------------------------
# CLASSES E OBJETOS

class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

class jogo_logica():
    def __init__(self):
        self.vida = 8
        self.palavra_pergunta = self.palavra_reposta = ""
        self.historico = ""
        self.letra = ""
        self.derrota = False
        self.vitoria = False

    # Reinicia as variaveis
    def restart(self):
        self.vida = 8
        self.palavra_pergunta = self.palavra_reposta = ""
        self.historico = ""
        self.letra = ""
        self.derrota = False
        self.vitoria = False

    # Verifica se a palavra ou letra pode esta dentro das regras
    def __verificar(self,palavra):
        
        temp = re.search(r"[^A-Z]+", palavra)
        
        if(not temp == None):
            return False
        else:
            return True
        
    # Recebe a palavra do usuario
    def recebePalavra(self,palavra=None):
        if palavra == None:
            while True:
                palavra = input("Digite uma palavra: ").upper()

                if(self.__verificar(palavra)):
                    self.palavra_reposta = palavra
                    self.__inicializa_pergunta()
                    return palavra
                else:
                    print("Palavra invalida")
        else:
            palavra = palavra.upper()
            if(self.__verificar(palavra)):
                self.palavra_reposta = palavra
                self.__inicializa_pergunta()
                return palavra
            else:
                raise("A palavra: "+palavra+" esta em um formato inaceitavel.")

    # Prepara a quantidade de espaço na pergunta
    def __inicializa_pergunta(self):
        self.palavra_pergunta = ""
        for i in range(0,len(self.palavra_reposta)):
            self.palavra_pergunta = self.palavra_pergunta + "-"

    # Recebe Letra do usuario
    def recebeLetra(self):
        while True:
            self.letra = input("Digite uma letra: ").upper()

            if(not (len(self.letra) > 1) and self.__verificar(self.letra)):
                return self.letra
            else:
                print("Não é uma letra")

    # Estado do jogo (perdeu? ganhou?)
    def status(self):
        
        # Derrota
        if(self.vida <= 0):
            #print("Você perdeu. A resposta é: "+self.palavra_reposta)
            self.derrota = True

        # Vitoria
        if(not (self.palavra_pergunta.find(self.palavra_reposta) == -1)):
            #print("Você ganhou")
            self.vitoria = True

    # Substitui a letra na palavra (pergunta)
    def substitui(self):

        temp = ""
        for p,r in zip(self.palavra_pergunta,self.palavra_reposta):
            if(r == self.letra):
                temp += r
            else:
                temp += p

        self.letra = ""
        self.palavra_pergunta = temp

    # Quando o usuario erra a letra
    def perde_vida(self):
        self.historico = self.historico+" "+self.letra 
        self.vida = self.vida - 1
        self.letra = ""

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_img(source, x, y,surface):
    surface.blit(pygame.image.load(source), (x, y)) 

#---------------------------------------------
# TELAS

# MENU PRINCIPAL
startButton = button((0,255,0),(LARGURA_TELA/2)-175,(ALTURA_TELA/2)-50,350,100,"Aleatório")
customButton = button((0,255,0),(LARGURA_TELA/2)-175,(ALTURA_TELA/2)+60,350,100,"Escolha palavra")

def main_menu(jogo):  

    screen.fill((0, 0, 0))
    draw_text('Jogo da forca', pygame.font.SysFont(FONTE, 60), (255, 255, 255), screen, 110, 60)
          
    # Lista de eventos MENU
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if startButton.isOver(pygame.mouse.get_pos()):
                print("EVENTO: Botão Iniciar pressionado")
                jogo.recebePalavra(listaPalavra[random.randint(0, len(listaPalavra)-1)])
                print(jogo.palavra_reposta)
                return False
            if customButton.isOver(pygame.mouse.get_pos()):
                print("EVENTO: Botão Custom pressionado")
                jogo.recebePalavra()
                return False
        if event.type == pygame.MOUSEMOTION:
            if startButton.isOver(pygame.mouse.get_pos()):
                startButton.color = (255,0,0)
            else:
                startButton.color = (0,255,0)

            if customButton.isOver(pygame.mouse.get_pos()):
                customButton.color = (255,0,0)
            else:
                customButton.color = (0,255,0)

    startButton.draw(screen,(0,0,0))
    customButton.draw(screen,(0,0,0))
    return True

# JOGO DA FORCA
deduziButton = button((0,255,0),200,50,250,100,"Tentar")

def jogo_da_forca(jogo):

    deduzi = False # Variavel que libera para o usuario escolher a letra 

    screen.fill((0,0,0))
    jogo.status() # Verifica vitoria ou derrota
    
    # Design da tela
    draw_img(BASE_IMAGEM+str(jogo.vida)+".png",50,30,screen)
    draw_text(jogo.palavra_pergunta,pygame.font.SysFont(FONTE, 60),(255,255,255),screen,200,170)
    draw_text("Letras erradas:",pygame.font.SysFont(FONTE, 60),(255,255,255),screen,30,250)
    draw_text(jogo.historico,pygame.font.SysFont(FONTE, 60),(255,255,255),screen,25,300)
    deduziButton.draw(screen)    

    # LISTA DE EVENTO JOGO DA FORCA
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print("EVENTO: Cancelo partida")
                jogo.palavra_reposta = ""
                return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if deduziButton.isOver(pygame.mouse.get_pos()):
                print("EVENTO: Botão deduzi pressionado")
                deduzi = True 
        if event.type == pygame.MOUSEMOTION:
            if deduziButton.isOver(pygame.mouse.get_pos()):
                deduziButton.color = (255,0,0)
            else:
                deduziButton.color = (0,255,0)

    #jogo.derrota = True
    #jogo.vitoria = True    

    if(jogo.vitoria):
        draw_text("Você ganhou",pygame.font.SysFont(FONTE, 40),(0,255,0),screen,40,350)
        draw_text('Aperte "Escape" para volta',pygame.font.SysFont(FONTE, 40),(255,255,255),screen,40,440)

    elif(jogo.derrota):
        draw_text("Você perdeu",pygame.font.SysFont(FONTE, 40),(255,0,0),screen,40,350)
        draw_text("A resposta é: "+jogo.palavra_reposta,pygame.font.SysFont(FONTE, 40),(255,0,0),screen,40,390)
        draw_text('Aperte "Escape" para volta',pygame.font.SysFont(FONTE, 40),(255,255,255),screen,40,440)

    elif(deduzi):

        # Recebe a letra do usuario
        #jogo.recebeLetra() # Recebe letra pelo console, apenas para debug
        jogo.letra = subprocess.check_output([sys.executable, "JogoDaForca/cameraDeduz.py"]).decode("utf-8")[0]
        
        # Essa letra já foi?
        if(not (jogo.historico.find(jogo.letra) == -1)):
            # Já foi
            print("Essa letra já foi usado")

        # Existe essa letra?
        elif(not (jogo.palavra_reposta.find(jogo.letra) == -1)):
            # Encontrou
            jogo.substitui()     

        else:
            # Não encotrou, então perde vida
            jogo.perde_vida()

    return False

#---------------------------------------------
# LOOP PRINCIPAL  

screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA)) # Tamanho da tela
pygame.display.set_caption("Jogo da forca") # Titulo da tela
menu = True
jogo = jogo_logica()

while True:

    if menu:
        jogo.restart() #limpa as variaveis
        menu = main_menu(jogo)       
    else:
        menu = jogo_da_forca(jogo)

    pygame.display.update() # Atualiza a tela do jogo


        
        
        

        
