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
    for trace_file in glob.glob(os.path.join(FLAGS.trace_dir,"*window.pickle")):
        clean_file = trace_file[:-7] #removes .pickle ending
        clean_file = clean_file + "clean.pickle"
        clean_window_holder = []
        with open(clean_file, 'wb+') as output_file:
            with open(trace_file, 'rb') as read_file:
                loaded_trace = pickle.load(read_file)
                for i in range(len(loaded_trace['windows_data'])):
                    for j in range(len(loaded_trace['windows_data'][i])):
                        hasNan = True in (math.isnan(x) for x in loaded_trace['windows_data'][i][j])
                        loaded_trace['windows_data'][i][j] = [0 if math.isnan(x) else x for x in loaded_trace['windows_data'][i][j]]
                        if hasNan:
                            loaded_trace['windows_data'][i][j].append(1)
                        else:
                            loaded_trace['windows_data'][i][j].append(0)
                pickle.dump(loaded_trace, output_file)

if __name__ == '__main__':
    app.run(main)
