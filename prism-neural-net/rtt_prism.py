import os
import sys
import csv
import pandas as pd
import statistics as stat
from scipy import stats
import pickle as pickle
import numpy as np
from absl import logging
from absl import flags
from absl import app
import glob

FLAGS = flags.FLAGS

flags.DEFINE_string('trace_dir', None, 'Traces.')

def get_packet(data,index):
    return (data["_ws.col.No."][index], data["_ws.col.Time"][index], data["ip.src"][index], 
    data["ip.dst"][index],  data["tcp.seq"][index], data["tcp.ack"][index], 
    data["tcp.len"][index], data["tcp.port\n"][index])

def get_rtt_packet(data,index):
    return (data["time"][index], data["RTT"][index], data["size"][index], 
    data["lost"][index])

    
#Remove quotation marks, and convert to numerical value. 
#Int for no, seq, ack, len, port and float for time.
def clean_field_value(item):
    entry_item = item[1].replace('"','')
    if item[0] in ["_ws.col.No.","tcp.seq","tcp.ack","tcp.len", "tcp.port\n"]:
        entry_item = int(entry_item)
    elif item[0] == "_ws.col.Time":
        entry_item = float(entry_item)
    return entry_item
    


def main(argv):
    FLAGS.trace_dir = argv[1]
    del(argv)
    trace_id = 0
    for trace_file in glob.glob(os.path.join(FLAGS.trace_dir,"*.csv")):
        if "packet_stats" in trace_file:
            continue
        data = {}
        trace = open(trace_file,"r").readlines()
        fields = trace[0].split(",") 
         #_ws.col.No.,_ws.col.Time,ip.src,ip.dst,tcp.seq,tcp.ack,tcp.len,tcp.port
         #Loop over lines in a file and store each field as an array in data
        for field_name in fields:
            data[field_name] = []
        for line in trace[1:]:
            for item in zip(fields,line.split(',')):
                entry_item = clean_field_value(item)
                data[item[0]].append(entry_item)

        #filters out small secondary flows by extracting the max sequence number
        # and using that to determine the primary flow
        max_sequence_index = data["tcp.seq"].index(max(data["tcp.seq"]))
        main_source = data["ip.src"][max_sequence_index]
        main_dest = data["ip.dst"][max_sequence_index]
        main_port = data["tcp.port\n"][max_sequence_index]

        #Split trace into packets and acks, and detect lost packets
        packets = {}
        packets_lost = {}
        acks = {}

        #Check if the packet is a data packet by comparing source, size and port.
        #Number, Time, Source, Destination, Seq, Ack, LenPort, TCP
        for i in range(len(data["_ws.col.No."])):
            num,time,src,dst,seq,ack,size,port = get_packet(data, i)
            if src == main_source and size > 0 and port == main_port:
                if seq in packets:
                    packets_lost[packets[seq]] = True
                else:
                    packets_lost[i] = False
                packets[seq] = i
            #checks for acks using src and size
            if src == main_dest and size == 0:
                acks[ack] = i
        per_packet_stats = {"time":[],"size":[],"lost":[],"RTT":[]}
        bytes_sent = 0
        bytes_recieved = 0

        for i in sorted(packets_lost.keys()):
            if i > 10:
                num,time,src,dst,seq,_,size,port = get_packet(data, i)
                rtt = None
                if packets_lost[i] == False:
                    ack = seq + size
                    bytes_sent += size
                    if ack in acks:
                        rtt = data["_ws.col.Time"][acks[ack]] - time
                    per_packet_stats["lost"].append(False)
                else:
                    per_packet_stats["lost"].append(True)
                per_packet_stats["time"].append(time)
                per_packet_stats["size"].append(size)
                per_packet_stats["RTT"].append(rtt)

                bytes_recieved += size
        per_window_stats = []

        if len(per_packet_stats["time"]) > 500:
            start = per_packet_stats['time'][0]
            wasThereLoss = False
            window = []
            i = 0
            currentWindow = start
            windowSize = 1/60
            interval = 1/60
            actualLossCount= set()
            bytesholder = [0]
            lostbytesholder = [0]
            rttholder = []
            single_loss_holder = []

            #Constucts 50ms windows
            while i < len(per_packet_stats["time"]) and currentWindow < per_packet_stats["time"][-1]:
                while i < len(per_packet_stats["time"]) and per_packet_stats["time"][i] < currentWindow + windowSize:                    
                    window.append(i)
                    i += 1

                window_packet_rtt = []
                window_packet_timestamps = []
                packet_window_lost = 0
                window_bytes_sent = 0
                lost_bytes = 0


                for packet in window:
                    time,packet_rtt,size,lost = get_rtt_packet(per_packet_stats, packet)
                    #[time, seq, len, rtt, Loss?]
            

                    if packet_rtt is not None:
                        window_packet_rtt.append(packet_rtt)
                        window_packet_timestamps.append(time)
                        window_bytes_sent += size
                    if lost:
                        window_bytes_sent += size
                        lost_bytes += size
                        if time not in actualLossCount:
                            packet_window_lost += 1
                            actualLossCount.add(time)

                #window_stats data is in the order of start time of window, min rtt, max rtt, mean rtt, varience of rtt, slope, intercept, number of lost packets lost, number of packets in window
                if len(window_packet_rtt) > 1:
                    window_stats = [round(currentWindow, 2), min(window_packet_rtt), max(window_packet_rtt), stat.mean(window_packet_rtt), stat.variance(window_packet_rtt)]
                elif len(window_packet_rtt) == 1:
                    window_stats= [round(currentWindow, 2), min(window_packet_rtt), max(window_packet_rtt), stat.mean(window_packet_rtt), np.nan]
                else:
                    window_stats= [round(currentWindow, 2), np.nan, np.nan, np.nan, np.nan]
                if len(window_packet_rtt) > 1:
                    slope, intercept, r, p, se = stats.linregress(window_packet_timestamps, window_packet_rtt)
                    window_stats.append(slope)
                    window_stats.append(intercept)
                else:
                    window_stats.append(np.nan)
                    window_stats.append(np.nan)
                window_stats.append(packet_window_lost)
                window_stats.append(len(window))
                if packet_window_lost > 0:
                    wasThereLoss = True
                per_window_stats.append(window_stats)
                if len(window_packet_rtt) > 0:
                    rttholder.append(stat.mean(window_packet_rtt))
                else:
                    rttholder.append(np.nan)
                
                bytesholder.append(window_bytes_sent)
                lostbytesholder.append(lost_bytes)


                currentWindow += interval
                while len(window) > 0 and per_packet_stats['time'][window[0]] <= currentWindow:
                    window.pop(0)

            per_window_stats = {'windowFields':['WindowTimeStamp', 'MinRtt','MaxRtt','MeanRtt','Varience','Slope','Intercept','NumPacketsLost','NumPackets'], 'data':per_window_stats,'LossFound':wasThereLoss,'TotalPackets':len(per_packet_stats), 'TotalBytesSuccessfullyTransmitted': bytes_sent, 'TotalBytesAttempted': bytes_recieved}
            temp_file = trace_file[:-4] #removes .csv
            trace_file = temp_file + 'PRISM.pickle'
            if len(rttholder) < 500:
                continue
            if np.nanmin(rttholder) < 0.002 or np.nanmax(rttholder) > 0.2:
                continue

            trace_id +=1
            with open(trace_file, 'wb') as f:
                pickle.dump(per_window_stats, f)
            

            packet_stats_file = temp_file[:-4]
            packet_stats_file = packet_stats_file + "_packet_stats.csv"
            with open(packet_stats_file, 'w') as psf:
                writer = csv.writer(psf)
                for i in range(len(bytesholder)):
                    writer.writerow([lostbytesholder[i], bytesholder[i], trace_id])
                 

            # bytesfile = temp_file[:-4]
            # bytesfile = bytesfile + "Bytes0.16.txt"
            # lostbytesfile = temp_file[:-4]
            # lostbytesfile = lostbytesfile + "LostBytes0.16.txt"
            # rttfile = temp_file[:-4]
            # rttfile = rttfile + "AvgRTT0.16.txt"
            # with open(bytesfile, 'w') as bytes_file:
            #     bytes_file.writelines("window size is " + str(windowSize))
            #     bytes_file.writelines("interval size is" + str(interval) + "\n")
            #     bytes_file.writelines(["%s\n" % item for item in bytesholder])
            # with open(lostbytesfile, 'w') as lost_file:
            #     lost_file.writelines("window size is " + str(windowSize))
            #     lost_file.writelines("interval size is" + str(interval) + "\n")
            #     lost_file.writelines(["%s\n" % item for item in lostbytesholder])
            # with open(rttfile, 'w') as rtt_file:
            #     rtt_file.writelines("window size is " + str(windowSize))
            #     rtt_file.writelines("interval size is" + str(interval) + "\n")
            #     rtt_file.writelines(["%s\n" % item for item in rttholder])


if __name__ == '__main__':
    app.run(main)