import cv2
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.layers import Activation, Dropout, Convolution2D, GlobalAveragePooling2D
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping, ModelCheckpoint
from datetime import datetime
import math
import matplotlib.pyplot as plt
import tensorflow as tf
import os

IMG_SAVE_PATH = 'Dataset'
BASE_PATH = 'RedeNeural/'
GRAFICO_PATH = 'Grafico_rede'

EPOCHS = 20
TAMANHO_TEST = 0.3
VALIDATION_SIZE = 1
BATCH_SIZE = 4
STEPS_PER_EPOCH = 8
DROPOUT = 0.5

# Carrega os dados
print("Carrega dataset")
dataset = []
CLASS_MAP = {}
i = 0
for directory in os.listdir(IMG_SAVE_PATH):
    path = os.path.join(IMG_SAVE_PATH, directory)
    if not os.path.isdir(path):
        continue
    for item in os.listdir(path):
        # to make sure no hidden files get in our way
        if item.startswith("."):
            continue
        img = cv2.imread(os.path.join(path, item))
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #pre-procesamento
        img = cv2.resize(img, (227, 227)) #pre-procesamento
        dataset.append([img, directory])

        if(not directory in CLASS_MAP):
            CLASS_MAP[directory] = i
            i = i + 1
del i
print("Fim - Carrega dataset")

def mapper(val):
    return CLASS_MAP[val]

print("Ajeita os dados")
'''
dataset = [
    [[...], 'A'],
    [[...], 'B'],
    ...
]
'''
data, labels = zip(*dataset)
labels = list(map(mapper, labels))


'''
labels: A,B,B,C,A...
one hot encoded: [1,0,0], [0,1,0], [0,1,0], [0,0,1], [1,0,0]...
'''
# one hot encode the labels
labels = np_utils.to_categorical(labels)
print("Fim - Ajeita os dados")

# Arquitetura SqueezeNet
print("Arquitetura")
model = Sequential([
    SqueezeNet(input_shape=(227, 227, 3), include_top=False),
    Dropout(DROPOUT),
    Convolution2D(len(CLASS_MAP), (1, 1), padding='valid'),
    Activation('relu'),
    GlobalAveragePooling2D(),
    Activation('softmax')
])
model.compile(
    optimizer=Adam(lr=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("Fim - Arquitetura")

model.summary()

# checkpoint
checkpoint = BASE_PATH + "bestModelTextGen.hdf5"
if os.path.isfile(checkpoint):
	model.load_weights(checkpoint)

# Separa os dados treino e teste
X_train, X_test, y_train, y_test = train_test_split(np.array(data), np.array(labels), stratify=labels, test_size=TAMANHO_TEST, random_state=42)
del data
del labels

# Configurações do treinamento
mc = ModelCheckpoint(checkpoint, monitor='loss', verbose=1, save_best_only=True, mode='min')
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=100, min_delta=0.000001)

compute_steps_per_epoch = lambda x: int(math.ceil(1. * x / BATCH_SIZE))
val_steps = compute_steps_per_epoch(VALIDATION_SIZE)

# Inicia o Treinamento
history = model.fit(X_train,  y_train, epochs=EPOCHS, steps_per_epoch=STEPS_PER_EPOCH, callbacks=[es, mc], validation_steps=val_steps, validation_data=(X_test, y_test))

if not os.path.isdir(BASE_PATH+GRAFICO_PATH): 
    os.mkdir(BASE_PATH+GRAFICO_PATH) # Cria a pasta Dataset, caso nao exista

time = datetime.now()
timestampStr = time.strftime("%d %b %Y %H %M %S %f)")
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Modelo Acurácia')
plt.ylabel('Acurácia')
plt.xlabel('Epoca')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig(BASE_PATH+GRAFICO_PATH+'/acuracia_'+timestampStr+'.png')
plt.clf()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Modelo Perda')
plt.ylabel('Perda')
plt.xlabel('Epoca')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig(BASE_PATH+GRAFICO_PATH+"/perda_"+timestampStr+".png")
plt.clf()

# Salva o modelo
model.save(BASE_PATH +"libras-alfabeto-model.h5")