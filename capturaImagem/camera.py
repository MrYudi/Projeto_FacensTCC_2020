import cv2
import os

# Como funciona:
# Aperte a letra do teclado, ele salvará na pasta com mesmo nome.
# Aperta Escape para sair do programa

# Configuração:
path = 'capturaImagem/Dataset/' # Caminho do Dataset
dicionario = { 255: 'NADA',
65:'A',66:'B',67:'C',68:'D',69:'E',70:'F',
71:'G',72:'H',73:'I',74:'J',75:'K',76:'L',
77:'M',78:'N',79:'O',80:'P',81:'Q',82:'R',
83:'S',84:'T',85:'U',86:'V',87:'W',88:'X',
89:'Y',90:'Z'}
limite_frame = 30 # Quantas fotos serão feito?
delay_frame = 10 # Qual é o delay entre as fotos?

if not os.path.isdir(path): 
    os.mkdir(path) # Cria a pasta Dataset, caso nao exista

# Iniciali [não mexer]
video = cv2.VideoCapture(0)
count_nome_frame = 0
count_frame = 30
count_frame_delay = 0
letra = k = 255

while(1):
    _, frame = video.read()
    
    k = cv2.waitKey(30) & 0xff # Escape

    if k == 27:
        break

    if (count_frame < limite_frame):

        count_frame_delay = 1 + count_frame_delay

        if not count_frame_delay < delay_frame:
            count_frame_delay = 0
        
            count_frame = 1 + count_frame
            count_nome_frame = 1 + count_nome_frame

            nomeArquivo = dicionario[letra] + str(count_nome_frame)+'.jpg'
            caminho = path + dicionario[letra]

            if not os.path.isdir(caminho): 
                os.mkdir(caminho) # Cria a pasta, caso nao exista

            cv2.imwrite(caminho +'/'+ nomeArquivo, frame) 
            print("Imagem: " + nomeArquivo)

    else:
        
        if(65 <= k and k <= 90) or (97 <= k and k <= 122):
            if(97 <= k and k <= 122): #caso seja minusculo
                k = k - 32

            letra = k
            count_frame = 0

    cv2.putText(frame,"Frame: "+str(count_frame),(0,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA) 
    cv2.putText(frame,"Letra: "+dicionario[letra],(0,100), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA) 
    cv2.imshow("Video", frame)

video.release()
cv2.destroyAllWindows()