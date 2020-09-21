# BIBLIOTECA

import sys, pygame, re
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
LARGURA_TELA = 500
ALTURA_TELA = 500
FONTE = "comicsans"
BASE_IMAGEM = "JogoDaForca\imagem\\"
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

    # Verifica se a palavra ou letra pode esta dentro das regras
    def __verificar(self,palavra):
        
        temp = re.search(r"[^A-Z]+", palavra)
        
        if(not temp == None):
            return False
        else:
            return True
        
    # Recebe a palavra do usuario
    def recebePalavra(self):
        while True:
            palavra = input("Digite uma palavra: ").upper()

            if(self.__verificar(palavra)):
                self.palavra_reposta = palavra
                return palavra
            else:
                print("Palavra invalida")

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
            print("Você perdeu. A resposta é: "+self.palavra_reposta)
            return False

        # Vitoria
        if(not (self.palavra_pergunta.find(self.palavra_reposta) == -1)):
            print("Você ganhou")
            return True
        return None

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
startButton = button((0,255,0),(LARGURA_TELA/2)-125,(ALTURA_TELA/2)-50,250,100,"Iniciar")

def main_menu():  

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
                return False
        if event.type == pygame.MOUSEMOTION:
            if startButton.isOver(pygame.mouse.get_pos()):
                startButton.color = (255,0,0)
            else:
                startButton.color = (0,255,0)

    startButton.draw(screen,(0,0,0))
    return True

# JOGO DA FORCA
def jogo_da_forca(jogo):

    screen.fill((0,0,0))
    jogo.status() # Precisa demostra a vitoria e derrota

    #draw_img(BASE_IMAGEM+str(jogo.vida)+".png",(LARGURA_TELA/2)-75,30,screen)


    # LISTA DE EVENTO JOGO DA FORCA
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print("EVENTO: Cancelo partida")
                return True

            print("Vida: " + str(jogo.vida))
            print("Letra usadas:"+jogo.historico)
            print(jogo.palavra_pergunta)

            # Recebe a letra do usuario
            jogo.recebeLetra() # ajeita para teste

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
        menu = main_menu()       
    else:
        if(len(jogo.palavra_reposta) == 0 ):
            jogo.recebePalavra()
            jogo.palavra_pergunta = ""

            #Texto do campo "vazio"
            for i in range(0,len(jogo.palavra_reposta)):
                jogo.palavra_pergunta = jogo.palavra_pergunta + "_"
        else:
            menu = jogo_da_forca(jogo)

    pygame.display.update() # Atualiza a tela do jogo


        
        
        

        
