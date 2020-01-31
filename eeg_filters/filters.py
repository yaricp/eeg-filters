# -*- coding: utf-8 -*-
"""
Module especially for filtering signal EEG.
It based on Butterworth filter from scipy.signal
You can look example:
https://scipy-cookbook.readthedocs.io/items/ButterworthBandpass.html

"""
import numpy as np
from scipy.signal import butter, filtfilt   #lfilter,


def get_tick_times(fs: int, time_measuring: float) -> list:
    """get times of measured value of EEG signal """
    n = int(time_measuring * fs)       # total number of samples
    return np.linspace(0, time_measuring, n, endpoint=False)


def make_filter(dataset: list, bandwidth: list, fs: int, order: int) -> list:
    """
    Apply Butterworth bandpass filter to dataset with bandwidth
    input:
        dataset - data of EEG signal for filtering;
        bandwidth - list of borders frequencies for filtering in Hz;
        fs - frequency sample rate;
        order - order of Butterworth filter;
    output:
        list of filtered data of EEG signal
    """
    # prepare data of signal
    data = np.array(dataset)
    # convert border frequencies from Hz 
    # to sampling frequency of the digital system
    nyq = 0.5 * fs
    normal_bandpass = [bandwidth[0] / nyq, bandwidth[1] / nyq]
    # applying Butterworth filter
    b, a = butter(order, normal_bandpass, btype='bandpass', analog=False)
    # b, a  - Numerator (b) and denominator (a) polynomials of the IIR filter
    return filtfilt(b, a, data) #lfilter(b, a, data)


def search_max_min(list_ticks: list, signal_data: list, where_find: list) -> dict:
    """
    Function searches maximum and minimum in slice of dataset.
    Also it searches time of maximum and minimum.
    input:
        list_ticks - list of time of measured value in EEG signal;
        signal_data - list of values of EEG signal;
        where_find - list of border of times for search extremums;
    Function returns the dictionary of extremums.
    First element of tuple in row of dictionary is a time,
    second is value of extremum.

    """
    begin_index = get_index_time(list_ticks, where_find[0])
    end_index = get_index_time(list_ticks, where_find[1])
    search_slice = signal_data[begin_index:end_index]
    local_max = np.amax(search_slice)
    local_min = np.amin(search_slice)
    max_index = np.where(search_slice == np.amax(search_slice))[0][0]
    min_index = np.where(search_slice == np.amin(search_slice))[0][0]
    return {'max': (list_ticks[begin_index + max_index], local_max),
            'min': (list_ticks[begin_index + min_index], local_min)}


def get_index_time(list_ticks: list, time: float) -> int:
    """Get index in time ticks list by float value of seconds"""
    ticks_array = np.array(list_ticks)
    index = np.where(ticks_array >= time)[0][0]
    return index
