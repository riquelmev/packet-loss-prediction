import pickle
import numpy
import numpy as np
from absl import logging
from absl import flags
from absl import app
import glob
import os
import math
import csv


FLAGS = flags.FLAGS

flags.DEFINE_string('trace_dir', None, 'Traces.')

def main(argv):
    FLAGS.trace_dir = argv[1]
    one_frame_file = "/home/vicente/PycharmProjects/prism-neural-net/one_frame_cluster_one_week.csv"
    two_frame_file = "/home/vicente/PycharmProjects/prism-neural-net/two_frame_cluster_one_week.csv"
    three_frame_file = "/home/vicente/PycharmProjects/prism-neural-net/three_frame_cluster_one_week.csv"
    four_frame_file = "/home/vicente/PycharmProjects/prism-neural-net/four_frame_cluster_one_week.csv"
    five_frame_file = "/home/vicente/PycharmProjects/prism-neural-net/five_frame_cluster_one_week.csv"


    #one cluster
    with open(one_frame_file, 'w') as one_frame:
        # one_frame_writer = csv.writer(one_frame)    
        for trace_file in glob.glob(os.path.join(FLAGS.trace_dir,"**/*stats.csv"),recursive = True):
            with open(trace_file, 'r') as read_file:
                loaded_trace = read_file.readlines()  
                for i in range(len(loaded_trace)):
                    one_frame.writelines(loaded_trace[i])

    #two cluster
    with open(two_frame_file, 'w') as two_frame:
        two_frame_writer = csv.writer(two_frame)    

        for trace_file in glob.glob(os.path.join(FLAGS.trace_dir,"**/*stats.csv"),recursive = True):
            with open(trace_file, 'r') as read_file:
                two_frame_reader = csv.reader(read_file, delimiter = ',')
                rows = list(two_frame_reader)
                for i in range(len(rows)-1):
                    two_frame_writer.writerow([rows[i][0],rows[i+1][0], 
                    rows[i][1], rows[i+1][1],rows[i][2]])
                
    #three cluster
    with open(three_frame_file, 'w') as three_frame:
        three_frame_writer = csv.writer(three_frame)    

        for trace_file in glob.glob(os.path.join(FLAGS.trace_dir,"**/*stats.csv"),recursive = True):
            with open(trace_file, 'r') as read_file:
                three_frame_reader = csv.reader(read_file, delimiter = ',')
                rows = list(three_frame_reader)
                for i in range(len(rows)-2):
                    three_frame_writer.writerow([rows[i][0],rows[i+1][0], rows[i+2][0],rows[i][1], rows[i+1][1], rows[i+2][1],rows[i][2]])
        
    #four cluster
    with open(four_frame_file, 'w') as four_frame:
        four_frame_writer = csv.writer(four_frame)    

        for trace_file in glob.glob(os.path.join(FLAGS.trace_dir,"**/*stats.csv"),recursive = True):
            with open(trace_file, 'r') as read_file:
                four_frame_reader = csv.reader(read_file, delimiter = ',')
                rows = list(four_frame_reader)
                for i in range(len(rows)-3):
                    four_frame_writer.writerow([rows[i][0],rows[i+1][0], rows[i+2][0],
                    rows[i+3][0], rows[i][1], rows[i+1][1], rows[i+2][1], rows[i+3][1],rows[i][2]])

    #five cluster
    with open(five_frame_file, 'w') as five_frame:
        five_frame_writer = csv.writer(five_frame)    

        for trace_file in glob.glob(os.path.join(FLAGS.trace_dir,"**/*stats.csv"),recursive = True):
            with open(trace_file, 'r') as read_file:
                five_frame_reader = csv.reader(read_file, delimiter = ',')
                rows = list(five_frame_reader)
                for i in range(len(rows)-4):
                    five_frame_writer.writerow([rows[i][0],rows[i+1][0], rows[i+2][0],
                    rows[i+3][0], rows[i+4][0],rows[i][1], rows[i+1][1], rows[i+2][1], rows[i+3][1], rows[i+4][1],rows[i][2]])

if __name__ == '__main__':
    app.run(main)