import pickle
import numpy
import numpy as np
from absl import logging
from absl import flags
from absl import app
import glob
import os
import math


FLAGS = flags.FLAGS

flags.DEFINE_string('trace_dir', None, 'Traces.')

def main(argv):
    FLAGS.trace_dir = argv[1]
    for trace_file in glob.glob(os.path.join(FLAGS.trace_dir,"*clean_loss.pickle")):
        with open(trace_file, 'rb') as read_file:
            loaded_trace = pickle.load(read_file)
            print("loss",len(loaded_trace['input_data']))
    for trace_file in glob.glob(os.path.join(FLAGS.trace_dir,"*clean_no_loss.pickle")):
        with open(trace_file, 'rb') as read_file:
            loaded_trace = pickle.load(read_file)
            print("noloss:",len(loaded_trace['input_data']))
            print(len(glob.glob(os.path.join(FLAGS.trace_dir,"*clean.pickle"))))

if __name__ == '__main__':
    app.run(main)
