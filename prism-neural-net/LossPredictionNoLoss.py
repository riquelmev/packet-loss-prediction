

import pickle as pickle
import sklearn
from sklearn.model_selection import train_test_split
import numpy as np
from numpy import argmax
import pylab as pl
from tqdm import tqdm
import json
#file = '/SNAPPcapAnalysis/NNdataMlabs.pickle'
# file = 'NNdataMlabs.pickle'
# with open(file, 'rb') as f:
#     load = pickle.load(f)
#
# print("loaded")
#file = '/home/vicente/PycharmProjects/pythonProject/RTTDATA/RTTOUT_1626295365.jsonl'





x_raw = []
y_raw= []

#print(load[0][0])
#print(load[0][1])
bins = []
for i in range(3):
    bins.append([])
count = 0
total_loss = 0
total = 0

x_loss = []
y_loss =[]

x_no_loss = []
y_no_loss = []
#IN_FILE = "NNdataMlabs.jsonl"
#IN_FILE = '/home/vicente/storage/NNdata50ms_NewCleanHopefully.jsonl'
IN_FILE = '/home/vicente/storage/JsonlMaster.jsonl'

# fpath = os.path.join(IN_DIR, IN_FILE)
import jsonlines
# for line in open(IN_FILE).readlines():
#     if line != '\n':
with jsonlines.open(IN_FILE) as f:
    for line in f.iter():
        if line != '\n':
            #window = json.loads(line)
            window = line

            #print(parsed_line)

    #for window in tqdm(load):
            trace = window[1]
            if count % 10000 == 0:
                print(count)
            window = window[0]
            count +=1
            #print(window)
            #temp = np.array(packet[0])
            #print(temp.dtype)
            #print(temp)
            if np.isnan(np.sum(np.array(window[0]))) or np.isnan(np.sum(np.array(window[1]))):
                continue
            #if count > 6000000:
            #if count > 6000000:
            #    break
            #x_raw.append(window[0])
            lossRate = 0.0
            if window[1] == 0 and count > 6000000:# and count < 6000000:
            #if window[1] == 0 and count < 3000000:
                #y_raw.append(0)
                x_no_loss.append(window[0])
                y_no_loss.append(0)
                #total = total +1
            #window = None
    #y_raw.append(window[1])
            # if count == 3000000:
            #     x_no_loss = np.asarray(x_no_loss)
            #     y_no_loss = np.asarray(y_no_loss)
            #     print(type(x_no_loss))
            #     print(type(y_no_loss))
            #
            #     num_classes = 4
            #     # y_loss = tf.keras.utils.to_categorical(y_loss, num_classes)
            #
            #     print("starting pickle")
            #     x_no_loss = np.array_split(x_no_loss, 5)
            #     y_no_loss = np.array_split(y_no_loss, 5)
            #     print(type(x_no_loss))
            #     print(type(y_no_loss))
            #     print(len(x_no_loss))
            #     print(len(y_no_loss))
            #     for i in range(5):
            #         print (y_no_loss[i])
            #     # size= []
            #     # offset = 15
            #     for j in range(5):
            #         print("Iteration: X", j)
            #         with open("/home/vicente/storage/data/x_no_loss" + str(j) + "50msListFilter.pickle", 'wb') as f:
            #             pickle.dump(x_no_loss[j], f)
            #         print(x_no_loss[j].shape)
            #         x_no_loss[j] = 0
            #
            #     for k in range(5):
            #         print(y_no_loss[k])
            #         print("Starting y asarray")
            #         print("Iteration: Y", k)
            #         with open("/home/vicente/storage/data/y_no_loss_data" + str(k) + "50msListFilter.pickle", 'wb') as f:
            #             pickle.dump(y_no_loss[k], f)
            #         # size.append(x_no_loss.shape[0])
            #         y_no_loss[i] = 0
            #         x_no_loss = []
            #         y_no_loss = []

x_no_loss = np.asarray(x_no_loss)
y_no_loss = np.asarray(y_no_loss)

num_classes = 4
#y_loss = tf.keras.utils.to_categorical(y_loss, num_classes)

print("starting pickle")
x_no_loss = np.array_split(x_no_loss,5)
y_no_loss = np.array_split(y_no_loss,5)

#size= []
offset = 10
for i in range(5):
    j=i + offset
    print("Iteration: X", j)
    with open("/home/vicente/storage/data/x_no_loss" + str(j) + "50msListFilter.pickle", 'wb') as f:
        pickle.dump(x_no_loss[i], f)
    print(x_no_loss[i].shape)
    x_no_loss[i] = 0

for i in range(5):
    j=i + offset
    print("Starting y asarray")
    print("Iteration: Y", j)
    with open("/home/vicente/storage/data/y_no_loss_data" + str(j) + "50msListFilter.pickle", 'wb') as f:
        pickle.dump(y_no_loss[i], f)
    #size.append(x_no_loss.shape[0])
    y_no_loss[i] = 0

# for i in range(5):
#     j = i + offset
#     print("Iteration: X", j)
#     with open("/home/vicente/storage/data/x_no_loss" + str(j) + "50ms.pickle", 'wb') as f:
#         pickle.dump(x_no_loss[i], f)
#     print(x_no_loss[i].shape)
#     x_no_loss[i] = 0


# for i in range(5):
#     j = i + offset
#     print("Starting y asarray")
#     print("Iteration: Y", j)
#     with open("/home/vicente/storage/data/y_no_loss_data" + str(j) + "50ms.pickle", 'wb') as f:
#         pickle.dump(y_no_loss[i], f)
#     #size.append(x_no_loss.shape[0])
#     y_no_loss[i] = 0
#

#print(size)
    # with open("y_no_loss_data" + str(i) + ".pickle", 'wb') as f:
    #     pickle.dump(y_no_loss[i], f)
    # y_no_loss[i] = None




#y_no_loss = y_no_loss[0]

#with open("y_no_loss_data.jsonl", 'w') as f:
#    for entry in y_no_loss:
#        json.dumps(entry, f)
#        f.write('\n')
#y_no_loss = None

# print("done with y no loss")
#




# for i in range(10):
#     file = i
#     with open("x_no_loss_data" + str(i) + ".jsonl", 'w') as f:
#         print("Starting loop:",i)
#         for entry in x_no_loss[i]:
#             json.dumps(entry, f)
#             f.write('\n')
# #