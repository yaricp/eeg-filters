import numpy as np
from scipy.signal import butter, lfilter, freqz


def get_tick_times(fs, time_measuring):
    '''
    
    '''
    T = time_measuring
    n = int(T * fs)     # total number of samples
    t = np.linspace(0, T, n, endpoint=False)    #tick of measuring
    return t

def butter_filter(data, cutoff, fs, btype, order=5):
    '''
    
    '''
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
    y = lfilter(b, a, data)
    return y
    

def make_filter(row, bandwidth, fs, order):
    '''
    Function  filters dataset by bandwidth
    '''
    data  = np.array(row)
    cutted_low_data = butter_filter(data, bandwidth[1], fs, 'low', order)
    cutted_high_data = butter_filter(cutted_low_data, bandwidth[0], fs, 'high', order)
    filtred_data = cutted_high_data
    return filtred_data


def search_max_min(list_ticks, data, where_find):
    '''
    Function searches maximum and minimum in slice of dataset. 
    Also it searches time of maximum and minimum.
    Function returns the dictionary of extremums.
    First element of tuple in row of dictionary is a time, 
    second is value of extremum.
    '''
    search_slice = data[where_find[0]:where_find[1]]
    local_max = np.amax(search_slice)
    local_min = np.amin(search_slice)
    time_max = np.where(search_slice == np.amax(search_slice))[0][0]
    time_min = np.where(search_slice == np.amin(search_slice))[0][0]
    return {'max':(list_ticks[where_find[0]+time_max], local_max), 
            'min':(list_ticks[where_find[0]+time_min], local_min)}
            