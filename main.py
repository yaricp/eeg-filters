import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, freqz

from settings import *

filepath = 'data.txt'


def dict_curves_from_file(filepath):
    dict_curves = {}
    with open(filepath,'r') as file:
        text = file.read()
    data = text.split('Data:')[1]
    rows = data.split('\r\n')

    for row in rows:
        list1 = row.split(':')
        if len(list1)>1:
            list2 = list1[1].split('   ')
            count_cols = len(list2)

    for row in rows:
        list1 = row.split(':')
        if len(list1)>1:
            list2 = list1[1].split('   ')
            for i in xrange(count_cols):
                value = list2[i].replace(' ','')
                if value:
                    flag_minus = False
                    if value.find('-') !=-1:
                        flag_minus = True
                    value = value.replace('-','')
                    float_value = float(value)
                    if flag_minus:
                        float_value = -float_value
                    if dict_curves.has_key(i):
                        curv = dict_curves[i]
                        curv.append(float_value)
                    else:
                        curv = [float_value]
                    dict_curves.update({i:curv})

    return dict_curves


def butter_filter(data, cutoff, fs, btype, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
    y = lfilter(b, a, data)
    return y


#http://qaru.site/questions/130793/creating-lowpass-filter-in-scipy-understanding-methods-and-units
dict_curves = dict_curves_from_file(filepath)
fs = SAMPLE_RATE
T = TIME_GAUGING
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
iter = 0
for bandwidth in BANDWIDTHS:
    for key_curv in dict_curves.keys():
        data  = np.array(dict_curves[key_curv])
        cutted_low_data = butter_filter(data, bandwidth[1], fs, 'low', ORDER)
        cutted_high_data = butter_filter(cutted_low_data, bandwidth[0], fs, 'high', ORDER)
        filtred_data = cutted_high_data
        max_value = max(filtred_data)
        #print max_value
        iter += ITER
        y = filtred_data + iter
        plt.plot(t, y, 'g-', linewidth=2, label='filtered data '+str(key_curv))

    plt.xlabel('Time [sec]')
    plt.grid()
    #plt.legend()
    plt.subplots_adjust(hspace=0.95)
    plt.show()
