import pickle as pickle
import sklearn
from sklearn.model_selection import train_test_split
import numpy as np
from numpy import argmax
from absl import logging
from absl import flags
from absl import app
import glob
import os
import math


x_raw = []
y_raw= []
x_loss = []
y_loss =[]
x_no_loss = []
y_no_loss = []


FLAGS = flags.FLAGS


flags.DEFINE_string('trace_dir', None, 'Traces.')

def main(argv):
    FLAGS.trace_dir = argv[1]
    for trace_file in glob.glob(os.path.join(FLAGS.trace_dir,"*clean_loss.pickle")):
        with open(trace_file, 'rb') as read_file:
            loaded_trace = pickle.load(read_file)
            print(loaded_trace.keys())

            print(loaded_trace['label'][0])
            if loss_rate[1] > 0:
                x_loss.append(loss_rate[0])

                y_loss.append(1)

            else:
                total = total +1

x_loss = np.asarray(x_loss)
y_loss = np.asarray(y_loss)

with open("/home/vicente/storage/data/x_loss_data50msListFilter.pickle", 'wb') as f:
    pickle.dump(x_loss, f)

with open("/home/vicente/storage/data/y_loss_data50msListFilter.pickle", 'wb') as f:
    pickle.dump(y_loss, f)

if __name__ == '__main__':
    app.run(main)
