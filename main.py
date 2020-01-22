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
    #dict_curves = {}
    list_times = []
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
                list_times = [row.split('   ')[i].replace(' ','') for i in range(1,len(row.split('   '))-1)]
                tmp_count = 0
            else:
                target_list = append_data_to_list(target_list,row)
                
    list_out = np.array(target_list).transpose()
    #print(list_out)
                
    return simple_rate, list_times, list_out


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

def make_filter(row, bandwidth, fs):
    data  = np.array(row)
    cutted_low_data = butter_filter(data, bandwidth[1], fs, 'low', ORDER)
    cutted_high_data = butter_filter(cutted_low_data, bandwidth[0], fs, 'high', ORDER)
    filtred_data = cutted_high_data
    return filtred_data
    
def search_max_min(list_ticks, data):
    search_slice = data[START_SEARCH:END_SEARCH]
    local_max = np.amax(search_slice)
    local_min = np.amin(search_slice)
    time_max = np.where(search_slice == np.amax(search_slice))[0][0]
    time_min = np.where(search_slice == np.amin(search_slice))[0][0]
    return {'max':(list_ticks[START_SEARCH+time_max], local_max), 
            'min':(list_ticks[START_SEARCH+time_min], local_min)}
    
def make_graphics(list_ticks, main_dict, bandwidth):
    iter = 0
    last_max_value = 0
    dict_data = main_dict['%s' % bandwidth]
    for time_stamp, row in dict_data.items():
        ext_dict = row['ext']
        iter -= ITER + last_max_value
        y = row['data'] + iter
        plt.plot(list_ticks, y, 'g-', 
                linewidth=2,
                label='filtered data '+str(time_stamp))
        plt.plot([ext_dict['max'][0], ], 
                [ext_dict['max'][1] + iter, ],
                'ro')
        plt.plot([ext_dict['min'][0], ], 
                [ext_dict['min'][1] + iter, ], 
                'bo')
        last_max_value = max(row['data'])
    plt.axis([0, list_ticks[-1],iter-2*ITER, 2*ITER])
    plt.xlabel('bandwidth: %s'% bandwidth)
    plt.grid()
    plt.show()

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
    '''
    Write data to putput
    '''
    
    #print(out_dict)
    with open('output/filter%s.dat' % bandwidth,'a') as outfile:
        for i in range(1, len(out_dict)+1):
            outfile.write('     '+str(i))
        outfile.write('\n')
        for row in range(0,3000):
            outfile.write('   %s:   ' % str(row+1))
            for col in range(0, len(out_dict)):
                outfile.write('%s    '% out_dict[col][row])
            outfile.write('\n')

def start_calc():
    #http://qaru.site/questions/130793/creating-lowpass-filter-in-scipy-understanding-methods-and-units
    fs, list_times, list_data = prepare_data_from_file(filepath)
    T = TIME_GAUGING
    n = int(T * fs)     # total number of samples
    t = np.linspace(0, T, n, endpoint=False)    #tick of measuring
    dict_bandwidth_data = {}
    for bandwidth in BANDWIDTHS:
        create_head_output_file(bandwidth)
        dict_curves_filtred = {}
        for key_curv, row in zip (list_times, list_data):
            filtred_data = make_filter(row, bandwidth, fs)
            ext_dict = search_max_min(t, filtred_data)
            dict_curves_filtred.update({key_curv:{'data':filtred_data, 
                                                    'ext': ext_dict, 
                                                }
                                        })
        dict_bandwidth_data.update({'%s' % bandwidth:dict_curves_filtred})
    for bandwidth in BANDWIDTHS:
        make_graphics(t, dict_bandwidth_data, bandwidth )
        #write_out_data(bandwidth, dict_curves_filtred)
    print(dict_bandwidth_data)

if __name__ == "__main__":
    start_calc()
