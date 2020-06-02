import cv2
import os

# Como funciona:
# Aperte a letra do teclado, ele salvará na pasta com mesmo nome.
# Aperta Escape para sair do programa

video = cv2.VideoCapture(0)
path = 'capturaImagem/Dataset/'
count = 0
dicionario = {
65:'A',66:'B',67:'C',68:'D',69:'E',70:'F',
71:'G',72:'H',73:'I',74:'J',75:'K',76:'L',
77:'M',78:'N',79:'O',80:'P',81:'Q',82:'R',
83:'S',84:'T',85:'U',86:'V',87:'W',88:'X',
89:'Y',90:'Z'}

while(1):
    _, frame = video.read()
    cv2.imshow("Video", frame)
   
    k = cv2.waitKey(30) & 0xff # Escape
    if k == 27:
        break
    elif (65 <= k and k <= 90) or (97 <= k and k <= 122):

        if(97 <= k and k <= 122): #caso seja minusculo
            k = k - 32

        count = 1 + count
        nomeArquivo = dicionario[k] + str(count)+'.jpg'
        caminho = path + dicionario[k]

        if not os.path.isdir(caminho): 
            os.mkdir(caminho) # Cria a pasta, caso nao exista

        cv2.imwrite(caminho +'/'+ nomeArquivo, frame) 
        print("Imagem: " + nomeArquivo)

video.release()
cv2.destroyAllWindows()