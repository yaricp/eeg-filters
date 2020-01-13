import os, sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
#from pylab import plot as plt
import numpy as np
from scipy.signal import butter, lfilter, freqz

from settings import *

filepath = 'input/data.txt'

            
                

def prepare_data_from_file(filepath):
    '''function get rows from input file and append data to dictionary of data'''
    dict_curves = {}
    dict_times = {}
    position = ''
    tmp_count = 0
    target_list = []
    with open(filepath,'r') as file:
        for row in file.readlines():
            if row.find('Sampling rate: ') != -1:
                simple_rate = float(row.split('Sampling rate: ')[1].replace('Hz',''))
                continue
            elif row.find('Measure times:') !=-1:
                position = 'times'
                tmp_count = 0
                continue
            elif row.find('Data:') !=-1:
                position = 'curves'
                tmp_count = 0
                continue
            elif position == '':
                continue
            elif tmp_count == 0:
               tmp_count += 1
               continue
            if position == 'times':
                dict_times = [row.split('   ')[i].replace(' ','') for i in range(1,len(row.split('   '))-1)]
                tmp_count = 0
            else:
                target_list = append_data_to_list(target_list,row)
                
    list_out = np.array(target_list).transpose()
    #print(list_out)
                
    return simple_rate, dict_times, list_out


def append_data_to_list(target_list,row):
    ''' Append data from row of file to dict of data'''
    row = row.replace('\n','')
    row_splitted = row.split(':')[1].split('   ')
    rowlist = []
    for i in range(1,len(row_splitted)):
        value = float(row_splitted[i].replace(' ',''))
        rowlist.append(value)
    target_list.append(rowlist)
    return target_list

#def append_data_to_dict(target_dict,row):
#    ''' Append data from row of file to dict of data'''
#    row = row.replace('\n','')
#    row_splitted = row.split(':')[1].split('   ')
#    for i in range(1,len(row_splitted)):
#        value = row_splitted[i].replace(' ','')
#        flag_minus = False
#        if value.find('-') !=-1:
#            flag_minus = True
#        value = value.replace('-','')
#        float_value = float(value)
#        if flag_minus:
#            float_value = -float_value
#        if i-1 in target_dict.keys():
#            list_data = target_dict[i-1]
#            list_data.append(float_value)
#        else:
#            list_data = [float_value]
#        target_dict.update({i-1:list_data})
#    return target_dict


def butter_filter(data, cutoff, fs, btype, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
    y = lfilter(b, a, data)
    return y

def create_head_output_file(bandwidth):
    '''create header of output files'''
    with open(filepath,'r') as file:
        textfile = file.read()
        header = textfile.split('Data:')[0]+'\n Data: \n'
        #sys.exit(0)
        with open('output/filter%s.dat' % bandwidth,'a') as outfile:
            outfile.write(header)


def write_out_data(bandwidth, out_dict):
    '''Write data to putput'''
    with open('output/filter%s.dat' % bandwidth,'a') as outfile:
        for i in range(1, len(out_dict)+1):
            outfile.write('     '+str(i))
        outfile.write('\n')
        for row in range(0,3000):
            outfile.write('   %s:   ' % str(row+1))
            for col in range(0, len(out_dict)):
                outfile.write('%s    '% out_dict[col][row])
            outfile.write('\n')


#http://qaru.site/questions/130793/creating-lowpass-filter-in-scipy-understanding-methods-and-units
fs, dict_times, list_data = prepare_data_from_file(filepath)
T = TIME_GAUGING
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
iter = 0
data = np.array(list_data[0])
print(len(list_data[0]))
print(list_data[0])
plt.plot(t, list_data[0], 'b-', linewidth=2, label='clear data ')
#plt.switch_backend('WXAgg')
plt.grid()
plt.subplots_adjust(hspace=0.55)
plt.show()
data  = list_data[0]
cutted_low_data = butter_filter(data, BANDWIDTHS[-1][1], fs, 'low', ORDER)
cutted_high_data = butter_filter(cutted_low_data, BANDWIDTHS[-1][0], fs, 'high', ORDER)
filtred_data = cutted_high_data
y = filtred_data
plt.plot(t, y, 'g-', linewidth=2, label='filtered data ')
plt.grid()
plt.subplots_adjust(hspace=0.55)
plt.show()
#print(dict_curves.keys())
#sys.exit(0)
for bandwidth in BANDWIDTHS:
    create_head_output_file(bandwidth)
    dict_curves_filtred = {}
    counter = 0
    last_max_value = 0
    for row in list_data:
        data  = np.array(row)
        cutted_low_data = butter_filter(data, bandwidth[1], fs, 'low', ORDER)
        cutted_high_data = butter_filter(cutted_low_data, bandwidth[0], fs, 'high', ORDER)
        filtred_data = cutted_high_data
        
        #dict_curves_filtred.update({key_curv:filtred_data})
        iter += ITER + last_max_value
        y = filtred_data + iter
        plt.plot(t, y, 'g-', linewidth=2, label='filtered data '+str(counter))
        counter += 1
        last_max_value = max(filtred_data)
    write_out_data(bandwidth, dict_curves_filtred)

    plt.xlabel('bandwidth: %s'% bandwidth)
    plt.grid()
    #plt.legend()
    #plt.subplots_adjust(hspace=0.55)
    plt.show()


