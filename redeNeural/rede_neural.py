import os
from os import listdir
from numpy import asarray
from numpy import save
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split
from PIL import Image
from tensorflow.keras.layers import Conv2D
import sys
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Flatten
from keras.layers import MaxPooling2D
from keras.layers import MaxPool2D
from keras.layers import Conv2D
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.utils import np_utils
import numpy as np
# load ascii text and covert to lowercase
from keras.models import load_model
import matplotlib.pyplot as plt
from keras.layers.normalization import BatchNormalization
import math
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from numpy import array
from numpy import argmax
from datetime import datetime
#import tensorflow as tf
#from keras import backend as k

# Configurações
base = "redeNeural/"
datasetPath = base + "Dataset/"
modelName = base + "bestmodel.h5"
checkpoint = base + "bestModelTextGen.hdf5"
nEpocas = 150
steps_per_epoch = 4
VALIDATION_SIZE = 1
BATCH_SIZE = 8
IMG_SIZE = 200

#config = tf.ConfigProto() # TensorFlow wizardry
#config.gpu_options.allow_growth = True # Don't pre-allocate memory; allocate as-needed
# config.gpu_options.per_process_gpu_memory_fraction = 0.5 # Only allow a total of half the GPU memory to be allocated
#k.tensorflow_backend.set_session(tf.Session(config=config)) # Create a session with the above options specified.

#imagePath = []
y = []
X = []

print("Carrega dataset")
for root, dirs, files in os.walk(datasetPath):
	for dir in dirs:
		for root2, dirs2, files2 in os.walk(datasetPath+dir):
			for file in files2:
				y.append(dir)
				photo = img_to_array(load_img(datasetPath+dir+"/"+file, target_size=(IMG_SIZE, IMG_SIZE)))
				X.append(photo)
print("Fim - Carrega dataset")

print("Ajeita os dados")
X = numpy.asarray(X)
numberClasses = len(np.unique(y))
count = len(y)
values = array(y)
# integer encode
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(values)
# binary encode
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
y = onehot_encoder.fit_transform(integer_encoded)
print("Fim - Ajeita os dados")

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.5, random_state=42)

#VGG
print("Arquitetura")
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', input_shape=(IMG_SIZE, IMG_SIZE, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(BatchNormalization())

model.add(Conv2D(64, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())

model.add(Conv2D(128, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())

model.add(Conv2D(256, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())

model.add(Conv2D(128, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())

model.add(Conv2D(32, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())

model.add(Dropout(0.4))

model.add(Flatten())
model.add(Dense(160, activation='relu'))
model.add(Dense(numberClasses, activation='softmax'))
# load the network weights
print("Fim - Arquitetura")

#checkpoint = "weights-improvement-02-2.3567-bigger.hdf5"

if os.path.isfile(checkpoint):
	model.load_weights(checkpoint)

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics = ['accuracy'])
# define the checkpoint
#filepath="weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"

mc = ModelCheckpoint(checkpoint, monitor='loss', verbose=1, save_best_only=True, mode='min')
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=100, min_delta=0.000001)

# fit the model
compute_steps_per_epoch = lambda x: int(math.ceil(1. * x / BATCH_SIZE))
val_steps = compute_steps_per_epoch(VALIDATION_SIZE)
history = model.fit( X_train, y_train, epochs=nEpocas, steps_per_epoch=steps_per_epoch, callbacks=[es, mc], validation_steps = val_steps, validation_data=(X_test, y_test))

time = datetime.now()
timestampStr = time.strftime("%d %b %Y %H %M %S %f)")
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig(base+'accuracy'+timestampStr+'.png')
plt.clf()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig(base+"loss"+timestampStr+".png")
plt.clf()


print("Saved model to disk")
model.save(modelName)

'''
inverted = label_encoder.inverse_transform([argmax(y_train[0, :])])
print(inverted)
'''
