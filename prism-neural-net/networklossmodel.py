from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import Flatten
from keras.layers import Reshape
from keras.layers import MaxPooling2D
from keras.layers import  AveragePooling2D
from keras.layers import Dropout
import gc
import keras
from matplotlib import pyplot as plt
import pandas as pd
from keras.layers import ReLU
from keras.layers import Activation
from tensorflow.keras.applications.vgg16 import VGG16
import tensorflow.keras.applications
from keras.layers.normalization import BatchNormalization
from sklearn import metrics
from sklearn.metrics import classification_report
from keras.metrics import MeanSquaredError
import pickle as pickle
import sklearn
from sklearn.model_selection import train_test_split
import numpy as np
from numpy import argmax
from keras import backend as K
import tensorflow as tf
import pickle
import numpy
import numpy as np
from absl import logging
from absl import flags
from absl import app
import glob
import os
import math
import time


FLAGS = flags.FLAGS

flags.DEFINE_string('trace_dir', None, 'Traces.')

def main(argv):
    FLAGS.trace_dir = argv[1]

    batch_size = 1024
    input_shape = (20,9,1)

    model = Sequential()
    model.add(Reshape(input_shape))
    model.add(Conv2D(64, (4,9), 1, activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2,1)))
    model.add(Conv2D(128, (4,1), 1, activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,1)))
    model.add(Dropout(0.1))
    model.add(Conv2D(256, (2,1),1, activation='relu'))
    model.add(Dropout(0.1))

    model.add(Flatten())


    model.add(Dense(256, activation= 'relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(1, activation='softmax'))


    model.compile(optimizer="Adam", loss='binary_crossentropy', metrics=["mse", "acc"])


    #model = keras.models.load_model('/mount/storage/2classmodelTest0.82')
    print(len(glob.glob(os.path.join(FLAGS.trace_dir,"*clean.pickle"))))
    loss_files = glob.glob(os.path.join(FLAGS.trace_dir,"*clean_loss.pickle"))
    no_loss_files = glob.glob(os.path.join(FLAGS.trace_dir,"*clean_noloss.pickle"))
    print(loss_files)
    print(no_loss_files)

    print(len(loss_files))
    print(len(no_loss_files))

    file_batch_size = 500
    batch_num = len(loss_files) // file_batch_size
    start_time = time.time()
    for i in range(batch_num * 10):
        print(time.time()-start_time)
        i = i % batch_num
        x_train = []
        y_train = []
        x_loss = []
        y_loss = []

        for j in range(file_batch_size):
            j = j + (i * file_batch_size)
            #print("i = ",i)
            #print("j = ", j)
            with open(loss_files[j], 'rb') as lf:
                loss_file = pickle.load(lf)
                x_loss += (loss_file['input_data'])
                y_loss += (loss_file['label'])

            with open(no_loss_files[j], 'rb') as nlf:
                no_loss_file = pickle.load(nlf)
                x_train += (no_loss_file['input_data'])
                y_train += (no_loss_file['label'])
        
        print(len(x_train))
        print(len(x_loss))
        imbalance = len(x_train) // len(x_loss)
        #print(imbalance)
        x_loss += imbalance * x_loss
        y_loss += imbalance * y_loss

        x_train += x_loss
        y_train += y_loss


        print("FINSIHED LOADING ONE BATCH")

        x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.1, shuffle= True)

        history = model.fit(x_train, y_train, validation_data=(x_valid,y_valid), epochs=1, batch_size=batch_size, shuffle=True)

    model.summary()

    # #pred = model.predict(x_val)
    # y_pred_ohe = model.predict(x_val)  # shape=(n_samples, 12)
    # # only necessary if output has one-hot-encoding, shape=(n_samples)
    # y_pred_labels = np.argmax(y_pred_ohe, axis=1)
    # y_cat = np.argmax(y_val, axis=1)
    # print(y_pred_labels)
    # print(y_cat)

    # matrix = metrics.confusion_matrix(y_cat, y_pred_labels)

    # print(matrix)

    # print(classification_report(y_cat,y_pred_labels))

                    
if __name__ == '__main__':
    app.run(main)
