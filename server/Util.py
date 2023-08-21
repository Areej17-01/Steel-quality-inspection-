import cv2
import pickle
import sklearn
from sklearn.preprocessing import StandardScaler
import numpy as np
import json
from keras.models import load_model


__locations = None
__data_columns = None
__model = None

def classify_image(image_bytes):
    load_save_artifacts()
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    #img = cv2.imread(image, cv2.IMREAD_COLOR)

    image = cv2.resize(img, (120, 120))
    image = image / 255
    X = np.array(image)
    print(X.shape)

    single_image = X
    single_image_with_batch = np.expand_dims(single_image, axis=0)

    y_pred = __model.predict(single_image_with_batch)

    predicted_classes = np.argmax(y_pred, axis=1)

    values={0:1,1:2,2:3,3:4}

    print("This steel image has defect label:",values[predicted_classes[0]])



def load_save_artifacts():
    print("loading artifact..............start")
    global __model
    if __model is None:
        __model = load_model('artifacts\my_model_steel.h5')
    print("loading saved artifacts........done")




if __name__ == "__main__":
    load_save_artifacts()
    #classify_image('0002cc93b.JPG')
    binary_image_data = open('0002cc93b.JPG', "rb").read()
    classify_image(binary_image_data)

