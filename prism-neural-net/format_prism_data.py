import os
import json
import jsonlines
import pickle
import sys
import glob
from absl import logging
from absl import flags
from absl import app
import glob

FLAGS = flags.FLAGS

flags.DEFINE_string('trace_dir', None, 'Traces.')



def main(argv):
    FLAGS.trace_dir = argv[1]
 #_ws.col.No.,_ws.col.Time,ip.src,ip.dst,tcp.seq,tcp.ack,tcp.len,tcp.port
    for raw_window_file in glob.glob(os.path.join(FLAGS.trace_dir,"*PRISM.pickle")):
        trace_number = 0
        training_window_file = raw_window_file[:-7] #removes .pickle ending
        training_window_file = training_window_file + "window.pickle"
        with open(training_window_file, 'wb+') as output_file:
            with open(raw_window_file, 'rb') as read_file:
                loaded_trace = pickle.load(read_file)
                training_data_20_windows = []
                predicted_windows = []
                if len(loaded_trace['data']) > 0:
                    for i in range(int(len(loaded_trace['data'])-24)):
                        if len(loaded_trace['data']) > 25:
                            train_data = [x[1:] for x in loaded_trace['data'][i:i+20]]
                            predicted_window = loaded_trace['data'][i+24]
                            #lost_packets_windows = predicted_window[-2]
                            training_data_20_windows.append(train_data)
                            predicted_windows.append(predicted_window)
                pickle.dump({'windows_data':training_data_20_windows,'predicted_windows': predicted_windows,'trace_number':trace_number}, output_file)


if __name__ == '__main__':
    app.run(main)
