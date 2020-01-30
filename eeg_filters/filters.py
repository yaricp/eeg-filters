# -*- coding: utf-8 -*-
import numpy as np
from scipy.signal import butter, lfilter


def get_tick_times(fs: int, time_measuring: float) -> list:
    """get ticks time of measured value """
    n = int(time_measuring * fs)       # total number of samples
    return np.linspace(0, time_measuring, n, endpoint=False)


def butter_filter(
                data: list,
                cutoff: int,
                fs: int,
                btype: str,
                order: int = 5
                ) -> list:
    """Make filter of list of data"""
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
    return lfilter(b, a, data)


def make_filter(row: list, bandwidth: list, fs: int, order: int) -> list:
    """Function  filters dataset by bandwidth"""
    data = np.array(row)
    cutted_low_data = butter_filter(
            data,
            bandwidth[1],
            fs,
            'low',
            order
            )
    cutted_high_data = butter_filter(
            cutted_low_data,
            bandwidth[0],
            fs,
            'high',
            order
            )
    return cutted_high_data


def search_max_min(list_ticks: list, data: list, where_find: list) -> dict:
    """
    Function searches maximum and minimum in slice of dataset.
    Also it searches time of maximum and minimum.
    Function returns the dictionary of extremums.
    First element of tuple in row of dictionary is a time,
    second is value of extremum.

    """
    begin_index = get_index_time(list_ticks, where_find[0])
    end_index = get_index_time(list_ticks, where_find[1])
    search_slice = data[begin_index:end_index]
    local_max = np.amax(search_slice)
    local_min = np.amin(search_slice)
    max_index = np.where(search_slice == np.amax(search_slice))[0][0]
    min_index = np.where(search_slice == np.amin(search_slice))[0][0]
    return {'max': (list_ticks[begin_index + max_index], local_max),
            'min': (list_ticks[begin_index + min_index], local_min)}


def get_index_time(list_ticks: list, time: float) -> int:
    """Get index in time ticks list by floay value of seconds"""
    ticks_array = np.array(list_ticks)
    index = np.where(ticks_array >= time)[0][0]
    return index
