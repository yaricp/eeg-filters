# -*- coding: utf-8 -*-

"""
Module especially for filtering signal EEG.

It based on Chebyshev filter from scipy.signal
You can look example:
https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.cheby1.html
Also you can search extremums in EEG signal into time borders.

"""

import numpy as np
from scipy.signal import filtfilt, cheby1
import matplotlib.pyplot as plt


def show_plot(
    incoming_data: dict,
    bandwidth: list,
    order: int = 3,
    rp: int = 2,
    iterator: float = 0.004,
    max_region: list | None = None,
    min_region: list | None = None,
    testmode: bool = False
) -> tuple | None:
    """ Function shows plot of data. """
    list_times = incoming_data["list_name_curves"]
    list_ticks = incoming_data["list_tick_times"]
    list_curves = incoming_data["list_curves"]
    fs = incoming_data["sample_rate"]
    iter_value: float = 0.0
    for time_stamp, dataset in zip(list_times, list_curves):
        data = apply_filter(
            dataset, bandwidth, fs, order, rp
        )
        iter_value -= iterator
        y = data + iter_value
        plt.plot(
            list_ticks, y, "g-",
            linewidth=1,
            label="filtered data "+str(time_stamp))
        if max_region:
            max_t, max_y = search_max_min(
                list_ticks, y, max_region, "max"
            )
            plt.plot(
                [max_t, ], [max_y, ], "ro", markersize=2
            )
        if min_region:
            min_t, min_y = search_max_min(
                list_ticks, y, min_region, "min"
            )
            plt.plot(
                [min_t, ], [min_y, ], "bo", markersize=2
            )
    plt.axis([0, list_ticks[-1], iter_value-2*iterator, 2*iterator])
    plt.xlabel("bandwidth: %s" % bandwidth)
    plt.grid()
    name = "filtered%s" % bandwidth
    filename = f"{name}.png"
    plt.savefig(filename)
    if testmode:
        return plt, filename
    try:
        plt.show()
    except Exception as e:
        raise Exception(e)
    return None


def apply_filter(
    dataset: list, bandwidth: list, fs: int, order: int, rp: int
) -> list:
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
    b, a = cheby1(
        N=order, rp=rp, Wn=normal_bandpass, btype="bandpass",
        analog=False
    )
    return filtfilt(b, a, data)


def search_max_min(
    list_tick_times: list, signal_data: list, where_find: list,
    what_find: str
) -> tuple:
    """
    Function searches maximum and minimum in slice of dataset.

    Also it searches time of maximum and minimum.
    input:
        list_tick_times - list of time of measured value in EEG signal;
        signal_data - list of values of EEG signal;
        where_find - list of border of times for search extremums;
        what_find - "max" or min;
    Returns: tuple -  time, value.

    """

    begin_index = get_index_time(list_tick_times, where_find[0])
    end_index = get_index_time(list_tick_times, where_find[1])
    search_slice = signal_data[begin_index:end_index]
    if what_find == "max":
        extremum_value = np.amax(search_slice)
        extremum_index = np.where(search_slice == np.amax(search_slice))[0][0]
    else:
        extremum_value = np.amin(search_slice)
        extremum_index = np.where(search_slice == np.amin(search_slice))[0][0]
    return list_tick_times[begin_index + extremum_index], extremum_value


def get_index_time(list_tick_times: list[float], time: float) -> int:
    """
    Get index in time ticks list by float value of seconds.

    Returns: integer value of index.

    """
    ticks_array = np.array(list_tick_times)
    return np.where(ticks_array >= time)[0][0]
