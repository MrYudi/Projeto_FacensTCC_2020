from keras.models import load_model
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import cv2
import numpy as np
import os
from keras.utils import np_utils
import pandas as pd

IMG_SAVE_PATH = 'Dataset'

# Carrega o Modelo
print("Carregando modelo...")
model = load_model('RedeNeural/libras-alfabeto-model.h5')
print("Modelo carregado\n\n")

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
data, labels = zip(*dataset)
labels = list(map(mapper, labels))

# one hot encode the labels
labels = np_utils.to_categorical(labels)
print("Fim - Ajeita os dados")

X_train, X_test, y_train, y_test = train_test_split(np.array(data), np.array(labels), stratify=labels, test_size=0.4, random_state=42)

dados_pred = []
dados_real = []

#for l in labels:
for l in y_test:
#for l in y_train:
    dados_real.append(np.argmax(np.array([l]), axis = 1)[0])

#for d in data:
for d in X_test:
#for d in X_train:
    dados_pred.append(np.argmax(model.predict(np.array([d])), axis = 1)[0])

print(confusion_matrix(dados_real,dados_pred))

