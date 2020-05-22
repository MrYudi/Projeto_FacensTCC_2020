from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import numpy
import os

base = os.path.dirname(os.path.abspath(__file__))
IMG_SIZE = 200
filePath = base+"/redeNeural/Dataset/COINS/1.png"

# load model
model = load_model('redeNeural/bestmodel.h5')

x = img_to_array(load_img(filePath, target_size=(IMG_SIZE, IMG_SIZE)))
X= []
X.append(x)

X = numpy.asarray(X)

prediction = model.predict( X )
print(prediction)

