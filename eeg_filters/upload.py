# -*- coding: utf-8 -*-

"""
Module for extract data of EEG signals by time of measuring.

It contain one public function:
    prepare_data - get filepath and give tuple of data;
and one private function:
    __append_data_to_list - for append data to list;
Input file can be only format -.

"""

import numpy as np


def prepare_data(filepath: str) -> tuple:
    """
    Function get rows from input file and put data to dictionary of data.

    input:
        filepath - path to source file with EEG signals;
    Returns:
        sample_rate - Sample rate from file;
        list_times - list times of measured EEG signal;
        list_ticks  - list of times measure;
        list_out - list of lists with values EEG signals
        (list of lists of curves).

    """

    list_times = []
    position = ''
    tmp_count = 0
    target_list = []
    count_measure = 0
    with open(filepath, 'r') as file:
        for row in file.readlines():
            if row.find('Sampling rate: ') != -1:
                sample_rate = float(
                        row.split('Sampling rate: ')[1].replace('Hz', '')
                        )
                continue
            elif row.find('Measure times:') != -1:
                position = 'times'
                tmp_count = 0
                continue
            elif row.find('Data:') != -1:
                position = 'curves'
                tmp_count = 0
                continue
            elif position == '':
                continue
            elif tmp_count == 0:
                tmp_count += 1
                continue
            if position == 'times':
                splitted_row = row.replace('\n', '').split('   ')
                if len(splitted_row) > 1:
                    list_times = [
                            splitted_row[i].replace(' ', '') for i in range(
                                    1, len(splitted_row) - 1
                                    )
                            ]
                tmp_count = 0
            else:
                target_list = __append_data_to_list(target_list, row)
                count_measure += 1
    list_out = np.array(target_list).transpose()
    time_measuring = count_measure/sample_rate
    list_ticks = np.linspace(
                        0,
                        time_measuring,
                        count_measure,
                        endpoint=False)
    return sample_rate, list_times, list_ticks, list_out


def __append_data_to_list(target_list: list, row: str) -> list:
    """
    Append data from row of source file to list of data.

    Returns: list of data.

    """

    row = row.replace('\n', '')
    row_splitted = row.split(':')[1].split('   ')
    rowlist = []
    for i in range(1, len(row_splitted)):
        str_value = row_splitted[i].replace(' ', '')
        if str_value:
            int_value = float(row_splitted[i].replace(' ', ''))
            rowlist.append(int_value)
    target_list.append(rowlist)
    return target_list
