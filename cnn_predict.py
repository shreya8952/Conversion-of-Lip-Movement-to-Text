import itertools
import numpy as np
import matplotlib.pyplot as plt

# from sklearn import svm, datasets
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import confusion_matrix
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers

import cnnmodel
from scipy import misc
from keras.preprocessing import image as image_utils


def predict():
    final_path = 'concatenated_images/'
    #read every image and run it

    print("[INFO] Loading image")
    image = image_utils.load_img(final_path)
    image = image_utils.img_to_array(image)
    input_image = np.expand_dims(image, axis=0)

    model = cnnmodel.create_model()
    #weights_path="vgg-finetune-model.h5"
    weights_path="vgg16_1.h5"
    model.load_weights(weights_path)

    #test_datagen = ImageDataGenerator(rescale=1./255)
    #validation_generator = test_datagen.flow_from_directory(
    #        validation_data_dir,
    #        target_size=(img_height, img_width),
    #        batch_size=32,
    #        shuffle=False,
    #        class_mode='categorical')

    model.compile(loss='categorical_crossentropy',
                metrics=['accuracy'])
    prediction = model.predict(input_image)
    prediction_class = np.argmax(prediction, axis=1)
    class_names=["Hello", "Good", "Day", "Bye", "Goodbye"]

    return prediction_class[0]


def final_verdict_(frechet_verdict,cnn_verdict):
    final_ver = {"word":'Uknown'}

    if(frechet_verdict == cnn_verdict['word']):
        final_ver = {'word':frechet_verdict}
    
    else:
        ann_verdict = ann_model()
        if(ann_model['confidence'] >= cnn_verdict['confidence']):
            final_ver = ann_verdict
        else:
            final_ver = cnn_verdict

    return final_ver

