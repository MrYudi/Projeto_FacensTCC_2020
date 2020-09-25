from keras.models import load_model
import cv2
import numpy as np

# Como funciona:
# Aperta Escape para sair do programa
# Coloque a mao na frente da camera dentro do quadrado

# Configuração
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
tamanho_img = 400
frame_analise = 25 # quantos frame irão passa para realizar uma análise
X = 60
Y = 60
FILTRO_CONFIRMACAO = 5 # Se o programa confirma, por exemplo, letra A cinco vezes seguidos, entao usuario esta realmente fazendo A
#dicionario = {
#0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',
#6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',
#12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',
#18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',
#24:'Y',25:'Z'}

dicionarioAtual = {
0:'A',1:'B',2:'L'}

# Carrega o Modelo
model = load_model('RedeNeural/libras-alfabeto-model.h5')

# Main
classe_anterior = classe_atual = '?' # Anterior -> deduçao antiga | atual -> da tentativa atual
count_frame = count_filtro = 0
analise = False # A camera pode começa a análisa
while(True):
    _, frame = video.read() # Captura o frame
    frame_original = frame.copy()

    if not analise:
        cv2.putText(frame_original,'Aperte "Enter" para iniciar',(60,40), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA) # Coloque o texto da classe_atual

    cv2.putText(frame_original,classe_atual,(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),2,cv2.LINE_AA) # Coloque o texto da classe_atual

    count_frame = count_frame + 1
    
    frame = frame[Y:Y+tamanho_img, X:X+tamanho_img] # Corte
    frame = cv2.resize(frame, (227, 227)) # Pre-processamento

    
    if(analise and count_frame >= frame_analise): # Análisa
        prediction = model.predict(np.array([frame])) # Prediz
        classe_atual = dicionarioAtual[np.argmax(prediction, axis = 1)[0]] # Pega o maior valor da array

        # Formatação da predict, apenas afins de debug
        #textoPrediction = ''
        #for d,p in zip(dicionarioAtual.keys(),prediction[0]):
        #    textoPrediction = textoPrediction + str(dicionarioAtual[d]) +"="+str(round(p, 5))+" | "
        #print(textoPrediction)

        if classe_anterior == classe_atual:
            count_filtro += 1
            if count_filtro >= FILTRO_CONFIRMACAO:
                count_filtro = 0
                break
        else:
            count_filtro = 0

        classe_anterior = classe_atual
        count_frame = 0
    
    k = cv2.waitKey(30) & 0xff # Escape
    if k == 27:
        classe_atual = '?'
        break
    if k == ord('\r'): # Enter
        analise = True

    cv2.rectangle(frame_original, (X, Y), (X + tamanho_img, Y + tamanho_img), (0,255,0), 0)
    #cv2.imshow("Imagem capturada", frame) # Exiba imagem que sera enviado para rede neural, afins de Debug
    cv2.imshow("Camera", frame_original) # Exiba
    
video.release()
cv2.destroyAllWindows()

print(classe_atual) # Return subprocess