from keras.models import load_model
from keras.preprocessing.image import img_to_array
import os
import cv2
import numpy as np

# Como funciona:
# Aperta Escape para sair do programa
# Coloque a luva na frente da camera

# Configuração
video = cv2.VideoCapture(0)
tamanho_img = 200
frame_analise = 10 # quantos frame irão passa para realizar uma análise
#dicionario = {
#0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',
#6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',
#12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',
#18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',
#24:'Y',25:'Z'}

dicionarioAtual = {
0:'A',1:'B',2:'C',3:'M',4:'N'}

# Carrega o Modelo
print("Carregando modelo...")
model = load_model('redeNeural/bestmodel.h5')
print("Modelo carregado")

# Inicializa
count_frame = 0
classe = '?'

while(1):
    _, frame = video.read() # Captura o frame
    
    cv2.putText(frame,classe,(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),2,cv2.LINE_AA) # Coloque o texto da classe
    cv2.imshow("Video", frame) # Exiba

    count_frame = count_frame + 1
    
    frame = cv2.resize(frame, (tamanho_img,tamanho_img), interpolation = cv2.INTER_AREA) # Converte o tamanho da imagem
    array_frame = np.asarray([img_to_array(frame)]) # pre-processamento

    if(count_frame >= frame_analise): # Análisa
        prediction = model.predict(array_frame) # Prediz
        classe = dicionarioAtual[np.argmax(prediction, axis = 1)[0]] # Pega o maior valor da array

        # Formatação da predict, apenas curiosidade
        textoPrediction = ''
        for d,p in zip(dicionarioAtual.keys(),prediction[0]):
            textoPrediction = textoPrediction + str(dicionarioAtual[d]) +"="+str(round(p, 5))+" | "

        print()
        print(classe)
        print(textoPrediction)

        count_frame = 0

    k = cv2.waitKey(30) & 0xff # Escape
    if k == 27:
        break

video.release()
cv2.destroyAllWindows()
