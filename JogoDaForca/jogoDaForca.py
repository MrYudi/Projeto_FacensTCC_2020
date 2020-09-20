# BIBLIOTECA

import sys, pygame
from pygame.locals import * # Algumas constante de Teclado

# Verificando erros de inicializacao
check_errors = pygame.init()
if check_errors[1] > 0:
    print("Ops, {0} o Pygame iniciou com algum problema..." . format(check_errors[1]))
    sys.exit(-1)
else:
    print("O Pygame foi inicializado com sucesso!")

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
   
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

#---------------------------------------------
# TELAS

# MENU PRINCIPAL
startButton = button((0,255,0),120,210,250,100,"Iniciar")

def main_menu():  

    screen.fill((0, 0, 0))
    draw_text('Jogo da forca', pygame.font.SysFont('comicsans', 60), (255, 255, 255), screen, 110, 40)
          
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
def jogo_da_forca():

    screen.fill((255,255,255))

    # LISTA DE EVENTO JOGO DA FORCA
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print("EVENTO: CANCELO PARTIDA")
                return True

    return False

#---------------------------------------------
# LOOP PRINCIPAL  

screen = pygame.display.set_mode((500, 500)) # Tamanho da tela
pygame.display.set_caption("Jogo da forca") # Titulo da tela
menu = True

while True:

    if menu:
        menu = main_menu()       
    else:
        menu = jogo_da_forca()

    pygame.display.update() # Atualiza a tela do jogo


        
        
        

        
