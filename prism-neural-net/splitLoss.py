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
    for trace_file in glob.glob(os.path.join(FLAGS.trace_dir,"*clean.pickle")):
            clean_file = trace_file[:-7] #removes .pickle ending
            no_loss_file =  clean_file + "_noloss.pickle"
            loss_file = clean_file + "_loss.pickle"
            with open(loss_file, 'wb+') as loss_output_file:
                with open(no_loss_file, 'wb+') as no_loss_output_file:
                    with open(trace_file, 'rb') as read_file:
                        loaded_trace = pickle.load(read_file)
                        loss_holder_input = []
                        no_loss_holder_input = []
                        loss_holder_label = []
                        no_loss_holder_label = []
                        for i in range(len(loaded_trace['windows_data'])):
                            #print(loaded_trace['predicted_windows'][i])
                            #print(loaded_trace['predicted_windows'][i][-2])
                            if loaded_trace['predicted_windows'][i][-2] > 0:
                                loss_holder_input.append(loaded_trace['windows_data'][i])
                                loss_holder_label.append(1)
                                #loss_holder_label.append(loaded_trace['predicted_windows'][i][-2])
                            else:
                                no_loss_holder_input.append(loaded_trace['windows_data'][i])
                                no_loss_holder_label.append(loaded_trace['predicted_windows'][i][-2])       
                        pickle.dump({'input_data':loss_holder_input,'label': loss_holder_label}, loss_output_file)
                        pickle.dump({'input_data':no_loss_holder_input,'label': no_loss_holder_label}, no_loss_output_file)
                    
if __name__ == '__main__':
    app.run(main)
