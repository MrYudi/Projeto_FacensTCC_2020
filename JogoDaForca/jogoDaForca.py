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
# Configurações Gerais
LARGURA_TELA = 700 # Não é recomendado alterar esse campo
ALTURA_TELA = 600 # Não é recomendado alterar esse campo
FONTE = "georgia" # Não é recomendado alterar esse campo

COR_BOTAO = (220,220,220)
COR_BOTAO_SELECIONADO = (150,150,150)
COR_BOTAO_BORDA = (100,100,100)

COR_RETANGULO = (200,200,200)

BASE_IMAGEM = "JogoDaForca\imagem\\" # Local das imagens do jogo da forca
listaPalavra = ["Torrada","Controle","Computador","Bola","Gato","Cachorro",
                "Madeira","Macaco","Casa","Elefante","Formiga"] # Lista de palavra possiveis, é recomendado que não tenha mais de 10 letra.
ICON = BASE_IMAGEM + "icon.jpg" # ICON

CAMERA = True # A letra será capturado pela camera ou console? Afins de DEBUG
MOSTRA_PALAVRA = False # Caso sejá aleatorio, será exibido a palavra no console.
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
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),3)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont(FONTE, 40)
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
        self.repetido = False

    # Reinicia as variaveis
    def restart(self):
        self.vida = 8
        self.palavra_pergunta = self.palavra_reposta = ""
        self.historico = ""
        self.letra = ""
        self.derrota = False
        self.vitoria = False
        self.repetido = False

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
startButton = button(COR_BOTAO,(LARGURA_TELA/2)-175,ALTURA_TELA-240,350,100,"Aleatório")
customButton = button(COR_BOTAO,(LARGURA_TELA/2)-175,ALTURA_TELA-120,350,100,"Escolha à palavra")

def main_menu(jogo):  
    
    screen.fill((48,72,136))
    
    draw_text('Jogo da forca', pygame.font.SysFont(FONTE, 60), (255, 255, 255), screen, LARGURA_TELA/2 - 368/2, 60)
    draw_img(BASE_IMAGEM+"menu_img.jpg",0,0,screen)

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
                if MOSTRA_PALAVRA:
                    print(jogo.palavra_reposta)
                return False
            if customButton.isOver(pygame.mouse.get_pos()):
                print("EVENTO: Botão Custom pressionado")
                jogo.recebePalavra()
                return False
        if event.type == pygame.MOUSEMOTION:
            if startButton.isOver(pygame.mouse.get_pos()):
                startButton.color = COR_BOTAO_SELECIONADO
            else:
                startButton.color = COR_BOTAO

            if customButton.isOver(pygame.mouse.get_pos()):
                customButton.color = COR_BOTAO_SELECIONADO
            else:
                customButton.color = COR_BOTAO

    startButton.draw(screen,COR_BOTAO_BORDA)
    customButton.draw(screen,COR_BOTAO_BORDA)
    return True

# JOGO DA FORCA
deduziButton = button(COR_BOTAO,230,50,250,100,"Tentar")
retaguloErradas = button(COR_RETANGULO,10,280,LARGURA_TELA-20,100,"")
retaguloAviso = button(COR_RETANGULO,10,405,LARGURA_TELA-20,180,"")

def jogo_da_forca(jogo):

    deduzi = False # Variavel que libera para o usuario escolher a letra 

    screen.fill((48,72,136))
    jogo.status() # Verifica vitoria ou derrota
    
    # Design da tela
    deduziButton.draw(screen,COR_BOTAO_BORDA)  
    retaguloErradas.draw(screen,COR_BOTAO_BORDA) 
    retaguloAviso.draw(screen,COR_BOTAO_BORDA) 

    draw_img(BASE_IMAGEM+str(jogo.vida)+".png",30,30,screen)
    draw_text(jogo.palavra_pergunta,pygame.font.SysFont(FONTE, 60),(0,0,0),screen,230,170)
    draw_text(jogo.historico,pygame.font.SysFont(FONTE, 60),(0,0,0),screen,25,295)

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
                deduziButton.color = COR_BOTAO_SELECIONADO
            else:
                deduziButton.color = COR_BOTAO

    #jogo.derrota = True
    #jogo.vitoria = True    

    if(jogo.vitoria):
        draw_text("Você ganhou",pygame.font.SysFont(FONTE, 40),(63,152,58),screen,30,ALTURA_TELA-190)
        draw_text('Aperte "Escape" para volta',pygame.font.SysFont(FONTE, 40),(0,0,0),screen,30,ALTURA_TELA-80)

    elif(jogo.derrota):
        draw_text("Você perdeu",pygame.font.SysFont(FONTE, 40),(230,0,0),screen,30,ALTURA_TELA-190)
        draw_text("A resposta é: "+jogo.palavra_reposta,pygame.font.SysFont(FONTE, 40),(230,0,0),screen,30,ALTURA_TELA-140)
        draw_text('Aperte "Escape" para volta',pygame.font.SysFont(FONTE, 40),(0,0,0),screen,30,ALTURA_TELA-80)
    
    elif(deduzi):
        jogo.repetido = False
        # Recebe a letra do usuario (Camera? Console?)
        if CAMERA:  
            # Camera habilitado para IA

            draw_text("Carregando a camera...",pygame.font.SysFont(FONTE, 40),(0,0,0),screen,30,ALTURA_TELA-190)
            draw_text("Aguarde",pygame.font.SysFont(FONTE, 40),(0,0,0),screen,30,ALTURA_TELA-140)
            pygame.display.update()
    
            jogo.letra = subprocess.check_output([sys.executable, "JogoDaForca/cameraDeduz.py"]).decode("utf-8")[0]
        
        else:
            # Recebe letra pelo console, apenas para debug
            draw_text("Letra via console",pygame.font.SysFont(FONTE, 40),(0,0,0),screen,30,ALTURA_TELA-190)
            draw_text("Digite a letra no console",pygame.font.SysFont(FONTE, 40),(0,0,0),screen,30,ALTURA_TELA-140)
            pygame.display.update()
    
            jogo.recebeLetra() 
        
        if not jogo.letra == "?": # Análise foi feita com sucesso
            # Essa letra já foi?
            if(not (jogo.historico.find(jogo.letra) == -1) or not (jogo.palavra_pergunta.find(jogo.letra) == -1)):
                # Já foi
                jogo.repetido = True

            # Existe essa letra?
            elif(not (jogo.palavra_reposta.find(jogo.letra) == -1)):
                # Encontrou
                jogo.substitui()     

            else:
                # Não encotrou, então perde vida
                jogo.perde_vida()
        
    # Letra repetida?
    elif(jogo.repetido):
        draw_text("Letra repetida",pygame.font.SysFont(FONTE, 40),(0,0,0),screen,30,ALTURA_TELA-190)
        draw_text("Escolha outra letra",pygame.font.SysFont(FONTE, 40),(0,0,0),screen,30,ALTURA_TELA-140)
    
    return False

#---------------------------------------------
# LOOP PRINCIPAL  

screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA)) # Tamanho da tela
pygame.display.set_icon(pygame.image.load(ICON))
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


        
        
        

        
