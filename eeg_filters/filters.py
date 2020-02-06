# -*- coding: utf-8 -*-

"""
Module especially for filtering signal EEG.

It based on Chebyshev filter from scipy.signal
You can look example:
https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.cheby1.html
Also you can search extremums in EEG signal into time borders.

"""

import numpy as np
from scipy.signal import filtfilt, cheby1   # lfilter, butter,
import matplotlib.pyplot as plt


def show_plot(
                list_times: list,
                list_ticks: list,
                list_data: list,
                bandwidth: list,
                fs: int,
                order: int = 3,
                rp: int = 2,
                iterator: float = 0.004,
                max_region: list = None,
                min_region: list = None) -> None:
    """ Function shows plot of data. """

    ITERATOR = iterator
    iter_value = 0
    for time_stamp, dataset in zip(list_times, list_data):
        data = make_filter(
                    dataset,
                    bandwidth,
                    fs,
                    order,
                    rp
                    )
        iter_value -= ITERATOR
        y = data + iter_value
        plt.plot(
                list_ticks, y, 'g-',
                linewidth=1,
                label='filtered data '+str(time_stamp))
        if max_region:
            max_t, max_y = search_max_min(
                                        list_ticks,
                                        y,
                                        max_region,
                                        'max'
                                        )
            plt.plot(
                    [max_t, ],
                    [max_y, ],
                    'ro',
                    markersize=2
                    )
        if min_region:
            min_t, min_y = search_max_min(
                                        list_ticks,
                                        y,
                                        min_region,
                                        'min'
                                        )
            plt.plot(
                    [min_t, ],
                    [min_y, ],
                    'bo',
                    markersize=2
                    )
    plt.axis([0, list_ticks[-1], iter_value-2*ITERATOR, 2*ITERATOR])
    plt.xlabel('bandwidth: %s' % bandwidth)
    plt.grid()
    name = 'filtered%s' % bandwidth
    plt.savefig('{}.{}'.format(name, 'png'), fmt='png')
    try:
        plt.show()
    except Exception as e:
        raise(e)


def make_filter(
                dataset: list,
                bandwidth: list,
                fs: int,
                order: int,
                rp: int) -> list:
    """
    Apply Chebyshev bandpass filter to dataset with bandwidth.

    input:
        dataset - data of EEG signal for filtering;
        bandwidth - list of borders frequencies for filtering in Hz;
        fs - frequency sample rate;
        order - order of Chebyshev filter;
        rp - The maximum ripple allowed below unity gain in the passband;
    Returns:
        list of filtered data of EEG signal.

    """

    #  prepare data of signal
    data = np.array(dataset)
    #  convert border frequencies from Hz
    #  to sampling frequency of the digital system
    nyq = 0.5 * fs
    normal_bandpass = [bandwidth[0] / nyq, bandwidth[1] / nyq]
    #  applying Butterworth filter
    #  b, a = butter(
    b, a = cheby1(
            N=order,
            rp=rp,
            Wn=normal_bandpass,
            btype='bandpass',
            analog=False)
    #  b, a  - Numerator (b) and denominator
    #  (a) polynomials of the IIR filter
    return filtfilt(b, a, data)  # lfilter(b, a, data)


def search_max_min(
                list_ticks: list,
                signal_data: list,
                where_find: list,
                what_find: str) -> tuple:
    """
    Function searches maximum and minimum in slice of dataset.

    Also it searches time of maximum and minimum.
    input:
        list_ticks - list of time of measured value in EEG signal;
        signal_data - list of values of EEG signal;
        where_find - list of border of times for search extremums;
        what_find - 'max' or 'min';
    Returns: tuple -  time, value.

    """

    begin_index = get_index_time(list_ticks, where_find[0])
    end_index = get_index_time(list_ticks, where_find[1])
    search_slice = signal_data[begin_index:end_index]
    if what_find == 'max':
        extremum_value = np.amax(search_slice)
        extremum_index = np.where(search_slice == np.amax(search_slice))[0][0]
    else:
        extremum_value = np.amin(search_slice)
        extremum_index = np.where(search_slice == np.amin(search_slice))[0][0]
    return list_ticks[begin_index + extremum_index], extremum_value


def get_index_time(list_ticks: list, time: float) -> int:
    """
    Get index in time ticks list by float value of seconds.

    Returns: integer value of index.

    """

    ticks_array = np.array(list_ticks)
    return np.where(ticks_array >= time)[0][0]
